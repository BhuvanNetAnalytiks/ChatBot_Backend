from main_library.model import DepartmentClassifier

def department_detection(user_message):
    print("USER MESSAGE:",user_message)
    """
    Handles user messages by classifying the department and responding accordingly.
    """    
    # Initialize classifiers
    department_classifier = DepartmentClassifier(
        model_path='/home/spurge/Desktop/ChatBot_Backend/main_library/dp_classifier_model.h5',
        embedding_model_name='all-MiniLM-L6-v2', # put your absolute path
        labels_path='/home/spurge/Desktop/ChatBot_Backend/main_library/labels.json' # put your absolute path
    )

    # Ensure input is stripped of leading/trailing spaces
    processing_message = user_message.strip()
    
    # Predict department
    department = department_classifier.predict_department(processing_message)
    # print(f"Detected Department: {department}")
    
    return department

