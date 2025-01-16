from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import relationship
from app.database import Base
from .base_tariff_detail_model import BaseTariffDetail


class SeTariffDetail(Base, BaseTariffDetail):
    """
    Model for Sarawak Energy (SE) tariff detail.
    """
    tariff_name = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
        doc="The name of the tariff (e.g., tariff_B, tariff_C1)."
    )

    type = Column(
        String,
        nullable=False,
        doc="Type of tariff (e.g., Commercial, Domestic, Industrial)."
    )

    min_amount = Column(
        Numeric(10, 2),
        nullable=True,
        doc="Minimum amount in RM."
    )

    all_rate = Column(
        Numeric(10, 2),
        nullable=True,
        doc="ALL rate in sen/kWh."
    )

    late_payment_charge = Column(
        Numeric(10, 2),
        nullable=True,
        doc="Late payment charge percentage."
    )

    late_payment_surcharge = Column(
        Numeric(10, 2),
        nullable=True,
        doc="Late payment surcharge in RM."
    )

    md = Column(
        Numeric(10, 2),
        nullable=True,
        doc="MD rate in RM/kW."
    )

    md_peak = Column(
        Numeric(10, 2),
        nullable=True,
        doc="MD PEAK rate in RM/kW."
    )

    peak_rate = Column(
        Numeric(10, 2),
        nullable=True,
        doc="PEAK rate in sen/kWh."
    )

    off_peak_rate = Column(
        Numeric(10, 2),
        nullable=True,
        doc="OFF PEAK rate in sen/kWh."
    )

    clc = Column(
        Numeric(10, 2),
        nullable=True,
        doc="CLC rate in RM/kW."
    )

    icpt = Column(
        Numeric(10, 2),
        nullable=True,
        doc="ICPT rate in sen/kWh."
    )

    kwtbb = Column(
        Numeric(10, 2),
        nullable=True,
        doc="KWTBB rate in percentage."
    )

    disc = Column(
        Numeric(10, 2),
        nullable=True,
        doc="Discount rate percentage."
    )

    optr = Column(
        Numeric(10, 2),
        nullable=True,
        doc="Operational rate percentage."
    )

    pf_0_75 = Column(
        Numeric(10, 2),
        nullable=True,
        doc="Power factor penalty rate at 0.75."
    )

    pf_0_85 = Column(
        Numeric(10, 2),
        nullable=True,
        doc="Power factor penalty rate at 0.85."
    )

    # Relationship to SeTariffRate
    se_tier_rates = relationship("SeTariffRate", back_populates="se_tariff", cascade="all, delete-orphan")
