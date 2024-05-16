import os
import json
from pathlib import Path
from dotenv import load_dotenv
from promptflow import tool
from anthropic import AnthropicBedrock

ENV_PATH = Path(__file__).parent / "env.local"
print(ENV_PATH)
load_dotenv(dotenv_path=ENV_PATH, override=True)

AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
AWS_SESSION_TOKEN = os.environ.get("AWS_SESSION_TOKEN")
AWS_REGION = "us-east-1"

@tool
def claude_sonnet(line_log: str) -> str:
    client = AnthropicBedrock(
        aws_access_key=AWS_ACCESS_KEY,
        aws_secret_key=AWS_SECRET_KEY,
        aws_session_token=AWS_SESSION_TOKEN,
        aws_region=AWS_REGION,
    )
    message = client.messages.create(
        model="anthropic.claude-3-sonnet-20240229-v1:0",
        max_tokens=256,
        messages=[{"role": "user", "content": line_log}]
    )

    if hasattr(message.content, 'chunks'):

        content_list = [chunk.text for chunk in message.content.chunks]
    else:
        content_list = [str(message.content)]

    json_str = json.dumps(content_list)
    return json_str