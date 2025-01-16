from sqlalchemy import Column, Integer, Numeric, Date
from app.database import Base
from .base_bill_detail_model import BaseBillDetail


class SeBillDetail(Base, BaseBillDetail):
    """
    Model for Serawak Energy Bill Details.
    """
    prev_reading_kwh = Column(
        Integer,
        nullable=True,
        doc="Previous meter reading in kWh."
    )

    curr_reading_kwh = Column(
        Integer,
        nullable=True,
        doc="Current meter reading in kWh."
    )

    peak_usage_kwh = Column(
        Integer,
        nullable=True,
        doc="Peak usage in kWh."
    )

    peak_amount_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Peak amount in RM."
    )

    non_peak_usage_kwh = Column(
        Integer,
        nullable=True,
        doc="Non-peak usage in kWh."
    )

    non_peak_amount_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Non-peak amount in RM."
    )

    total_usage_kwh = Column(
        Integer,
        nullable=True,
        doc="Total usage in kWh."
    )

    total_amount_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Total amount in RM."
    )

    max_demand = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Maximum demand."
    )

    max_demand_amount_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Maximum demand amount in RM."
    )

    icpt_amount_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="ICPT amount in RM."
    )

    clc_amount_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="CLC amount in RM."
    )

    kwtbb_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="KWTBB amount in RM."
    )

    power_factor = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Power factor."
    )

    power_factor_penalty_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Power factor penalty in RM."
    )

    load_factor_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Load factor in RM."
    )

    late_payment_charge_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Late payment charge in RM."
    )

    due_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Due amount in RM."
    )

    total_due_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Total due amount in RM."
    )

    date_of_last_payment = Column(
        Date,
        nullable=True,
        doc="Date of last payment."
    )

    amount_of_last_payment_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Amount of last payment in RM."
    )

    usage = Column(
        Integer,
        nullable=True,
        doc="Usage."
    )

    usage_incl_maintenance = Column(
        Integer,
        nullable=True,
        doc="Usage including maintenance."
    )

    usage_excl_maintenance = Column(
        Integer,
        nullable=True,
        doc="Usage excluding maintenance."
    )

    amount_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Amount in RM."
    )

    amount_incl_maintenance_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Amount including maintenance in RM."
    )

    amount_excl_maintenance_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Amount excluding maintenance in RM."
    )

    min_monthly_charge_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Minimum monthly charge in RM."
    )
