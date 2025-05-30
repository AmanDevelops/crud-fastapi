from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.security import \
    OAuth2PasswordBearer  # Used for OAuth2 authentication, tokenUrl specifies the endpoint for obtaining tokens
from sqlalchemy.orm import Session

from app.database import get_db
from app.exceptions import *
from app.models import Review, User
from app.schemas import LoginDetails, ReviewDetails
from app.utils import create_jwt, verify_jwt, verify_password

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        media_type="application/json",
        content={"success": False, "message": exc.message},
    )


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
        raise InvalidCredentialsException()

    jwt_token = create_jwt({"username": user.username, "role": user.role})

    return JSONResponse(
        content={
            "success": True,
            "username": user.username,
            "auth_token": jwt_token,
            "role": user.role,
        },
        media_type="application/json",
        status_code=200,
    )


def get_review_by_id(id: int, db: Session):
    """
    Helper function to fetch a review by ID.

    Args:
        id: The ID of the review to fetch.
        db: Database session dependency.

    Returns:
        The review object if found, or None if not found.
    """
    review = db.query(Review).filter_by(id=id).first()
    if review is None:
        raise NotFoundException()
    return review


@app.get("/api/v1/get/{id}")
def fetch_data(
    id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """
    Fetches review data based on the provided review ID.

    Args:
        id: The ID of the review to fetch.
        token: The JWT token for authentication.
        db: Database session dependency.

    Returns:
        A JSON response containing the review data if found, or an error message if not found or unauthorized.
    """
    verify_jwt(token)

    review = get_review_by_id(id, db)

    return JSONResponse(
        content={
            "success": True,
            "data": {
                "id": review.id,
                "title": review.title,
                "description": review.description,
                "is_active": review.is_active,
            },
        },
        media_type="application/json",
        status_code=200,
    )


@app.post("/api/v1/add")
def add_data(
    review_details: ReviewDetails,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    Adds a new review to the database.

    Args:
        review_details: The details of the review to be added (title and description).
        token: The JWT token for authentication.
        db: Database session dependency.
    Returns:
        A JSON response containing the success status and the newly added review data, or an error message if unauthorized.
    """
    verify_jwt(token)

    if review_details.title is None or review_details.description is None:
        raise MissingDataException()

    new_review = Review(
        title=review_details.title, description=review_details.description
    )
    db.add(new_review)
    db.commit()

    return JSONResponse(
        content={
            "success": True,
            "data": {
                "id": new_review.id,
                "title": new_review.title,
                "description": new_review.description,
                "is_active": new_review.is_active,
            },
        },
        media_type="application/json",
        status_code=200,
    )


@app.put("/api/v1/update/{id}")
def update_data(
    id: int,
    review_details: ReviewDetails,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    Updates an existing review in the database based on the provided review ID.

    Args:
        id: The ID of the review to update.
        review_details: The updated details of the review (title, description, and is_active status).
        token: The JWT token for authentication.
        db: Database session dependency.

    Returns:
        A JSON response containing the success status and the updated review data, or an error message if unauthorized or the review is not found.
    """
    verify_jwt(token)
    review = get_review_by_id(id, db)

    review.title = (
        review_details.title if review_details.title is not None else review.title
    )
    review.description = (
        review_details.description
        if review_details.description is not None
        else review.description
    )
    review.is_active = (
        review_details.is_active
        if review_details.is_active is not None
        else review.is_active
    )

    db.commit()

    return JSONResponse(
        content={
            "success": True,
            "data": {
                "id": review.id,
                "title": review.title,
                "description": review.description,
                "is_active": review.is_active,
            },
        },
        media_type="application/json",
        status_code=200,
    )


@app.delete("/api/v1/delete/{id}")
def delete_review(
    id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """
    Deletes a review from the database based on the provided review ID.

    Args:
        id: The ID of the review to delete.
        token: The JWT token for authentication.
        db: Database session dependency.

    Returns:
        A JSON response containing the success status and a message indicating the deletion,
        or an error message if unauthorized or the review is not found.
    """
    verify_jwt(token)
    review = get_review_by_id(id, db)

    db.delete(review)
    db.commit()

    return JSONResponse(
        content={"success": True, "message": "Review successfully deleted"},
        media_type="application/json",
        status_code=200,
    )
