import sys
from dotenv import load_dotenv
import shutil
import uuid

from langchain_core.messages import ToolMessage, HumanMessage

sys.path.append(".")
load_dotenv()
from graphs.assistant_graph import build_assistant_graph
from tools import utilities
from database.db_utils import update_dates


db_file = update_dates()
print(f'Updated DB is {db_file}')
compiled_graph = build_assistant_graph()
utilities.write_graph_to_pdf(compiled_graph, "part3_conditional_interrupt")

config = {
    "configurable": {
        # The passenger_id is used in our flight tools to
        # fetch the user's flight information
        "passenger_id": "3442 587242",
        # Checkpoints are accessed by thread_id
        "thread_id": str(uuid.uuid4()),
    }
}

# Let's create an example conversation a user might have with the assistant
tutorial_questions = [
    "Hi there, what time is my flight?",
    "Am i allowed to update my flight to something sooner? I want to leave later today.",
    "Update my flight to sometime next week then",
    "The next available option is great",
    "what about lodging and transportation?",
    "Yeah i think i'd like an affordable hotel for my week-long stay (7 days). And I'll want to rent a car.",
    "OK could you place a reservation for your recommended hotel? It sounds nice.",
    "yes go ahead and book anything that's moderate expense and has availability.",
    "Now for a car, what are my options?",
    "Awesome let's just get the cheapest option. Go ahead and book for 7 days",
    "Cool so now what recommendations do you have on excursions?",
    "Are they available while I'm there?",
    "interesting - i like the museums, what options are there? ",
    "OK great pick one and book it for my second day there.",
]

_printed = set()
# We can reuse the tutorial questions from part 1 to see how it does.
for question in tutorial_questions:
    events = compiled_graph.stream(
        input={"messages": [HumanMessage(content=question)]}, config=config, stream_mode="values"
    )
    for event in events:
        utilities._print_event(event, _printed)
    snapshot = compiled_graph.get_state(config)
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
            result = compiled_graph.invoke(
                None,
                config,
            )   
        else:
            # Satisfy the tool invocation by
            # providing instructions on the requested changes / change of mind
            result = compiled_graph.invoke(
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
        snapshot = compiled_graph.get_state(config)
        message = snapshot.values['messages'][-1]
        message = message.pretty_repr(html=True)
        print(f"""{message}\n""")