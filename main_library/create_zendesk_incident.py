import requests
import json 
from dotenv import load_dotenv
import os
from requests.auth import HTTPBasicAuth

instance_url = os.getenv('ZENDESK_INSTANCE_URL')
admin_email = os.getenv('ZENDESK_EMAIL')
api_token = os.getenv('ZENDESK_API_KEY')


def create_zendesk_ticket(subject, description, priority='normal'):
    url = f"{instance_url}/api/v2/tickets.json"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "ticket": {
            "subject": subject,
            "description": description,
            "priority": priority
        }
    }

    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(data),
        auth=HTTPBasicAuth(f"{admin_email}/token", api_token)
    )

    if response.status_code == 201:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}
