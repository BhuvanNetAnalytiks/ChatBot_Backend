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
        methods = step.get("methods", ["GET"])  # Default to GET if not specified
        parameters = step.get("parameters", [])

        # Avoid duplicate imports
        if func_name not in imported_functions:
            file_content += f"from {module_path} import {func_name}\n"
            imported_functions.add(func_name)

        # Add route for the function
        file_content += f"\n@app.route('{endpoint}', methods={methods})\n"
        file_content += f"def {func_name}_api():\n"
        
        if parameters:
            file_content += f"    if request.is_json:\n"
            file_content += f"        params = request.get_json()\n"
            file_content += f"    else:\n"
            file_content += f"        params = request.form.to_dict()\n\n"
            
            # Extract parameters with default values if not provided
            param_extraction = "\n".join(
                [f"    {param} = params.get('{param}', 'default_value')" for param in parameters]
            )
            file_content += param_extraction + "\n\n"
            
            # Call the function with extracted parameters
            param_list = ", ".join(parameters)
            file_content += f"    result = {func_name}({param_list})\n"
        else:
            file_content += f"    # Call the function without parameters\n"
            file_content += f"    result = {func_name}()\n"
        
        file_content += "    return jsonify({'result': result})\n\n"

    # Final Flask app run
    file_content += "if __name__ == '__main__':\n"
    file_content += "    app.run(debug=True)\n"

    # Ensure the directory exists
    os.makedirs("orchestrations", exist_ok=True)

    # Save the generated Python file
    file_path = "orchestrations/generated_orchestration.py"
    with open(file_path, "w") as f:
        f.write(file_content)

    return f"Orchestration file created successfully at {file_path}."