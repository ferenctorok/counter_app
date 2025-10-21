from unittest import mock

import pytest

from counter_app.models import Counter


@pytest.fixture(name="session_without_counter_mock")
def fxt_session_mock() -> mock.MagicMock:
    """
    Create a mock for a session that does not yet have a counter.

    If there is no counter in the dataset yet, `db_sess.query(Counter).first()`
    returns None. With this fixture, we create a mock that mocks this behavior.
    """
    session_mock = mock.MagicMock()
    session_mock.query().first.return_value = None
    return session_mock


@pytest.fixture(name="session_with_counter_mock")
def fxt_session_with_counter_mock() -> tuple[mock.MagicMock, Counter]:
    """
    Create a mock for a session that already has a counter.

    If there is already a counter in the dataset,
    `db_sess.query(Counter).first()` returns that counter. With this fixture, we
    create a mock that mocks this behavior.
    """
    session_mock = mock.MagicMock()
    counter = Counter(value=10)
    session_mock.query().first.return_value = counter
    return session_mock, counter
