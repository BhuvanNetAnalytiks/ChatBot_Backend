import mysql.connector
import hashlib
import os
from dotenv import load_dotenv
 
# Load environment variables
load_dotenv()
 
def db_auth_handler(action: str, username: str, password: str):
    """
    Handles user authentication (register & login).
    
    Args:
        action (str): 'register' or 'login'
        username (str): User's username
        password (str): User's password
    
    Returns:
        dict: Response status and message
    """
    connection = None
    cursor = None
 
    try:
        # Database Connection
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'auth_system')
        )
        cursor = connection.cursor(dictionary=True)
 
        # Validate Input
        if not username or not password:
            return {"status": "error", "message": "Username and password are required"}
 
        # Hash Password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
 
        if action == "register":
            # Check if username exists
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                return {"status": "error", "message": "Username already exists"}
 
            # Insert New User
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)",
                           (username, hashed_password))
            connection.commit()
            return {"status": "success", "message": "User registered successfully"}
 
        elif action == "login":
            # Verify Credentials
            cursor.execute("SELECT id, password FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
 
            if user and user['password'] == hashed_password:
                return {"status": "success", "message": "Login successful", "user_id": user['id']}
            return {"status": "error", "message": "Invalid username or password"}
 
        else:
            return {"status": "error", "message": "Invalid action"}
 
    except mysql.connector.Error as err:
        return {"status": "error", "message": f"Database error: {str(err)}"}
    
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()