from sqlalchemy import Column, Date, String
from app.database import Base
from .base_bill_detail_model import BaseBillDetail


class KuchingWaterBillDetail(Base, BaseBillDetail):
    """
    Model for Kuching Water bill detail.
    """
