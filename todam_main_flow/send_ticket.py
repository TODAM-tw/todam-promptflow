import os
import json
import requests

from pathlib import Path
from dotenv import load_dotenv
from promptflow.tools.aoai import tool

ENV_PATH = Path(__file__).parent / "env.local"
print(ENV_PATH)
load_dotenv(dotenv_path=ENV_PATH, override=True)
# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need

API_ENDPOINT = os.environ.get("API_ENDPOINT")


@tool
def send_ticket(answer: str) -> str:
    data = json.loads(answer)
    api_url = API_ENDPOINT
    response = requests.post(api_url, json=data)

    if response.status_code == 200 or response.status_code == 201:
        print("Ticket created successfully!")
        return response.status_code
    else:
        print(f"Ticket creation failed (status {response.status_code}).")
        return response.status_code
