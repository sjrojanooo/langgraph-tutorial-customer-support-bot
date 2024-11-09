import sys
sys.path.append(".")
from dotenv import load_dotenv
load_dotenv()

from langchain_community.tools.tavily_search import TavilySearchResults

from tools.policies import lookup_policy
from tools.flights import (
    fetch_user_flight_information, 
    search_flights,
    update_ticket_to_new_flight, 
    cancel_ticket
)
from tools.car_rentals import (
    search_car_rentals,
    book_car_rental,
    update_car_rental,
    cancel_car_rental
)

from tools.hotels import (
    search_hotels,
    book_hotel,
    update_hotel,
    cancel_hotel
)

from tools.excursions import (
    search_trip_recommendations,
    book_excursion,
    update_excursion,
    cancel_excursion
)

# read only tools and will not require user approval
SAFE_TOOL_LIST = [
    TavilySearchResults(max_results=1),
    fetch_user_flight_information, 
    search_flights,
    lookup_policy,
    search_car_rentals, 
    search_hotels, 
    search_trip_recommendations
]

# Sesnsitive tools require the users approval 
# making any updates to their trip
SENSITIVE_TOOL_LIST = [
    update_ticket_to_new_flight,
    cancel_ticket,
    book_car_rental,
    update_car_rental,
    cancel_car_rental,
    book_hotel,
    update_hotel,
    cancel_hotel,
    book_excursion,
    update_excursion,
    cancel_excursion
]

# Complete list of tools
COMPLETE_TOOL_LIST = SAFE_TOOL_LIST + SENSITIVE_TOOL_LIST

# Sensitive Tool Names
SENSITIVE_TOOL_NAMES = {t.name for t in SENSITIVE_TOOL_LIST}