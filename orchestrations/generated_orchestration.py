from flask import Flask, jsonify, request
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

app = Flask(__name__)

from main_library.function1 import function

@app.route('/run_function1', methods=['POST'])
def function_api():
    # Call the function without parameters
    result = function()
    return jsonify({'result': result})

from main_library.function2 import function2

@app.route('/run_function2', methods=['GET'])
def function2_api():
    # Call the function without parameters
    result = function2()
    return jsonify({'result': result})

from main_library.create_servicenow_incidenet import create_servicenow_incident

@app.route('/create_servicenow_incident', methods=['POST'])
def create_servicenow_incident_api():
    if request.is_json:
        params = request.get_json()
    else:
        params = request.form.to_dict()

    description = params.get('description', 'default_value')
    urgency = params.get('urgency', 'default_value')
    impact = params.get('impact', 'default_value')

    result = create_servicenow_incident(description, urgency, impact)
    return jsonify({'result': result})

from main_library.create_zendesk_incident import create_zendesk_ticket

@app.route('/create_zendesk_incident', methods=['POST'])
def create_zendesk_ticket_api():
    if request.is_json:
        params = request.get_json()
    else:
        params = request.form.to_dict()

    subject = params.get('subject', 'default_value')
    description = params.get('description', 'default_value')
    priority = params.get('priority', 'default_value')

    result = create_zendesk_ticket(subject, description, priority)
    return jsonify({'result': result})

from main_library.create_jira_incident import create_jira_ticket

@app.route('/create_jira_incident', methods=['POST'])
def create_jira_ticket_api():
    if request.is_json:
        params = request.get_json()
    else:
        params = request.form.to_dict()

    project_key = params.get('project_key', 'default_value')
    summary = params.get('summary', 'default_value')
    description = params.get('description', 'default_value')
    issuetype = params.get('issuetype', 'default_value')

    result = create_jira_ticket(project_key, summary, description, issuetype)
    return jsonify({'result': result})

from main_library.llm_claude import query_claude_llm

@app.route('/llm_claude', methods=['POST'])
def query_claude_llm_api():
    if request.is_json:
        params = request.get_json()
    else:
        params = request.form.to_dict()

    question = params.get('question', 'default_value')
    context = params.get('context', 'default_value')

    result = query_claude_llm(question, context)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
