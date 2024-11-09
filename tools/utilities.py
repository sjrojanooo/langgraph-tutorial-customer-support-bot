from langgraph.graph import END
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableLambda
from langgraph.prebuilt import ToolNode, tools_condition

from state.state import AgentState
from tools.constants import SENSITIVE_TOOL_NAMES

def handle_tool_error(state) -> dict:
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }


def create_tool_node_with_fallback(tools: list) -> dict:
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )


def _print_event(event: dict, _printed: set, max_length=1500):
    current_state = event.get("dialog_state")
    if current_state:
        print("Currently in: ", current_state[-1])
    message = event.get("messages")
    if message:
        if isinstance(message, list):
            message = message[-1]
        if message.id not in _printed:
            msg_repr = message.pretty_repr(html=True)
            if len(msg_repr) > max_length:
                msg_repr = msg_repr[:max_length] + " ... (truncated)"
            print(msg_repr)
            _printed.add(message.id)
            
            
def write_graph_to_pdf(graph: object, filename: str) -> None:
    with open(f"graph_pngs/{filename}.png", "wb") as f: 
        f.write(graph.get_graph().draw_mermaid_png())
        
        
def route_tools_condition(state: AgentState) -> str: 
    # tools condition returns either a value error when no message exists, 
    # "tools", or "__end__" as the next node 
    # https://langchain-ai.github.io/langgraph/reference/prebuilt/#langgraph.prebuilt.tool_node.tools_condition
    next_node = tools_condition(state)
    # If no nodes are invoked return to the user
    if next_node == END: 
        return END
    ai_message = state["messages"][-1]
    # This assumes single tool calls. To handle parallel tool calling, you'd want to
    # use an ANY condition
    first_tool_call = ai_message.tool_calls[0]
    if first_tool_call["name"] in SENSITIVE_TOOL_NAMES: 
        return "sensitive_tools"
    return "safe_tools"