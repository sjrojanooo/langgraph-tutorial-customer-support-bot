import sys
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
from langsmith import Client

client = Client()
list_runs = client.list_runs(project_id=os.environ['LANGSMITH_PROJECT_UUID'])
filtered_runs = [run for run in list_runs if run.start_time >= datetime(2024,11,9)][0]

with open('./artifacts/conversations/langsmith_conversation_part3.txt', 'w') as f: 
    f.write("--------------------CUSTOMER SERVICE CHATBOT--------------------\n")
    for message in filtered_runs.inputs['messages']:
        if 'type' in message.keys(): 
            if message['type'] == 'human': 
                f.write(f"{message['type'].upper()}: {message['content']}\n")
            elif message['type'] == 'ai':
                if isinstance(message['content'], list): 
                    f.write(f"{message['type'].upper()}: {message['content'][0]}\n") 
                else: 
                    f.write(f"{message['type'].upper()}: {message['content']}\n")
    f.close()