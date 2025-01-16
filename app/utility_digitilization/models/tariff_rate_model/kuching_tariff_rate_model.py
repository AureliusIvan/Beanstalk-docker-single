from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from app.database import Base
from .base_tariff_rate_model import BaseTariffRate


class KuchingTariffRate(Base, BaseTariffRate):
    """
    Model for Kuching Water Tariff Rate.
    """
    tier_name = Column(
        String,
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
        Numeric(10, 2),
        nullable=False,
        doc="Rate in RM per 1000 liters for this tier."
    )

    kuching_tariff_details_id = Column(
        Integer,
        ForeignKey("kuching_tariff_details.id", ondelete="CASCADE"),
        nullable=False,
        doc="Foreign key to the Kuching tariff."
    )
