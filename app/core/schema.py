from pydantic import BaseModel, Field, EmailStr, validator, PrivateAttr
from typing import Optional
from datetime import date, timedelta, datetime
from uuid import uuid4
from fastapi import Query

# Create Item Schema with Auto-generated item_id and expiry_date as current_date + 1 day
class ItemCreate(BaseModel):
    _item_id: str = PrivateAttr(default_factory=lambda: str(uuid4()))
    name: str = Field(..., example="John Doe")
    email: EmailStr = Field(..., example="john@example.com")
    item_name: str = Field(..., example="Laptop")
    quantity: int = Field(..., example=5)
    _expiry_date: datetime = PrivateAttr(default_factory=lambda: (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'))

    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "john@example.com",
                "item_name": "Laptop",
                "quantity": 5,
                "expiry_date": (datetime.now() + timedelta(days=1)).isoformat()  # Use full datetime in example
            }
        }

# Update Item Schema (for PUT request, Insert Date is excluded)
class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Name")
    email: Optional[str] = Field(None, description="Email")
    item_name: Optional[str] = Field(None, description="Item Name")
    quantity: Optional[int] = Field(None, description="Quantity")
    expiry_date: Optional[datetime] = Field(None, description="Expiry Date in YYYY-MM-DD format", example="2024-12-31")
        
    class Config:
        schema_extra = {
            "example": {
                "name": "John Smith",
                "email": "john.smith@example.com",
                "item_name": "Smartphone",
                "quantity": 10,
                "expiry_date": "2025-12-31"
            }
        }
        
# Response Model for a Single Item
class ItemResponse(BaseModel):
    item_id: str
    name: str
    email: str
    item_name: str
    quantity: int
    expiry_date: str
    insert_date: str

    class Config:
        schema_extra = {
            "example": {
                "id": "60c72b2f9e25a79e2e123456",
                "name": "John Doe",
                "email": "john@example.com",
                "item_name": "Laptop",
                "quantity": 5,
                "expiry_date": "2024-12-31",
                "insert_date": "2024-10-10"
            }
        }

# Response Model for Item Aggregation (Grouped by Email)
class ItemAggregationResponse(BaseModel):
    email: str
    count: int

    class Config:
        schema_extra = {
            "example": {
                "email": "john@example.com",
                "count": 10
            }
        }

# Define the filter request model
class ItemFilterRequest(BaseModel):
    email: Optional[str] = Field(None, description="Email of the item owner")
    expiry_date_after: Optional[str] = Field(None, description="Filter items expiring after this date (YYYY-MM-DD)")
    insert_date_after: Optional[str] = Field(None, description="Filter items inserted after this date (YYYY-MM-DD)")
    quantity_gte: Optional[int] = Field(None, description="Filter items with quantity greater than or equal to this value")

    class Config:
        schema_extra = {
            "example": {
                "email": "john@example.com",
                "expiry_date_after": "2024-12-31",
                "insert_date_after": "2024-01-01",
                "quantity_gte": 5
            }
        }


# Create Clock-In Schema with Auto-generated clock_in_id and insert_date as current datetime
class ClockInCreate(BaseModel):
    _clock_in_id: str = PrivateAttr(default_factory=lambda: str(uuid4()))# Exclude from Swagger UI
    email: EmailStr = Field(..., example="john@example.com")
    location: str = Field(..., example="New York")
    
    class Config:
        schema_extra = {
            "example": {
                # The example won't show 'clock_in_id'
                "email": "john@example.com",
                "location": "New York"
            }
        }
        
# Update Clock-In Schema (Insert DateTime is excluded)
class ClockInUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None, description="Email")
    location: Optional[str] = Field(None, description="Location")
    
    class Config:
        schema_extra = {
            "example": {
                "email": "john.smith@example.com",
                "location": "Los Angeles"
            }
        }

# Response Model for a Single Clock-In Record
class ClockInResponse(BaseModel):
    clock_in_id: str
    email: str
    location: str
    insert_datetime: str

    class Config:
        schema_extra = {
            "example": {
                "clock_in_id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "john@example.com",
                "location": "New York",
                "insert_datetime": "2024-10-12T10:45:00"
            }
        }

# Define the filter request model for Clock-In Records
class ClockInFilterRequest(BaseModel):
    email: Optional[str] = Field(None, description="Email of the user")
    location: Optional[str] = Field(None, description="Location of the clock-in")
    insert_datetime_after: Optional[datetime] = Field(None, description="Filter clock-ins after this datetime")

    class Config:
        schema_extra = {
            "example": {
                "email": "john@example.com",
                "location": "New York",
                "insert_datetime_after": "2024-10-01T00:00:00"
            }
        }
