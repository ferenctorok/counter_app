from unittest import mock

from counter_app.models import Counter
from counter_app.services import (
    get_or_create_counter,
    modify_counter_by_value,
    set_counter_to_value,
)


def test_get_or_create_counter_creates_counter_if_there_is_none_before(
    session_without_counter_mock: mock.MagicMock,
) -> None:
    """
    Test that a counter is created if there is none in the database yet.

    We expect that the created counter has the initial value of 0, and that the
    appropriate methods on the session mock were called.
    """
    counter = get_or_create_counter(session_without_counter_mock)

    assert counter.value == 0
    session_without_counter_mock.add.assert_called_once_with(counter)
    session_without_counter_mock.commit.assert_called_once()
    session_without_counter_mock.refresh.assert_called_once_with(counter)


def test_get_or_create_counter_returns_existing_counter_if_it_exists(
    session_with_counter_mock: tuple[mock.MagicMock, Counter],
) -> None:
    """Test that the counter is returned from the database if it exists."""
    # Arrange
    session_mock, existing_counter = session_with_counter_mock

    # Act
    counter = get_or_create_counter(session_mock)

    # Assert
    assert counter is existing_counter
    session_mock.add.assert_not_called()
    session_mock.commit.assert_not_called()
    session_mock.refresh.assert_not_called()


def test_modify_counter_by_value_with_non_existent_counter(
    session_without_counter_mock: mock.MagicMock,
) -> None:
    """
    Test modifying the counter by a value when no counter exists yet.

    We expect that a new counter is created with the initial value of 0, and
    then modified by the specified amount.
    """
    # Arrange
    amount = 5

    # Act
    counter = modify_counter_by_value(session_without_counter_mock, amount)

    # Assert
    assert counter.value == amount
    session_without_counter_mock.add.assert_called_once_with(counter)
    session_without_counter_mock.commit.assert_called()
    session_without_counter_mock.refresh.assert_called_with(counter)


def test_modify_counter_by_value_with_existing_counter(
    session_with_counter_mock: tuple[mock.MagicMock, Counter],
) -> None:
    """Test modifying the counter by a value when a counter already exists."""
    # Arrange
    session_mock, existing_counter = session_with_counter_mock
    initial_value = existing_counter.value
    amount = 3

    # Act
    counter = modify_counter_by_value(session_mock, amount)

    # Assert
    assert counter.value == initial_value + amount
    session_mock.add.assert_not_called()
    session_mock.commit.assert_called()
    session_mock.refresh.assert_called_with(counter)


def test_set_counter_to_value_with_non_existent_counter(
    session_without_counter_mock: mock.MagicMock,
) -> None:
    """
    Test setting the counter to a specific value when no counter exists yet.

    We expect that a new counter is created with the specified value.
    """
    # Arrange
    value = 7

    # Act
    counter = set_counter_to_value(session_without_counter_mock, value)

    # Assert
    assert counter.value == value
    session_without_counter_mock.add.assert_called_once_with(counter)
    session_without_counter_mock.commit.assert_called()
    session_without_counter_mock.refresh.assert_called_with(counter)


def test_set_counter_to_value_with_existing_counter(
    session_with_counter_mock: tuple[mock.MagicMock, Counter],
) -> None:
    """Test setting the counter to a value when a counter already exists."""
    # Arrange
    session_mock, _ = session_with_counter_mock
    value = 15

    # Act
    counter = set_counter_to_value(session_mock, value)

    # Assert
    assert counter.value == value
    session_mock.add.assert_not_called()
    session_mock.commit.assert_called()
    session_mock.refresh.assert_called_with(counter)
