"""Pydantic models (schemas) for data validation and serialization."""

from pydantic import BaseModel


class LoginDetails(BaseModel):
    """
        Schema for user login credentials.
    """
    username: str
    password: str
