from unittest import mock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from counter_app.database import DBConnectionManager
from counter_app.models import Counter
from counter_app.router import counter_router


@pytest.fixture(name="test_client_with_no_database")
def fxt_test_client_with_no_database() -> TestClient:
    """Create a test client with the counter endpoints included."""
    app = FastAPI()
    app.include_router(counter_router)
    return TestClient(app)


@pytest.fixture(name="test_setup_without_counter")
def fxt_test_setup_without_counter(
    session_without_counter_mock: mock.MagicMock,
) -> tuple[TestClient, mock.MagicMock, int]:
    """
    Create a test client with the counter endpoints included.

    The fixture returns the test client as well as the current counter
    instance in the mocked database session.
    """
    app = FastAPI()
    app.dependency_overrides[DBConnectionManager.get_session] = (
        lambda: session_without_counter_mock
    )
    app.include_router(counter_router)

    return TestClient(app), session_without_counter_mock, 0


@pytest.fixture(name="test_setup_with_counter")
def fxt_test_setup_with_counter(
    session_with_counter_mock: tuple[TestClient, Counter],
) -> tuple[TestClient, mock.MagicMock, int]:
    """
    Create a test client with the counter endpoints included.

    The fixture returns the test client as well as the current value of the
    counter in the mocked database session.
    """
    session_mock, current_counter = session_with_counter_mock

    app = FastAPI()
    app.dependency_overrides[DBConnectionManager.get_session] = (
        lambda: session_mock
    )
    app.include_router(counter_router)
    return TestClient(app), session_mock, current_counter.value


def test_read_counter_with_no_database_throws(
    test_client_with_no_database: TestClient,
) -> None:
    """Test that reading the counter without a database throws."""
    # Arrange
    client = test_client_with_no_database

    # Act
    with pytest.raises(RuntimeError, match=r"Database engine not initialized*"):
        client.get("/counter")


@pytest.mark.parametrize(
    "client_fxt_name",
    ["test_setup_without_counter", "test_setup_with_counter"],
)
def test_read_counter_returns_right_value(
    client_fxt_name: str,
    request: pytest.FixtureRequest,
) -> None:
    """
    Test that reading the counter returns the correct value.

    We expect that independently from whether there is already a counter in the
    database or not, the correct counter value is returned. If there is no
    counter yet, it should be created with the initial value of 0.

    Additionally, we expect that the returned status code is 200.
    """
    # Arrange
    fxt_value = request.getfixturevalue(client_fxt_name)
    client: TestClient = fxt_value[0]
    counter_value: int = fxt_value[2]

    # Act
    response = client.get("/counter")

    # Assert
    exp_status_code = 200
    assert response.status_code == exp_status_code
    assert response.json() == {"value": counter_value}


def test_increment_counter_with_no_database_throws(
    test_client_with_no_database: TestClient,
) -> None:
    """Test that incrementing the counter without a database throws."""
    # Arrange
    client = test_client_with_no_database

    # Act
    with pytest.raises(RuntimeError, match=r"Database engine not initialized*"):
        client.post("/counter/increment", json={"amount": 5})


@pytest.mark.parametrize(
    "client_fxt_name",
    ["test_setup_without_counter", "test_setup_with_counter"],
)
def test_increment_counter_with_negative_amount_returns_400(
    client_fxt_name: str,
    request: pytest.FixtureRequest,
) -> None:
    """Test that incrementing the counter with a negative amount returns 400."""
    # Arrange
    fxt_value = request.getfixturevalue(client_fxt_name)
    client: TestClient = fxt_value[0]

    # Act
    response = client.post("/counter/increment", json={"amount": -3})

    # Assert
    exp_status_code = 400
    assert response.status_code == exp_status_code
    assert response.json() == {"detail": "Amount must be positive"}


@pytest.mark.parametrize(
    "client_fxt_name",
    ["test_setup_without_counter", "test_setup_with_counter"],
)
def test_increment_counter_with_valid_amount(
    client_fxt_name: str,
    request: pytest.FixtureRequest,
) -> None:
    """
    Test that incrementing the counter with a valid amount.

    We expect that the return code is 200, and that there are signs in the
    mocked database session that the counter was modified.
    """
    # Arrange
    fxt_value = request.getfixturevalue(client_fxt_name)
    client: TestClient = fxt_value[0]
    session_mock: mock.MagicMock = fxt_value[1]
    prev_counter_val = fxt_value[2]
    increment_amount = 7

    # Act
    response = client.post(
        "/counter/increment", json={"amount": increment_amount}
    )

    # Assert
    exp_status_code = 200
    assert response.status_code == exp_status_code

    refresh_call_args = session_mock.refresh.call_args_list
    last_args = refresh_call_args[-1][0]
    counter_arg: Counter = last_args[0]
    assert counter_arg.value == prev_counter_val + increment_amount


def test_reset_counter_with_no_database_throws(
    test_client_with_no_database: TestClient,
) -> None:
    """Test that resetting the counter without a database throws."""
    # Arrange
    client = test_client_with_no_database

    # Act
    with pytest.raises(RuntimeError, match=r"Database engine not initialized*"):
        client.post("/counter/reset")


@pytest.mark.parametrize(
    "client_fxt_name",
    ["test_setup_without_counter", "test_setup_with_counter"],
)
def test_reset_counter_resets_counter_to_zero_and_returns_200(
    client_fxt_name: str,
    request: pytest.FixtureRequest,
) -> None:
    """
    Test that resetting the counter sets it to zero.

    We expect that the return code is 200, and that there are signs in the
    mocked database session that the counter was set to zero.
    """
    # Arrange
    fxt_value = request.getfixturevalue(client_fxt_name)
    client: TestClient = fxt_value[0]
    session_mock: mock.MagicMock = fxt_value[1]

    # Act
    response = client.post("/counter/reset")

    # Assert
    exp_status_code = 200
    assert response.status_code == exp_status_code

    refresh_call_args = session_mock.refresh.call_args_list
    last_args = refresh_call_args[-1][0]
    counter_arg: Counter = last_args[0]
    assert counter_arg.value == 0
