import json
import os

def create_orchestration(orchestration_json):
    """Generates a dynamic Flask API based on orchestration JSON without executing it."""
    
    steps = orchestration_json.get("steps", [])

    # Base Flask app setup
    file_content = (
        "from flask import Flask, jsonify, request, redirect\n"
        "from flask_cors import CORS\n"
        "import json\n"
        "import os\n"
        "from pathlib import Path\n"
        "import sys\n\n"
        "sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), \"..\")))\n"
        "json_file_path = Path(__file__).resolve().parents[1] / \"orchestration.json\"\n\n"
        "app = Flask(__name__)\n\n"
        "CORS(app)\n\n"
        "try:\n"
        "    with open(json_file_path, 'r') as json_file:\n"
        "       orchestration_data = json.load(json_file)\n"
        "       print(orchestration_data)  # You can now use this data in your code\n"
        "except FileNotFoundError:\n"
        "   print(f\"Error: {json_file_path} not found.\")\n\n"
        "@app.route('/get_orchestration', methods=['GET'])\n"
        "def get_orchestration():\n"
        "   try:\n"
        "        with open(json_file_path, 'r') as json_file:\n"
        "           orchestration_data = json.load(json_file)\n"
        "           return jsonify(orchestration_data)\n"
        "   except FileNotFoundError:\n"
        "        return jsonify({\"error\": \"Orchestration file not found\"}), 404\n"
        "   except Exception as e:\n"
        "        return jsonify({\"error\": str(e)}), 500\n\n"
        "@app.route('/log_message', methods=['POST'])\n"
        "def log_message():\n"
        "   try:\n"
        "       data = request.get_json()\n"
        "       message = data.get('message')\n"
        "       sender = data.get('sender')\n\n"
        "       print(f\"Received message from {sender}: {message}\")\n"
        "       return jsonify({\n"
        "           \"status\": \"success\",\n"
        "           \"message\": \"Message logged successfully\"\n"
        "       }), 200\n"
        "   except Exception as e:\n"
        "       return jsonify({\n"
        "           \"status\": \"error\",\n"
        "           \"error\": str(e)\n"
        "         }), 500\n\n"
    )

    # Track imported functions
    imported_functions = set()

    for step in steps:
        func_name = step["function"]
        module_path = step["module"]
        endpoint = step["endpoint"]
        methods = step.get("methods", ["GET"])
        parameters = step.get("parameters", [])
        response_type = step.get("response_type", "json")  # Default to JSON response

        # Avoid duplicate imports
        if func_name not in imported_functions:
            file_content += f"from {module_path} import {func_name}\n"
            imported_functions.add(func_name)

        # Add route for the function
        file_content += f"\n@app.route('{endpoint}', methods={methods})\n"
        file_content += f"def {func_name}_api():\n"
        
        if parameters:
            # Separate query and body parameters
            query_params = [p["name"] for p in parameters if p["type"] == "query"]
            body_params = [p["name"] for p in parameters if p["type"] == "body"]
            
            # Get body parameters if any
            if body_params:
                file_content += "    # Get body parameters\n"
                file_content += "    if request.is_json:\n"
                file_content += "        body_params = request.get_json()\n"
                file_content += "    else:\n"
                file_content += "        body_params = request.form.to_dict()\n\n"
            
            # Extract parameters based on their type
            param_extraction = []
            for param in parameters:
                if param["type"] == "query":
                    param_extraction.append(
                        f"    {param['name']} = request.args.get('{param['name']}')"
                    )
                else:
                    param_extraction.append(
                        f"    {param['name']} = body_params.get('{param['name']}')"
                    )
            
            file_content += "\n".join(param_extraction) + "\n\n"
            
            # Call the function with extracted parameters
            param_list = ", ".join(p["name"] for p in parameters)
            file_content += f"    result = {func_name}({param_list})\n"
        else:
            file_content += f"    result = {func_name}()\n"
        
        # Handle different response types
        if response_type == "redirect":
            file_content += "    return result  # Return redirect response directly\n"
        else:
            file_content += "    return jsonify({'result': result})\n\n"

    # Final Flask app run
    file_content += "if __name__ == '__main__':\n"
    file_content += "    app.run(debug=True)\n"

    # Save the generated Python file
    os.makedirs("orchestrations", exist_ok=True)
    file_path = "orchestrations/generated_orchestration.py"
    with open(file_path, "w") as f:
        f.write(file_content)

    return f"Orchestration file created successfully at {file_path}."