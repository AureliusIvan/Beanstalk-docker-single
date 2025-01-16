from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from .base_tariff_rate_model import BaseTariffRate


class SeTariffRate(Base, BaseTariffRate):
    """
    Model for Sarawak Energy tariff tier rate.
    """
    tier_name = Column(
        String,
        nullable=False,
        doc="The name of the tier (e.g., 1-100, >1300)."
    )

    min_usage_kwh = Column(
        Integer,
        nullable=False,
        doc="Minimum usage for the tier in units."
    )

    max_usage_kwh = Column(
        Integer,
        nullable=False,
        doc="Maximum usage for the tier in kWh; 0 if no upper limit."
    )

    rate_sen_per_kwh = Column(
        Numeric(10, 2),
        nullable=False,
        doc="Rate for the tier in sen/kWh."
    )

    se_tariff_id = Column(
        Integer,
        ForeignKey("se_tariff_details.id"),
        nullable=False,
        doc="Foreign key referencing the Sarawak Energy tariff this tier belongs to."
    )

    se_tariff = relationship("SeTariffDetail", back_populates="se_tier_rates")
