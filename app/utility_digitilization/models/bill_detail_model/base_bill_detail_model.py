from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Date, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid


@as_declarative()
class BaseBillDetail:
    """
    Abstract base model for all database models.
    Provides common fields and utility methods.
    """
    id = Column(
        String,
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

    site_id = Column(
        Integer,
        ForeignKey("sites.id", ondelete="CASCADE"),
        nullable=False,
        doc="Foreign key to the sites table."
    )

    utility_accts_id = Column(
        Integer,
        ForeignKey("utility_accts.id", ondelete="CASCADE"),
        nullable=False,
        doc="Foreign key to the utility accounts table."
    )

    utility_bills_id = Column(
        String,
        ForeignKey("utility_bills.id", ondelete="CASCADE"),
        nullable=False,
        doc="Foreign key to the utility bills table."
    )

    invoice_number = Column(
        String,
        nullable=False,
        doc="Invoice number."
    )

    month = Column(
        Integer,
        nullable=False,
        doc="Month of the bill."
    )

    days = Column(
        Integer,
        nullable=False,
        doc="Number of days in the billing period."
    )

    bill_date = Column(
        Date,
        nullable=False,
        doc="Date of the bill."
    )

    bill_period_from = Column(
        Date,
        nullable=False,
        doc="Billing period start date."
    )

    bill_period_to = Column(
        Date,
        nullable=False,
        doc="Billing period end date."
    )

    late_payment_charge_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Late payment charge in RM."
    )

    discount_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Discount in RM."
    )

    arrears_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Arrears amount in RM."
    )

    current_due_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Due amount in RM."
    )

    total_due_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Total due amount in RM."
    )

    date_of_last_payment = Column(
        Date,
        nullable=True,
        doc="Date of last payment."
    )

    amount_of_last_payment_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Amount of last payment in RM."
    )

    rounding_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Rounding amount in RM."
    )

    total_bill_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Total bill amount in RM."
    )

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # Relationships
    @declared_attr
    def site(cls):
        """
        Relationship to the `Site` model.
        """
        return relationship("Site", back_populates=cls.__tablename__)

    @declared_attr
    def utility_bill(cls):
        """
        Relationship to the `UtilityBill` model.
        """
        return relationship("UtilityBill", back_populates=cls.__tablename__)

    @declared_attr
    def utility_acct(cls):
        """
        Relationship to the `UtilityAcct` model.
        """
        return relationship("UtilityAcct", back_populates=cls.__tablename__)

    def get_table_name(self):
        """
        Return the table name.
        """
        return self.__tablename__

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

    def save(self, db_session):
        """
        Save the current instance to the database.
        """
        db_session.add(self)
        db_session.commit()

    def delete(self, db_session):
        """
        Delete the current instance from the database.
        """
        db_session.delete(self)
        db_session.commit()

    @classmethod
    def find_by_id(cls, db_session, record_id):
        """
        Find a record by its ID.
        """
        return db_session.query(cls).filter_by(id=record_id).first()

    @classmethod
    def find_all(cls, db_session):
        """
        Retrieve all records for the model.
        """
        return db_session.query(cls).all()

    def __repr__(self):
        """
        String representation of the model.
        """
        return f"<{self.__class__.__name__} {self.id}>"
