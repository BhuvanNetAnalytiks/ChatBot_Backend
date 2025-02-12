from dotenv import load_dotenv 
import os
import requests

# ServiceNow API credentials and URL
SERVICE_NOW_INSTANCE = os.getenv('SERVICE_NOW_INSTANCE')
SERVICE_NOW_USER = os.getenv('SERVICE_NOW_USER')
SERVICE_NOW_PASSWORD = os.getenv('SERVICE_NOW_PASSWORD')

def create_servicenow_incident(description, urgency='2', impact='2'):
   
    url = f'{SERVICE_NOW_INSTANCE}/api/now/table/incident'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
   
    data = {
        'short_description': description,
        'urgency': urgency,
        'impact': impact,
    }
   
    response = requests.post(url, auth=(SERVICE_NOW_USER, SERVICE_NOW_PASSWORD), headers=headers, json=data)

    if response.status_code == 201:
        result = response.json()['result']
        return {
            'number': result['number'],
            'sys_id': result['sys_id']
        }
    else:
        return {'error': response.status_code}
