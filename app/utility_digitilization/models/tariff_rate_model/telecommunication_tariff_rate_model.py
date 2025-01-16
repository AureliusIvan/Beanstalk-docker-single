from app.database import Base
from .base_tariff_rate_model import BaseTariffRate


class TelecommunicationTariffRate(Base, BaseTariffRate):
    """
    Model for Telecommunication Tariff Rate.
    """
