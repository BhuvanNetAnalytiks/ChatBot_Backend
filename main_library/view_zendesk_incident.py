import requests
from dotenv import load_dotenv
import os
import base64

# Load environment variables
load_dotenv()

# Zendesk credentials
ZENDESK_EMAIL = os.getenv('ZENDESK_EMAIL')
ZENDESK_TOKEN = os.getenv('ZENDESK_API_KEY')
ZENDESK_INSTANCE_URL = os.getenv('ZENDESK_INSTANCE_URL')

def view_zendesk_ticket_detailed(ticket_id=None):
    """
    View detailed Zendesk ticket information including comments
    Args:
        ticket_id: The ticket ID number
    Returns:
        Dictionary containing detailed ticket information or error message
    """
    if not ticket_id:
        return {'error': 'Please provide a ticket ID'}

    # First get the basic ticket information
    ticket_url = f"{ZENDESK_INSTANCE_URL}/api/v2/tickets/{ticket_id}"
    
    auth = base64.b64encode(f"{ZENDESK_EMAIL}/token:{ZENDESK_TOKEN}".encode()).decode()
    
    headers = {
        'Authorization': f'Basic {auth}',
        'Content-Type': 'application/json'
    }

    try:
        # Get basic ticket info
        ticket_response = requests.get(
            ticket_url,
            headers=headers,
            timeout=10
        )

        if ticket_response.status_code != 200:
            return {'error': f"Failed to get ticket. Status code: {ticket_response.status_code}"}

        ticket_info = ticket_response.json().get('ticket', {})
        
        # Now get the comments
        comments_url = f"{ZENDESK_INSTANCE_URL}/api/v2/tickets/{ticket_id}/comments"
        
        comments_response = requests.get(
            comments_url,
            headers=headers,
            timeout=10
        )

        if comments_response.status_code == 200:
            comments = comments_response.json().get('comments', [])
            
            # Create the full response
            return {
                'ticket': {
                    'id': ticket_info.get('id'),
                    'status': ticket_info.get('status'),
                    'priority': ticket_info.get('priority'),
                    'subject': ticket_info.get('subject'),
                    'description': ticket_info.get('description'),
                    'requester_id': ticket_info.get('requester_id'),
                    'assignee_id': ticket_info.get('assignee_id'),
                    'created_at': ticket_info.get('created_at'),
                    'updated_at': ticket_info.get('updated_at'),
                    'tags': ticket_info.get('tags', [])
                },
                'comments': [{
                    'id': comment.get('id'),
                    'author_id': comment.get('author_id'),
                    'body': comment.get('body'),
                    'created_at': comment.get('created_at'),
                    'public': comment.get('public')
                } for comment in comments]
            }
        else:
            try:
                error_detail = comments_response.json()
                return {'error': f"Status code: {comments_response.status_code}, Details: {error_detail}"}
            except:
                return {'error': f"Status code: {comments_response.status_code}, Response: {comments_response.text}"}

    except requests.exceptions.RequestException as e:
        return {'error': f"Connection error: {str(e)}"}
