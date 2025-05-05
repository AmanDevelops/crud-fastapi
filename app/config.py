import os

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super_secret_password")
JWT_EXPIRY_TIME = 1  # Hours
