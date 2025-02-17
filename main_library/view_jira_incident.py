import requests
import json
from requests.auth import HTTPBasicAuth
import os

# Load Jira credentials from environment variables
jira_url = os.getenv('JIRA_INSTANCE_URL')
api_token = os.getenv('JIRA_API_TOKEN')
email = os.getenv('JIRA_EMAIL')

def view_jira_ticket_status(ticket_id):
    if not ticket_id:
        return {'error': 'Please provide a valid ticket ID'}

    url = f"{jira_url}/rest/api/3/issue/{ticket_id}"
    headers = {"Accept": "application/json"}

    response = requests.get(
        url,
        headers=headers,
        auth=HTTPBasicAuth(email, api_token)
    )

    if response.status_code == 200:
        issue_data = response.json()
        
        return {
            "ticket_id": ticket_id,
            "summary": issue_data['fields']['summary'],
            "status": issue_data['fields']['status']['name'],
            "priority": issue_data['fields'].get('priority', {}).get('name', 'Not specified'),
            "assignee": issue_data['fields']['assignee']['displayName'] if issue_data['fields'].get('assignee') else "Unassigned",
            "reporter": issue_data['fields']['reporter']['displayName'],
            "created": issue_data['fields']['created'],
            "updated": issue_data['fields']['updated']
        }
    else:
        return {"error": response.status_code, "message": response.text}
