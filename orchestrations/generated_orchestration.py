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

if __name__ == '__main__':
    app.run(debug=True)
