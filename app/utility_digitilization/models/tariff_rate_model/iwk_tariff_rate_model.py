from app.database import Base
from sqlalchemy import Column, Integer
from .base_tariff_rate_model import BaseTariffRate


class IwkTariffRate(Base, BaseTariffRate):
    """
    Model for IWK Tariff Rates.
    """
    tier_name = Column(
        Integer,
        nullable=False,
        doc="Name of the tariff tier."
    )

    min_usage_l = Column(
        Integer,
        nullable=False,
        doc="Minimum usage in liters for this tier."
    )

    max_usage_l = Column(
        Integer,
        nullable=False,
        doc="Maximum usage in liters for this tier."
    )

    rate_rm_per_1000l = Column(
        Integer,
        nullable=False,
        doc="Rate in RM per 1000 liters for this tier."
    )

    iwk_tariff_details_id = Column(
        Integer,
        nullable=False,
        doc="Foreign key to the IWK tariff."
    )
