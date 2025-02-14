from dotenv import load_dotenv 
import os
import requests

# Load environment variables
load_dotenv()  

# ServiceNow API credentials and URL
SERVICE_NOW_INSTANCE = os.getenv('SERVICE_NOW_INSTANCE')
SERVICE_NOW_USER = os.getenv('SERVICE_NOW_USER')
SERVICE_NOW_PASSWORD = os.getenv('SERVICE_NOW_PASSWORD')

def view_ticket_detailed(number=None, sys_id=None):
    """
    View detailed ServiceNow ticket information
    Args:
        number: The incident number (e.g., 'INC0010002')
        sys_id: The system ID
    Returns:
        Dictionary containing detailed ticket information or error message
    """
    # Ensure the URL is properly formatted
    base_url = f'https://{SERVICE_NOW_INSTANCE}' if not SERVICE_NOW_INSTANCE.startswith('https://') else SERVICE_NOW_INSTANCE
    url = f'{base_url}/api/now/table/incident'

    # Set up parameters with comprehensive fields
    params = {
        'sysparm_display_value': 'true',
        'sysparm_fields': ','.join([
            'number',
            'sys_id',
            'state',
            'short_description',
            'description',
            'priority',
            'urgency',
            'impact',
            'assigned_to',
            'assignment_group',
            'caller_id',
            'category',
            'subcategory',
            'opened_at',
            'sys_updated_on',
            'comments',
            'work_notes'
        ])
    }

    # Add query parameters based on input
    if number:
        params['sysparm_query'] = f'number={number}'
    elif sys_id:
        url = f'{url}/{sys_id}'
    else:
        return {'error': 'Please provide either number or sys_id'}

    headers = {
        'Accept': 'application/json'
    }

    try:
        response = requests.get(
            url,
            auth=(SERVICE_NOW_USER, SERVICE_NOW_PASSWORD),
            headers=headers,
            params=params,
            timeout=10
        )

        if response.status_code == 200:
            response_data = response.json()
            
            if 'result' in response_data:
                result = response_data['result']
                
                if isinstance(result, list):
                    if not result:
                        return {'error': 'No ticket found'}
                    ticket = result[0]
                else:
                    ticket = result

                return {
                    'number': ticket.get('number'),
                    'sys_id': ticket.get('sys_id'),
                    'state': ticket.get('state'),
                    'short_description': ticket.get('short_description'),
                    'description': ticket.get('description'),
                    'priority': ticket.get('priority'),
                    'urgency': ticket.get('urgency'),
                    'impact': ticket.get('impact'),
                    'assigned_to': ticket.get('assigned_to'),
                    'assignment_group': ticket.get('assignment_group'),
                    'caller': ticket.get('caller_id'),
                    'category': ticket.get('category'),
                    'subcategory': ticket.get('subcategory'),
                    'opened_at': ticket.get('opened_at'),
                    'last_updated': ticket.get('sys_updated_on'),
                    'comments': ticket.get('comments'),
                    'work_notes': ticket.get('work_notes')
                }
            else:
                return {'error': 'Unexpected response format'}

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