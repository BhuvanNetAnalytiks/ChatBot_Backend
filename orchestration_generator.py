import json
import os

def create_orchestration(orchestration_json):
    """Generates a dynamic Flask API based on orchestration JSON without executing it."""
    
    steps = orchestration_json.get("steps", [])

    # Base Flask app setup
    file_content = (
        "from flask import Flask, jsonify, request\n"
        "import os\n"
        "import sys\n\n"
        "sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), \"..\")))\n\n"
        "app = Flask(__name__)\n\n"
    )

    # Track imported functions
    imported_functions = set()

    for step in steps:
        func_name = step["function"]
        module_path = step["module"]
        endpoint = step["endpoint"]
        methods = step.get("methods", ["GET"])
        parameters = step.get("parameters", [])

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