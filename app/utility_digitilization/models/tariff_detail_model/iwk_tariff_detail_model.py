from app.database import Base
from .base_tariff_detail_model import BaseTariffDetail


class IwkTariffDetail(Base, BaseTariffDetail):
    """
    Model for IWK tariff detail.
    """
