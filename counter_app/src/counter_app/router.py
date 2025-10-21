from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from counter_app import schemas, services
from counter_app.database import DBConnectionManager

counter_router = APIRouter(prefix="/counter", tags=["counter"])


@counter_router.get(
    "",
    summary="Get current counter value",
    description=(
        "Retrieve the current value of the counter. If no counter exists yet,"
        " one will be created automatically."
    ),
    response_model=schemas.CounterValue,
    response_description="Current counter value",
    tags=["counter"],
    responses={
        200: {"description": "Counter value retrieved successfully"},
        500: {"description": "Internal server error"},
    },
)
def read_counter(
    db_sess: Session = Depends(DBConnectionManager.get_session),
) -> schemas.CounterValue:
    """Get the current value of the counter."""
    counter = services.get_or_create_counter(db_sess)
    return schemas.CounterValue(value=counter.value)


@counter_router.post(
    "/increment",
    summary="Increment counter",
    description=(
        "Increase the counter by a specified positive amount. The amount must"
        " be greater than zero."
    ),
    status_code=status.HTTP_200_OK,
    response_description="Counter incremented successfully (no response body)",
    tags=["counter"],
    responses={
        200: {"description": "Counter incremented successfully"},
        400: {"description": "Invalid increment amount; must be positive"},
        500: {"description": "Internal server error"},
    },
)
def increment(
    payload: schemas.CounterIncrement,
    db_sess: Session = Depends(DBConnectionManager.get_session),
) -> Response:
    """Increment the counter by the specified positive amount."""
    if payload.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount must be positive",
        )
    services.modify_counter_by_value(db_sess, payload.amount)
    return Response(status_code=status.HTTP_200_OK)


@counter_router.post(
    "/reset",
    summary="Reset counter",
    description="Reset the counter to zero.",
    status_code=status.HTTP_200_OK,
    response_description="Counter reset successfully (no response body)",
    tags=["counter"],
    responses={
        200: {"description": "Counter reset successfully"},
        500: {"description": "Internal server error"},
    },
)
def reset(
    db_sess: Session = Depends(DBConnectionManager.get_session),
) -> Response:
    """Reset the counter to zero."""
    services.set_counter_to_value(db_sess, 0)
    return Response(status_code=status.HTTP_200_OK)
