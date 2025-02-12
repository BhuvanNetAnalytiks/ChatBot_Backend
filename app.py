from flask import Flask, request, jsonify
import importlib.util
import sys
import os

app = Flask(__name__)

@app.route('/api/save_orchestration', methods=['POST'])
def save_orchestration():
    orchestration_json = request.json
    result = create_orchestration(orchestration_json)
    
    # Load the generated orchestration file
    spec = importlib.util.spec_from_file_location(
        "generated_orchestration",
        os.path.join("orchestrations", "generated_orchestration.py")
    )
    generated_module = importlib.util.module_from_spec(spec)
    sys.modules["generated_orchestration"] = generated_module
    spec.loader.exec_module(generated_module)
    
    # Register the routes from the generated module
    for rule in generated_module.app.url_map.iter_rules():
        app.add_url_rule(
            rule.rule,
            endpoint=rule.endpoint,
            view_func=generated_module.app.view_functions[rule.endpoint],
            methods=rule.methods
        )
    
    return jsonify({"message": result})

if __name__ == '__main__':
    app.run(debug=True)