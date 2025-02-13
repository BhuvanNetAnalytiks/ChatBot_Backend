import requests
import json
from requests.auth import HTTPBasicAuth
import os
 
 
jira_url = os.getenv('JIRA_INSTANCE_URL')
api_token = os.getenv('JIRA_API_TOKEN')
email = os.getenv('JIRA_EMAIL')
 
def create_jira_ticket(project_key="TEST", summary="my mouse isnt working", description_text="pc is not turning on", issue_type="Task"):
    url = f"{jira_url}/rest/api/3/issue"
    headers = {
        "Content-Type": "application/json"
    }
    
    # Use Atlassian Document Format for the description
    description = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "text": description_text,
                        "type": "text"
                    }
                ]
            }
        ]
    }
    
    data = {
        "fields": {
            "project": {
                "key": project_key
            },
            "summary": summary,
            "description": description,
            "issuetype": {
                "name": issue_type
            }
        }
    }
 
    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(data),
        auth=HTTPBasicAuth(email, api_token)
    )
 
    if response.status_code == 201:
        return response.json()
    else:
        return {"error": response.status_code, "message": response.text}
  
 
