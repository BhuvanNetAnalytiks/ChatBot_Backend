from flask import Flask, request, jsonify
import os
import json
from orchestration_generator import create_orchestration

app = Flask(__name__)

ORCHESTRATION_JSON_PATH = os.path.join(os.path.dirname(__file__), "orchestration.json")


@app.route("/api/save_orchestration", methods=["POST"])
def save_orchestration():
    try:
        # Load orchestration JSON from file
        if not os.path.exists(ORCHESTRATION_JSON_PATH):
            return jsonify({"error": "orchestration.json not found"}), 400

        with open(ORCHESTRATION_JSON_PATH, "r") as f:
            orchestration_data = json.load(f)

        # Call function to generate orchestration file
        result = create_orchestration(orchestration_data)

        return jsonify({"message": "Orchestration file saved successfully", "file": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
