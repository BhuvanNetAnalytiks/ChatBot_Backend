from flask import request, jsonify
from main_library.model import DepartmentClassifier


def handle_user_message():
    """
    Handles user messages by classifying the department and responding accordingly.
    """    
    # Initialize classifiers
    department_classifier = DepartmentClassifier(
        model_path='main_library/dp_classifier_model.h5',
        embedding_model_name='all-MiniLM-L6-v2',
        labels_path='main_library/labels.json'
    )

    # Parse user message from UI
    data = request.json
    user_message = data.get('text', '').strip()
    print(user_message)
        
    processing_message = user_message
    department = department_classifier.predict_department(processing_message)
    print(f"Detected Department: {department}")

