from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from app.database import Base
from .base_tariff_rate_model import BaseTariffRate


class LakuBintuluTariffRate(Base, BaseTariffRate):
    """
    Model for Laku (Bintulu) Tariff Rate.
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

    laku_bintulu_tariff_details_id = Column(
        Integer,
        ForeignKey("laku_bintulu_tariff_details.id", ondelete="CASCADE"),
        nullable=False,
        doc="Foreign key to the tariff detail."
    )
