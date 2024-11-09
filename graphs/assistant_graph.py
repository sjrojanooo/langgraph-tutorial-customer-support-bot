from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, START

from state.state import AgentState, ConfigSchema
from agents.agents import (
    assistant_agent, 
    fetch_user_flight_information_agent
    )
from tools.utilities import (
    create_tool_node_with_fallback, 
    route_tools_condition
)
from tools.constants import SAFE_TOOL_LIST, SENSITIVE_TOOL_LIST

def build_assistant_graph(): 
    builder = StateGraph(AgentState, config_schema=ConfigSchema)
    
    # Define nodes: these do the work
    builder.add_node("fetch_user_info", fetch_user_flight_information_agent)
    builder.add_node("assistant", assistant_agent)
    builder.add_node("safe_tools", create_tool_node_with_fallback(SAFE_TOOL_LIST))
    builder.add_node("sensitive_tools", create_tool_node_with_fallback(SENSITIVE_TOOL_LIST))
    
    # Define edges: these determine how the control flow moves
    builder.add_edge(START, "fetch_user_info")
    builder.add_edge("fetch_user_info", "assistant")
    builder.add_conditional_edges(
        "assistant",
        route_tools_condition, ["safe_tools", "sensitive_tools", END]
    )
    builder.add_edge("safe_tools", "assistant")
    builder.add_edge("sensitive_tools", "assistant")

    # The checkpointer lets the graph persist its state
    # this is a complete memory for the entire graph.
    memory = MemorySaver()
    graph = builder.compile(
        checkpointer=memory, 
        interrupt_before=["sensitive_tools"]
        )
    return graph