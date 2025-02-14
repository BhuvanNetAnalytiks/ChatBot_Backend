from dotenv import load_dotenv 
import os
import requests

# Load environment variables
load_dotenv()  # Add this line to ensure env variables are loaded

# ServiceNow API credentials and URL
SERVICE_NOW_INSTANCE = os.getenv('SERVICE_NOW_INSTANCE')
SERVICE_NOW_USER = os.getenv('SERVICE_NOW_USER')
SERVICE_NOW_PASSWORD = os.getenv('SERVICE_NOW_PASSWORD')

def create_servicenow_incident(description="Some problem", urgency='2', impact='2'):
    # Ensure the URL is properly formatted
    if not SERVICE_NOW_INSTANCE.startswith('https://'):
        url = f'https://{SERVICE_NOW_INSTANCE}/api/now/table/incident'
    else:
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
   
    try:
        response = requests.post(
            url, 
            auth=(SERVICE_NOW_USER, SERVICE_NOW_PASSWORD), 
            headers=headers, 
            json=data,
            timeout=10  # Add timeout
        )

        if response.status_code == 201:
            result = response.json()['result']
            return {
                'number': result['number'],
                'sys_id': result['sys_id']
            }
        else:
            if "Instance Hibernating" in response.text:
                return {
                    'error': 'ServiceNow instance is hibernating. Please log in to your instance to wake it up: ' +
                            'https://developer.servicenow.com/dev.do#!/home?wu=true'
                }
            try:
                error_detail = response.json()
                return {'error': f"Status code: {response.status_code}, Details: {error_detail}"}
            except:
                return {'error': f"Status code: {response.status_code}, Response: {response.text}"}
    except requests.exceptions.RequestException as e:
        return {'error': f"Connection error: {str(e)}"}