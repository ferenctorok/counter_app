from pydantic import BaseModel


class CounterValue(BaseModel):
    """Schema for representing the counter value."""

    value: int


class CounterIncrement(BaseModel):
    """Schema for an increment request."""

    amount: int
