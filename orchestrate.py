import json

def create_orchestration(orchestration_json):
    # Load orchestration steps
    steps = orchestration_json.get("steps", [])
    
    # Generate new Python file content
    file_content = "from flask import Flask, jsonify\n"
    file_content += "from main_library import *\n\n"
    file_content += "app = Flask(__name__)\n\n"
    
    for step in steps:
        func_name = step["function"]
        endpoint = step["endpoint"]
        methods = step.get("methods", ["GET"])
        
        # Add route for the function
        file_content += f"@app.route('{endpoint}', methods={methods})\n"
        file_content += f"def {func_name}_api():\n"
        file_content += f"    result = {func_name}()\n"
        file_content += "    return jsonify({'result': result})\n\n"
    
    file_content += "if __name__ == '__main__':\n"
    file_content += "    app.run(debug=True)\n"
    
    # Save the new Python file
    with open("orchestrations/generated_orchestration.py", "w") as f:
        f.write(file_content)
    
    return "Orchestration file created successfully."