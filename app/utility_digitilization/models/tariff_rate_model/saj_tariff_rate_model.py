from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from app.database import Base
from .base_tariff_rate_model import BaseTariffRate


class SajTariffRate(Base, BaseTariffRate):
    """
    Model for SAJ Tariff Rate.
    """
    saj_tariff_id = Column(
        Integer,
        ForeignKey("saj_tariff_details.id", ondelete="CASCADE"),
        nullable=False,
        doc="Foreign key to the SAJ tariff."
    )

    tier_name = Column(
        String,
        nullable=False,
        doc="Name of the tariff tier."
    )

    min_usage_m3 = Column(
        Integer,
        nullable=False,
        doc="Minimum usage in cubic meters (m³) for this tier."
    )

    max_usage_m3 = Column(
        Integer,
        nullable=False,
        doc="Maximum usage in cubic meters (m³) for this tier."
    )

    rate_rm_per_m3 = Column(
        Numeric(9, 2),
        nullable=False,
        doc="Rate in RM per cubic meter for this tier."
    )
