from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from enum import Enum
import uuid
from datetime import datetime


class SizeEnum(str, Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class CoffeeTypeEnum(str, Enum):
    ICED = "iced"
    HOT = "hot"


class FlavorEnum(str, Enum):
    FRENCH_VANILLA = "french vanilla"
    HAZELNUT = "hazelnut"
    CARAMEL = "caramel"
    MOCHA = "mocha"
    VANILLA = "vanilla"
    CINNAMON = "cinnamon"


class MilkTypeEnum(str, Enum):
    WHOLE = "whole"
    OAT = "oat"
    ALMOND = "almond"
    SOY = "soy"
    NONE = "none"


class CoffeeOrder(BaseModel):
    size: SizeEnum = Field(..., description="Size of the coffee")
    coffee_type: CoffeeTypeEnum = Field(..., description="Type of coffee (iced or hot)")
    flavors: list[FlavorEnum] = Field(default=[], description="List of flavors to add")
    milk: Optional[MilkTypeEnum] = Field(None, description="Type of milk to use")
    extra_shot: Optional[int] = Field(None, ge=0, le=5, description="Number of extra espresso shots (0-5)")
    special_instructions: Optional[str] = Field(None, max_length=200, description="Special instructions for the order")

    @validator('extra_shot')
    def validate_extra_shot(cls, v):
        if v is not None and v < 0:
            raise ValueError('Extra shots cannot be negative')
        if v is not None and v > 5:
            raise ValueError('Maximum 5 extra shots allowed')
        return v

    @validator('flavors')
    def validate_flavors(cls, v):
        if len(v) > 3:
            raise ValueError('Maximum 3 flavors allowed per coffee')
        return v


class CoffeeOrderResponse(BaseModel):
    order_id: str = Field(..., description="Unique order identifier")
    size: SizeEnum
    coffee_type: CoffeeTypeEnum
    flavors: list[FlavorEnum]
    milk: Optional[MilkTypeEnum]
    extra_shot: Optional[int]
    special_instructions: Optional[str]
    estimated_price: float = Field(..., description="Estimated price in USD")
    estimated_prep_time: int = Field(..., description="Estimated preparation time in minutes")
    order_time: datetime = Field(..., description="Time when order was placed")
    status: Literal["received", "preparing", "ready", "completed"] = Field(default="received")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class OrderStatus(BaseModel):
    order_id: str
    status: Literal["received", "preparing", "ready", "completed"]
    estimated_ready_time: Optional[datetime] = None


class MenuResponse(BaseModel):
    sizes: list[str]
    coffee_types: list[str]
    flavors: list[str]
    milk_types: list[str]
    max_extra_shots: int = 5
    max_flavors: int = 3
