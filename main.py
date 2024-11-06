import sys
sys.path.append(".")
from dotenv import load_dotenv
load_dotenv()
import shutil
import uuid

from langchain_core.messages import ToolMessage, HumanMessage

from graphs.assistant_graph import build_assistant_graph
from tools import utilities, constants
from database.db_utils import update_dates


db_file = update_dates()
print(f'Updated DB is {db_file}')
part_2_graph = build_assistant_graph()
utilities.write_graph_to_pdf(part_2_graph, "part2_interrupt_graph")


config = {
    "configurable": {
        # The passenger_id is used in our flight tools to
        # fetch the user's flight information
        "passenger_id": "3442 587242",
        # Checkpoints are accessed by thread_id
        "thread_id": str(uuid.uuid4()),
    }
}
_printed = set()
# We can reuse the tutorial questions from part 1 to see how it does.
for question in constants.tutorial_questions:
    events = part_2_graph.stream(
        input={"messages": [HumanMessage(content=question)]}, config=config, stream_mode="values"
    )
    for event in events:
        utilities._print_event(event, _printed)
    snapshot = part_2_graph.get_state(config)
    while snapshot.next:
        # We have an interrupt! The agent is trying to use a tool, and the user can approve or deny it
        # Note: This code is all outside of your graph. Typically, you would stream the output to a UI.
        # Then, you would have the frontend trigger a new run via an API call when the user has provided input.
        try:
            user_input = input(
                "Do you approve of the above actions? Type 'y' to continue;"
                " otherwise, explain your requested changed.\n\n"
            )
        except:
            user_input = "y"
        if user_input.strip() == "y":
            # Just continue
            # CONTINUE FLOW HERE IF APPROVED BY USER 
            # Known as a breakpoint in the graph
            # https://langchain-ai.github.io/langgraph/concepts/low_level/#recursion-limit:~:text=recursion%20limit%20works.-,Breakpoints,-%C2%B6
            # look at NodeInterrupt for dynamic interruption
            # Note from this trace that you typically resume a flow by invoking the graph with (None, config). 
            # The state is loaded from the checkpoint as if it never was interrupted.
            result = part_2_graph.invoke(
                None,
                config,
            )   
        else:
            # Satisfy the tool invocation by
            # providing instructions on the requested changes / change of mind
            result = part_2_graph.invoke(
                {
                    "messages": [
                        ToolMessage(
                            tool_call_id=event["messages"][-1].tool_calls[0]["id"],
                            content=f"API call denied by user. Reasoning: '{user_input}'. Continue assisting, accounting for the user's input.",
                        )
                    ]
                },
                config,
            )
        # get the latest graph state and pretty pring the message
        snapshot = part_2_graph.get_state(config)
        message = snapshot.values['messages'][-1]
        message = message.pretty_repr(html=True)
        print(f"""{message}\n""")