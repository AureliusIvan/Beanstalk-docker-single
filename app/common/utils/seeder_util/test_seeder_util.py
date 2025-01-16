import pytest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
from .seeder_util import add_records_to_db


# Mock Model
class MockModel:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @classmethod
    def query(cls, db):
        return db.query(cls)


# Mock Data
mock_data = [
    {"id": 1, "unique_field": "value1", "field1": "data1"},
    {"id": 2, "unique_field": "value2", "field1": "data2"},
]


@pytest.fixture
def mock_db():
    """Fixture for a mock database session."""
    session = MagicMock(spec=Session)
    session.query.return_value.filter_by.return_value.first.side_effect = [None, mock_data[1]]
    return session


def test_add_records_to_db(mock_db):
    """Test the `add_records_to_db` function."""
    # Call the function
    add_records_to_db(mock_db, MockModel, mock_data, "unique_field")

    # Assertions
    # Ensure the session.query was called to check for duplicates
    assert mock_db.query.call_count == 2
    mock_db.query().filter_by.assert_any_call(unique_field="value1")
    mock_db.query().filter_by.assert_any_call(unique_field="value2")

    # Ensure the `add` method was called for only the new record
    assert mock_db.add.call_count == 1
    assert mock_db.add.call_args[0][0].__dict__ == mock_data[0]

    # Ensure no commit was called within this function (it's expected to commit outside)
    assert not mock_db.commit.called
