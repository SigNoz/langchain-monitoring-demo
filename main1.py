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



load_dotenv()


#open inference
resource = Resource.create({"service.name": "langchain-rag-app-openinference"})
# Configure the OTLP exporter for your custom endpoint
provider = TracerProvider(resource=resource)
otlp_exporter = OTLPSpanExporter(
    # Change to your provider's endpoint
    endpoint="https://ingest.in.signoz.cloud:443/v1/traces",
    # Add any required headers for authentication
    headers={"signoz-ingestion-key": os.getenv("SIGNOZ_INGESTION_KEY")},
)
processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

LangChainInstrumentor().instrument()


location_coordinates = {
    "new york": (40.7128, -74.0060),
    "los angeles": (34.0522, -118.2437),
    "chicago": (41.8781, -87.6298),
    "san francisco": (37.7749, -122.4194),
    "miami": (25.7617, -80.1918),
    "paris": (48.8566, 2.3522),
    "tokyo": (35.6895, 139.6917),
    "sydney": (-33.8688, 151.2093),
    "dubai": (25.276987, 55.296249),
    "london": (51.5074, -0.1278),
}


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

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



# class WeatherInput(BaseModel):
#     location: str = Field(description="city destination location")
#     start_date: str = Field(description="Check-in date in the form yyyy-mm-dd")
#     end_date: str = Field(description="Check-out date in the form yyyy-mm-dd")

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



from langchain.chat_models import init_chat_model
llm = init_chat_model("gpt-4o-mini", model_provider="openai")





tools = [get_flight_tickets, get_hotel_bookings, get_weather, get_activities]
# Tool binding
# model_with_tools = llm.bind_tools(tools)
# Tool calling



agent_executor = create_react_agent(llm, tools)
# input_message = {"role": "user", "content": "what are the round trip flight tickets from New York to Los Angeles?"}
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
        "Present the response in a structured and friendly manner, as a travel planner would, including headings and bullet points for clarity."
    )
}
# input_message = {"role": "user", "content": "I am planning a trip from San Francisco to New York. Please provide me with the following details: \n1. Round trip flight ticket prices and details.\n2. Hotel booking details for New York. I will be checking in on August 10, 2025, and checking out on August 15, 2025.\n3. Important weather details for New York during my stay.\n4. Tourist activities available in New York.\nUse all the tools available to retrieve this information."}
input_message = {"role": "user", "content": "I am planning a trip from Los Angeles to Tokyo. I will be checking in on August 10, 2025, and checking out on August 15, 2025."}
# input_message = {"role": "user", "content": "Hi there how are you doing today?"}
response = agent_executor.invoke({"messages": [system_message, input_message]})
# response = agent_executor.invoke({"messages": [input_message]})
# print(response)
# for message in response["messages"]:
#     message.pretty_print()
print(response["messages"][-1].content)



