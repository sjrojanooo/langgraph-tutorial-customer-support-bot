from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import MessagesState
from langgraph.graph.message import AnyMessage, add_messages

class ConfigSchema(TypedDict): 
    passenger_id: str
    thread_id: str

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    user_info: str