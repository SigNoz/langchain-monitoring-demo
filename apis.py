from fastapi import FastAPI, Request
from pydantic import BaseModel
from datetime import datetime
import random

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FlightTicket(BaseModel):
    flight_number: str
    airline: str
    price: float
    departure_time: str
    arrival_time: str
    departure_airport: str  # Added departure_airport field
    arrival_airport: str  # Added arrival_airport field

# Global dictionary mapping departure locations to airlines
location_to_airline = {
    "new york": "Delta Airlines",
    "los angeles": "American Airlines",
    "chicago": "United Airlines",
    "san francisco": "Southwest Airlines",
    "miami": "JetBlue Airways",
    "paris": "Air France",
    "tokyo": "Japan Airlines",
    "sydney": "Qantas",
    "dubai": "Emirates",
    "london": "British Airways",
}

# Global dictionary mapping departure locations to airports
location_to_airport = {
    "new york": "JFK",
    "los angeles": "LAX",
    "chicago": "ORD",
    "san francisco": "SFO",
    "miami": "MIA",
    "paris": "CDG",
    "tokyo": "HND",
    "sydney": "SYD",
    "dubai": "DXB",
    "london": "LHR",
}

@app.get("/flight-tickets")
def get_flight_tickets(departure: str, arrival: str, departure_date: str, return_date: str):
    """Fetch flight tickets based on departure and arrival destinations."""
    departure = departure.lower()
    arrival = arrival.lower()
    departure_airline = location_to_airline.get(departure, "Generic Airlines")
    departure_airport = location_to_airport.get(departure, "Unknown Airport")
    arrival_airline = location_to_airline.get(arrival, "Generic Airlines")
    arrival_airport = location_to_airport.get(arrival, "Unknown Airport")
    dummy_tickets = {
        "outbound_flight": FlightTicket(
            flight_number="AI101",
            airline=departure_airline,
            price=150.0,
            departure_time=f"{departure_date} T10:00:00",
            arrival_time=f"{departure_date} T12:00:00",
            departure_airport=departure_airport,
            arrival_airport=arrival_airport,
        ),
        "return_flight": FlightTicket(
            flight_number="AI102",
            airline=arrival_airline,
            price=150.0,
            departure_time=f"{return_date} T10:00:00",
            arrival_time=f"{return_date} T12:00:00",
            departure_airport=arrival_airport,
            arrival_airport=departure_airport,
        ),
    }
    return dummy_tickets

# Global dictionary mapping destination locations to hotels
location_to_hotel = {
    "new york": "The Plaza Hotel",
    "los angeles": "The Beverly Hills Hotel",
    "chicago": "The Langham",
    "san francisco": "Fairmont San Francisco",
    "miami": "Fontainebleau Miami Beach",
    "paris": "Hotel Ritz Paris",
    "tokyo": "Park Hyatt Tokyo",
    "sydney": "Shangri-La Sydney",
    "dubai": "Burj Al Arab",
    "london": "The Savoy",
}

@app.get("/hotel-bookings")
def get_hotel_bookings(destination: str, check_in_date: str, check_out_date: str):
    """Fetch hotel bookings based on destination and duration of stay."""
    destination = destination.lower()
    hotel_name = location_to_hotel.get(destination, "Generic Hotel")

    # Parse the check-in and check-out dates
    check_in = datetime.strptime(check_in_date, "%m/%d/%Y")
    check_out = datetime.strptime(check_out_date, "%m/%d/%Y")

    # Calculate the duration of stay in days
    duration = (check_out - check_in).days

    dummy_booking = {
        "hotel_name": hotel_name,
        "price_per_night": 200.0,
        "total_price": 200.0 * duration,
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
    }
    return dummy_booking

# List of weather maps with important weather details
weather_maps = {
    "new york": {"temperature": "25°C", "condition": "Sunny", "humidity": "60%", "wind_speed": "15 km/h"},
    "los angeles": {"temperature": "30°C", "condition": "Clear", "humidity": "50%", "wind_speed": "10 km/h"},
    "chicago": {"temperature": "20°C", "condition": "Cloudy", "humidity": "70%", "wind_speed": "20 km/h"},
    "san francisco": {"temperature": "18°C", "condition": "Foggy", "humidity": "80%", "wind_speed": "5 km/h"},
    "miami": {"temperature": "28°C", "condition": "Rainy", "humidity": "85%", "wind_speed": "25 km/h"},
    "paris": {"temperature": "22°C", "condition": "Partly Cloudy", "humidity": "65%", "wind_speed": "12 km/h"},
    "tokyo": {"temperature": "27°C", "condition": "Sunny", "humidity": "55%", "wind_speed": "18 km/h"},
    "sydney": {"temperature": "24°C", "condition": "Windy", "humidity": "60%", "wind_speed": "30 km/h"},
    "dubai": {"temperature": "35°C", "condition": "Hot", "humidity": "40%", "wind_speed": "8 km/h"},
    "london": {"temperature": "19°C", "condition": "Drizzle", "humidity": "75%", "wind_speed": "10 km/h"},
}

@app.get("/get-weather")
def get_weather(location: str):
    return weather_maps[location.lower()]

# Global dictionary mapping locations to tourist activities
location_to_activities = {
    "new york": ["Visit Times Square", "Explore Central Park", "See a Broadway Show"],
    "los angeles": ["Walk along Hollywood Boulevard", "Relax at Santa Monica Beach", "Visit Universal Studios"],
    "chicago": ["Admire the Art Institute of Chicago", "Walk along Navy Pier", "Take a river architecture tour"],
    "san francisco": ["Walk across the Golden Gate Bridge", "Visit Alcatraz Island", "Explore Fisherman's Wharf"],
    "miami": ["Relax on South Beach", "Visit the Art Deco District", "Explore the Everglades"],
    "paris": ["Climb the Eiffel Tower", "Visit the Louvre Museum", "Stroll along the Seine River"],
    "tokyo": ["Explore the Meiji Shrine", "Visit the Tokyo Skytree", "Shop in Shibuya"],
    "sydney": ["Climb the Sydney Harbour Bridge", "Visit the Sydney Opera House", "Relax at Bondi Beach"],
    "dubai": ["Visit the Burj Khalifa", "Shop at the Dubai Mall", "Explore the Dubai Desert"],
    "london": ["See the Tower of London", "Ride the London Eye", "Visit the British Museum"],
}

@app.get("/get-activities")
def get_activities(location: str):
    """Fetch tourist activities based on the location."""
    location = location.lower()
    activities = location_to_activities.get(location, ["No activities found for this location."])
    return {"activities": activities}

