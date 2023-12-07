"""Schemas for the API."""
from pydantic import BaseModel, Field


## API Schemas
class ProductMessage(BaseModel):
    """Represents the id passed by the scanner when a product is scanned.

    Args:
        product_id (str): The ID of the product
        message (str): The content of the message.
    """

    product_id: str = Field(..., example="1457564")
    quantity: int = Field(..., example=1)


## API Schemas
class UserMessage(BaseModel):
    """Represents the id passed by the scanner when a iser credential is scanned.

    Args:
        message (str): The content of the message.
    """

    message: str = Field(..., example="10001")
