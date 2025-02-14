from dotenv import load_dotenv 
import os
import requests

# Load environment variables
load_dotenv()  

# ServiceNow API credentials and URL
SERVICE_NOW_INSTANCE = os.getenv('SERVICE_NOW_INSTANCE')
SERVICE_NOW_USER = os.getenv('SERVICE_NOW_USER')
SERVICE_NOW_PASSWORD = os.getenv('SERVICE_NOW_PASSWORD')

def get_servicenow_incident(incident_id):
    url = f'{SERVICE_NOW_INSTANCE}/api/now/table/incident?sysparm_query=number={incident_id}&sysparm_limit=1'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
 
    try:
        response = requests.get(url, auth=(SERVICE_NOW_USER, SERVICE_NOW_PASSWORD), headers=headers)
 
        if response.status_code == 200:
            result = response.json()['result']
            state = result.get('state', '')
            state_description = result.get('state_name', 'Unknown Status')
 
            status_map = {
                '1': 'New',
                '2': 'In Progress',
                '3': 'On Hold',
                '6': 'Resolved',
                '7': 'Closed',
                '8': 'Cancelled'
            }
 
            state_description = status_map.get(state, state_description)
 
            number = result.get('number', 'N/A')
            short_description = result.get('short_description', 'No description available')
 
            return {
                'state': state_description,
                'state_code': state,
                'number': number,
                'short_description': short_description
            }
        else:
            return {'error': f'HTTP Error {response.status_code}'}
 
    except Exception as e:
        return {'error': str(e)}
