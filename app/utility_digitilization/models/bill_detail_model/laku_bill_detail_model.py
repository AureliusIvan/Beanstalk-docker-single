from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Date, Numeric
from app.database import Base
from .base_bill_detail_model import BaseBillDetail


class LakuBillDetail(Base, BaseBillDetail):
    """
    Bill Detail Model for LAKU.
    """
    area_served = Column(String)
    category = Column(String)
    account_number = Column(String)
    meter_no = Column(String)
    bill_no = Column(String)
    usage_below_23000_litres = Column(
        Numeric(9, 2)
    )
    usage_above_23000_litres = Column(
        Numeric(9, 2)
    )
    amount_below_23000_litres = Column(Numeric(9, 2))
    amount_above_23000_litres = Column(Numeric(9, 2), )
    meter_rent = Column(Numeric(9, 2))
    curr_reading = Column(Numeric(9, 2))  # Rename from current_reading if necessary
    prev_reading = Column(Numeric(9, 2))  # Rename from previous_reading if necessary
    total_usage = Column(Numeric(9, 2))  # In litres
    minimum_charge = Column(Numeric(9, 2))
