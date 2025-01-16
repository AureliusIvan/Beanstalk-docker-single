from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from datetime import datetime


@as_declarative()
class BaseTariffDetail:
    """
    Abstract base model for all database models.
    """
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    @declared_attr
    def __tablename__(cls):
        """
        Generates __tablename__ automatically based on the class name.
        Converts CamelCase to snake_case.
        """
        # separate CamelCase to snake_case
        cls_name = cls.__name__
        snake_case = [cls_name[0].lower()]
        for char in cls_name[1:]:
            if char.isupper():
                snake_case.append("_")
                snake_case.append(char.lower())
            else:
                snake_case.append(char)
        return "".join(snake_case) + "s"

    @declared_attr
    def utility_acct(cls):
        """
        Relationship to the `Site` model.
        """
        return relationship("UtilityAcct", back_populates=cls.__tablename__)
