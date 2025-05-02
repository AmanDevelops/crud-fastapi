import bcrypt
import app.config as config
import datetime
import jwt

def encrypt_password(password: str) -> str:
    """Hashes a password using bcrypt."""
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a stored bcrypt hash."""
    plain_password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)

def create_jwt(payload: dict) -> str:
    """
    Creates JWT Token with secret key from config.py
    """
    payload['exp'] = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=config.JWT_EXPIRY_TIME)
    return jwt.encode(payload, config.JWT_SECRET_KEY, algorithm='HS256')

def verify_jwt(token: str) -> dict:
    try:
        decoded = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=["HS256"])
        return {
            "success": True,
            "payload": decoded
        }
    except jwt.ExpiredSignatureError:
        return {
            "success": False,
            "code": "TOKEN_EXPIRED"
        }
    except jwt.InvalidTokenError:
        return {
            "success": False,
            "code": "INVALID_TOKEN"
        }