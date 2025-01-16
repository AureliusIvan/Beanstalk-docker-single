from sqlalchemy import Column, Integer, ForeignKey, Date, DateTime, String
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid

class UtilityBill(Base):
    """
    Model for Utility bill.
    """
    __tablename__ = "utility_bills"

    id = Column(
        String,
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        doc="Primary key for the utility bill, using UUID."
    )

    utility_accts_id = Column(
        Integer,
        ForeignKey("utility_accts.id", ondelete="CASCADE"),
        nullable=False,
        doc="Foreign key to the Utility account. Used by the bill detail."
    )

    uploaded_at = Column(DateTime, default=datetime.now, nullable=False)

    bill_month_year = Column(
        Date,
        nullable=False,
        doc="Month and year of the bill."
    )

    file = Column(
        Integer,
        nullable=True,
        doc="Blob file of the bill."
    )

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # relationship
    utility_acct = relationship(
        "UtilityAcct",
        back_populates="utility_bill"
    )

    # Bill details relationships for various types of bills
    tnb_bill_details = relationship(
        "TnbBillDetail",
        back_populates="utility_bill",
        cascade="all, delete-orphan",
        doc="Details specific to TNB utility bill."
    )

    malakoff_bill_details = relationship(
        "MalakoffBillDetail",
        back_populates="utility_bill",
        cascade="all, delete-orphan",
        doc="Details specific to Malakoff utility bill."
    )

    se_bill_details = relationship(
        "SeBillDetail",
        back_populates="utility_bill",
        cascade="all, delete-orphan",
        doc="Details specific to SE utility bill."
    )

    saj_bill_details = relationship(
        "SajBillDetail",
        back_populates="utility_bill",
        cascade="all, delete-orphan",
        doc="Details specific to SAJ utility bill."
    )

    laku_bill_details = relationship(
        "LakuBillDetail",
        back_populates="utility_bill",
        cascade="all, delete-orphan",
        doc="Details specific to LAKU utility bill."
    )

    kuching_water_bill_details = relationship(
        "KuchingWaterBillDetail",
        back_populates="utility_bill",
        cascade="all, delete-orphan",
        doc="Details specific to Kuching Water utility bill."
    )

    iwk_bill_details = relationship(
        "IwkBillDetail",
        back_populates="utility_bill",
        cascade="all, delete-orphan",
        doc="Details specific to IWK utility bill."
    )
    telecommunication_bill_details = relationship(
        "TelecommunicationBillDetail",
        back_populates="utility_bill",
        cascade="all, delete-orphan",
        doc="Details specific to Telecommunication utility bill."
    )
