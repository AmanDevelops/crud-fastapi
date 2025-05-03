"""Pydantic models (schemas) for data validation and serialization."""

from pydantic import BaseModel
from typing import Optional


class LoginDetails(BaseModel):
    """
        Schema for user login credentials.
    """
    username: str
    password: str

class ReviewDetails(BaseModel):
    """
    Schema for user reviews.

    Fields:
    - title (Optional[str]): The title of the review. Defaults to None.
    - description (Optional[str]): The description of the review. Defaults to None.
    - is_active (Optional[bool]): Indicates if the review is active. Defaults to None.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
