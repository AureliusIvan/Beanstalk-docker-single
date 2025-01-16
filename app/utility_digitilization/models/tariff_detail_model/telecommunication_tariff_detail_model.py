from app.database import Base
from .base_tariff_detail_model import BaseTariffDetail


class TelecommunicationTariffDetail(Base, BaseTariffDetail):
    """
    Model for Telecommunication Tariff Detail.
    """
