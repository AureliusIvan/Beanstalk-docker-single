from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from .base_tariff_rate_model import BaseTariffRate


class TnbMalakoffTariffRate(Base, BaseTariffRate):
    """
    Model for TNB Tariff Rate.
    """
    tnb_tariff_id = Column(
        Integer,
        ForeignKey("tnb_malakoff_tariff_details.id", ondelete="CASCADE"),
        nullable=False,
        doc="Foreign key to the TNB tariff."
    )

    tier_name = Column(
        String,
        nullable=False,
        doc="Name of the tariff tier."
    )

    min_usage_kwh = Column(
        Integer,
        nullable=False,
        doc="Minimum usage in kWh for this tier."
    )

    max_usage_kwh = Column(
        Integer,
        nullable=False,
        doc="Maximum usage in kWh for this tier."
    )

    rate_sen_per_kwh = Column(
        Numeric(9, 2),
        nullable=False,
        doc="Rate in sen per kWh for this tier."
    )

    detail = relationship("TnbMalakoffTariffDetail", back_populates="rates")
