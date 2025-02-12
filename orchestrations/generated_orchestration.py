from flask import Flask, jsonify, request
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

app = Flask(__name__)

from main_library.function1 import function

@app.route('/run_function1', methods=['POST'])
def function_api():
    params = request.json if request.is_json else request.args
    result = function(**params)
    return jsonify({'result': result})

from main_library.function2 import function2

@app.route('/run_function2', methods=['GET'])
def function2_api():
    params = request.json if request.is_json else request.args
    result = function2(**params)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
