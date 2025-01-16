from sqlalchemy.orm import Session
from typing import List, Dict


# Function to seed the database
def add_records_to_db(db: Session, model, data: List[Dict], unique_field: str):
    """
    Add records to the database if they do not already exist.

    :param db: The database session
    :param model: The database model class
    :param data: The data to be inserted
    :param unique_field: The unique field to check before insertion
    """
    for entry in data:
        if not db.query(model).filter_by(**{unique_field: entry[unique_field]}).first():
            db.add(model(**entry))
