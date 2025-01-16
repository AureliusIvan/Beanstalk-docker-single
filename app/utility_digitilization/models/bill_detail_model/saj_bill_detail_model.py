from sqlalchemy import Column, Integer, Numeric, Date
from app.database import Base
from .base_bill_detail_model import BaseBillDetail


class SajBillDetail(Base, BaseBillDetail):
    """
    Model for SAJ Bill Details.
    """
    reading_m3 = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Meter reading in cubic meters (m³)."
    )

    prev_reading_m3 = Column(
        Integer,
        nullable=True,
        doc="Previous meter reading in cubic meters (m³)."
    )

    curr_reading_m3 = Column(
        Integer,
        nullable=True,
        doc="Current meter reading in cubic meters (m³)."
    )

    usage_m3 = Column(
        Integer,
        nullable=True,
        doc="Usage in cubic meters (m³)."
    )

    sub_meter_usage_m3 = Column(
        Integer,
        nullable=True,
        doc="Sub-meter usage in cubic meters (m³)."
    )

    total_usage_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Total usage amount in RM."
    )

    pf = Column(
        Numeric(9, 4),
        nullable=True,
        doc="Power Factor."
    )

    late_payment_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Late payment amount in RM."
    )

    current_due_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Current due amount in RM."
    )

    minimum_charge_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Minimum charge amount in RM."
    )

    total_due_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Total due amount in RM."
    )

    date_of_last_payment = Column(
        Date,
        nullable=True,
        doc="Date of the last payment."
    )

    amount_of_last_payment_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Amount of the last payment in RM."
    )
