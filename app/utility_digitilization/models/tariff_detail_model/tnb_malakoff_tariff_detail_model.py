from sqlalchemy import Column, String, Numeric
from sqlalchemy.orm import relationship
from app.database import Base
from .base_tariff_detail_model import BaseTariffDetail


class TnbMalakoffTariffDetail(Base, BaseTariffDetail):
    """
    Model for TNB/Malakoff tariff detail.
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
        doc="Type of tariff (e.g., Low Voltage Commercial Tariff, Medium Voltage Peak/Off-Peak Tariff)."
    )

    min_amount = Column(
        Numeric(10, 2),
        nullable=False,
        doc="Minimum amount charged in RM, with 2 decimal precision."
    )

    all_charge = Column(
        Numeric(10, 2),
        nullable=True,
        doc="Energy charge for all hours in sen per kWh."
    )

    all_incl_maintenance = Column(
        Numeric(10, 2),
        nullable=True,
        doc="Energy charge including maintenance for all hours in sen per kWh."
    )

    all_excl_maintenance = Column(
        Numeric(10, 2),
        nullable=True,
        doc="Energy charge excluding maintenance for all hours in sen per kWh."
    )

    md = Column(
        Numeric(10, 2),
        nullable=True,
        doc="Maximum demand (MD) rate in RM per kW, with 2 decimal precision."
    )

    md_peak = Column(
        Numeric(10, 2),
        nullable=True,
        doc="Peak MD rate in RM per kW, applicable for peak hours."
    )

    peak = Column(
        Numeric(10, 2),
        nullable=True,
        doc="Energy charge during peak hours, in sen per kWh."
    )

    off_peak = Column(
        Numeric(10, 2),
        nullable=True,
        doc="Energy charge during off-peak hours, in sen per kWh."
    )

    clc = Column(
        Numeric(10, 2),
        nullable=True,
        doc="Customer Load Charge (CLC) in RM per kW."
    )

    icpt = Column(
        Numeric(10, 2),
        nullable=True,
        doc="Imbalance Cost Pass-Through (ICPT) rate in sen per kWh."
    )

    kwtbb = Column(
        Numeric(5, 2),
        nullable=True,
        doc="Kumpulan Wang Tenaga Boleh Baharu (KWTBB) levy, expressed as a percentage."
    )

    disc = Column(
        Numeric(5, 2),
        nullable=True,
        doc="Discount percentage, if applicable."
    )

    optr = Column(
        Numeric(5, 2),
        nullable=True,
        doc="Other percentage rate, if applicable."
    )

    pf_0_75 = Column(
        Numeric(5, 2),
        nullable=True,
        doc="Power factor penalty or incentive rate for PF 0.75, as a percentage."
    )

    pf_0_85 = Column(
        Numeric(5, 2),
        nullable=True,
        doc="Power factor penalty or incentive rate for PF 0.85, as a percentage."
    )

    rates = relationship("TnbMalakoffTariffRate", back_populates="detail")
