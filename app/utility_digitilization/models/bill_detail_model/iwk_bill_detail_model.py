from sqlalchemy import Column, Numeric, Date
from app.database import Base
from .base_bill_detail_model import BaseBillDetail


class IwkBillDetail(Base, BaseBillDetail):
    """
    Model for IWK Bill Details.
    """
    reading_m3 = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Meter reading in cubic meters (m³)."
    )

    total_usage_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Total usage amount in RM."
    )
