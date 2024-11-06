from datetime import datetime
from typing import Annotated

from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable, RunnableConfig
from typing_extensions import TypedDict
from langgraph.graph.message import AnyMessage, add_messages
from langchain_community.tools.tavily_search import TavilySearchResults

from state.state import AgentState
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


TOOL_LIST = [
    TavilySearchResults(max_results=1),
    fetch_user_flight_information,
    search_flights,
    lookup_policy,
    update_ticket_to_new_flight,
    cancel_ticket,
    search_car_rentals,
    book_car_rental,
    update_car_rental,
    cancel_car_rental,
    search_hotels,
    book_hotel,
    update_hotel,
    cancel_hotel,
    search_trip_recommendations,
    book_excursion,
    update_excursion,
    cancel_excursion
]
    
def assistant_agent(state: AgentState, config: RunnableConfig) -> AgentState: 
    llm = ChatAnthropic(model="claude-3-sonnet-20240229", temperature=1)
    assistant_agent_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a helpful customer support assistant for Swiss Airlines.
                 Use the provided tools to search for flights, company policies, and other information to assist the user's queries. 
                 When searching, be persistent. Expand your query bounds if the first search returns no results. 
                 If a search comes up empty, expand your search before giving up.
                \n\nCurrent user:\n<User>\n{user_info}\n</User>
                \nCurrent time: {time}."""
            ),
            MessagesPlaceholder(variable_name="messages")
        ]
    ).partial(time=datetime.now())
    chain = assistant_agent_prompt | llm.bind_tools(TOOL_LIST)
    
    while True: 
        result = chain.invoke(state)

        # If the LLM happens to return an empty response, we will re-prompt it
        # for an actual response.
        if not result.tool_calls and (
            not result.content
            or isinstance(result.content, list)
            and not result.content[0].get("text")
        ):
            # add default message and have tell agent to response with real output
            messages = state["messages"] + [("user", "Respond with a real output.")]
            # append the message to the state
            state = {**state, "messages": messages}
        else:
            break
        
    return {"messages": result}
        
    
def fetch_user_flight_information_agent(state: AgentState) -> AgentState:
    return {"user_info": fetch_user_flight_information.invoke({})}