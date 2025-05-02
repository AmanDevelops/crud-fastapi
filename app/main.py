from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import LoginDetails
from app.utils import verify_password, create_jwt

app = FastAPI()


@app.post("/user/login")
def user_login(login_details: LoginDetails, db: Session = Depends(get_db)):
    """
    Authenticates a user based on username and password.

    Args:
        login_details: User login credentials (username and password).
        db: Database session dependency.

    Returns:
        A JSON response containing the username and validation status.
    """

    user = db.query(User).filter_by(username=login_details.username).first()
    if user is None or not verify_password(login_details.password, user.password):
        return JSONResponse(
            content={"error": "Invalid username or password"},
            media_type="application/json",
            status_code=401,
        )

    jwt_payload = {
        "username": user.username,
        "role":"ADMIN"
    }

    jwt_token = create_jwt(jwt_payload)

    return JSONResponse(
            content={
                "username": user.username,
                "auth_token": jwt_token,
                "isValidated": True,
            },
            media_type="application/json",
            status_code=200,
        )
