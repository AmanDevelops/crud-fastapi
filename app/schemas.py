"""Pydantic models (schemas) for data validation and serialization."""

from pydantic import BaseModel


class LoginDetails(BaseModel):
    """
        Schema for user login credentials.
    """
    username: str
    password: str

class ReviewDetails(BaseModel):
    """
    Schema for user reviews, including a title and description.
    """
    title: str
    description: str
