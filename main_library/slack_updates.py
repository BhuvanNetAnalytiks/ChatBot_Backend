import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def post_to_slack(channel: str, message: str):
    """
    Posts a message to a Slack channel.

    :param channel: The Slack channel to post in (e.g., "#general").
    :param message: The message text to send.
    :return: The response from Slack API.
    """
    slack_token = os.getenv("SLACK_BOT_TOKEN")  # Get token from .env
    if not slack_token:
        raise ValueError("Slack token is missing. Please check your .env file.")

    url = "https://slack.com/api/chat.postMessage"

    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json"
    }

    data = {
        "channel": channel,
        "text": message
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()  # Return response as JSON for debugging
