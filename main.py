from langchain import hub
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from typing_extensions import List, TypedDict
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader
import os
from dotenv import load_dotenv
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from openinference.instrumentation.langchain import LangChainInstrumentor #openifnerence
from opentelemetry.instrumentation.langchain import LangchainInstrumentor #openllemetry
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableLambda
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
import requests
from pydantic import BaseModel, Field
from fastapi import FastAPI, Request, Query
from typing import Optional
from langchain.chat_models import init_chat_model
from fastapi.middleware.cors import CORSMiddleware
from langgraph.checkpoint.memory import MemorySaver
import uuid




load_dotenv()



# Initialize FastAPI app
app = FastAPI()



# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#open inference
resource = Resource.create({"service.name": "langchain-agent-app-openinference"})
# Configure the OTLP exporter for your custom endpoint
provider = TracerProvider(resource=resource)
otlp_exporter = OTLPSpanExporter(
    # Change to your provider's endpoint
    endpoint="https://ingest.us.signoz.cloud:443/v1/traces",
    # Add any required headers for authentication
    headers={"signoz-ingestion-key": os.getenv("SIGNOZ_INGESTION_KEY")},
)
processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

LangChainInstrumentor().instrument()


@tool
def get_flight_tickets(departure: str, arrival: str, departure_date: str, return_date: str):
    """Fetch round trip flight tickets based on departure and arrival destinations and depature and return dates."""
    url = "http://127.0.0.1:8000/flight-tickets"
    params = {"departure": departure, "arrival": arrival, "departure_date": departure_date, "return_date": return_date}
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()


class HotelInput(BaseModel):
    destination: str = Field(description="city destination")
    check_in_date: str = Field(description="Check-in date in the form mm/dd/yyyy")
    check_out_date: str = Field(description="Check-out date in the form mm/dd/yyyy")


@tool(args_schema=HotelInput)
def get_hotel_bookings(destination: str, check_in_date: str, check_out_date: str):
    """Fetch hotel bookings info based on destination and check in and check out date"""
    url = "http://127.0.0.1:8000/hotel-bookings"
    params = {"destination": destination, "check_in_date": check_in_date, "check_out_date": check_out_date}
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()


@tool
def get_weather(destination: str):
    """Get the weather details for a given destination."""
  
    url = "http://127.0.0.1:8000/get-weather"
    # print(url)
    params = {"location": destination}
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()


@tool
def get_activities(destination: str):
    """Fetch tourist activities for a given destination."""
    url = "http://127.0.0.1:8000/get-activities"
    params = {"location": destination}
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()

agent_executor = None
config = None
message_count = 0

# Initialize agent_executor on startup
@app.on_event("startup")
async def startup_event():
    global agent_executor
    memory = MemorySaver()
    
    llm = init_chat_model("gpt-4o-mini", model_provider="openai")
    tools = [get_flight_tickets, get_hotel_bookings, get_weather, get_activities]
    agent_executor = create_react_agent(llm, tools, checkpointer=memory)
    

# Define query route
@app.get("/query")
async def query(
    departure: Optional[str] = None,
    arrival: Optional[str] = None,
    check_in: Optional[str] = None,
    check_out: Optional[str] = None,
    query: Optional[str] = None
):
    """Query route to get travel details."""

    global message_count
    global config

    if departure is not None and arrival is not None and check_in is not None and check_out is not None:
        message_count = 0

    system_message = {
        "role": "system",
        "content": (
            "You are a smart travel assistant. The user will only provide:\n"
            "- departure location\n"
            "- arrival location\n"
            "- departure date\n"
            "- return date\n"
            "Based on this, you must:\n"
            "1. Get round trip flight tickets.\n"
            "2. Get hotel bookings in the arrival city from arrival to return date.\n"
            "3. Get weather info in the arrival city for the duration.\n"
            "4. Get popular tourist activities in the arrival city.\n"
            "Use the available tools to fetch each of these items.\n"
            "Present the response in a structured and friendly manner, as a travel planner would, including headings and bullet points for clarity.\n"
            "Also include emojis for each heading to make it more engaging."
        )
    }

    if message_count == 0:
        config = {"configurable": {"thread_id": str(uuid.uuid4())}}
        input_message = {
            "role": "user",
            "content": (
                f"I am planning a trip from {departure} to {arrival}. "
                f"I will be checking in on {check_in} and checking out on {check_out}."
            )
        }

        # Invoke agent_executor
        response = agent_executor.invoke({"messages": [system_message, input_message]}, config)

    else:
        input_message = {
            "role": "user",
            "content": query
        }
        response = agent_executor.invoke({"messages": [input_message]}, config)

    message_count += 1
    # Return the response
    return {"response": response["messages"][-1].content}



