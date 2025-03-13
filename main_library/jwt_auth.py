import os
import jwt
from datetime import datetime, timedelta
from flask import make_response

# Secret keys for JWT tokens
SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'sess')
REFRESH_SECRET_KEY = os.environ.get('JWT_REFRESH_SECRET_KEY', 'sess-refresh')

COOKIE_NAME = 'auth_token'
REFRESH_COOKIE_NAME = 'refresh_token'

def create_jwt_token(user_id, email, display_name):
    """Generate a short-lived JWT token (expires in 8 hours)."""
    payload = {
        'user_id': user_id,
        'email': email,
        'display_name': display_name,
        'exp': datetime.utcnow() + timedelta(hours=8),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def create_refresh_token(user_id):
    """Generate a long-lived refresh token (expires in 7 days)."""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=7),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, REFRESH_SECRET_KEY, algorithm='HS256')

def verify_jwt_token(token):
    """Verify JWT token and extract user info."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload.get('user_id'), payload.get('email'), payload.get('display_name')
    except jwt.ExpiredSignatureError:
        return 'EXPIRED', None, None
    except jwt.InvalidTokenError:
        return None, None, None

def verify_refresh_token(token):
    """Verify refresh token and extract user_id."""
    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=['HS256'])
        return payload.get('user_id')
    except jwt.ExpiredSignatureError:
        return 'EXPIRED'
    except jwt.InvalidTokenError:
        return None

def set_auth_cookie(jwt_token, refresh_token):
    """Set authentication cookies for JWT and refresh tokens."""
    response = make_response({"message": "Cookies Set"})  # ✅ No jsonify()

    response.set_cookie(
        'auth_token',
        value=jwt_token,
        max_age=8 * 60 * 60,  # 8 hours
        httponly=True,
        secure=True,
        samesite='Strict'
    )
    response.set_cookie(
        'refresh_token',
        value=refresh_token,
        max_age=7 * 24 * 60 * 60,  # 7 days
        httponly=True,
        secure=True,
        samesite='Strict'
    )

    return {"message": "Cookies Set"}  # ✅ Return JSON-serializable object


def clear_auth_cookie():
    """Clear authentication cookies on logout."""
    response = make_response()  # Create an empty response object

    response.set_cookie(
        COOKIE_NAME, '', max_age=0, httponly=True, secure=True, samesite='Strict'
    )
    response.set_cookie(
        REFRESH_COOKIE_NAME, '', max_age=0, httponly=True, secure=True, samesite='Strict'
    )

    return {"message": "Cookies Cleared"}  # ✅ Return a JSON-safe dictionary
