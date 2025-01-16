from sqlalchemy import Column, Integer, Numeric, Date
from app.database import Base
from .base_bill_detail_model import BaseBillDetail


class TnbBillDetail(Base, BaseBillDetail):
    """
    Model for TNB Bill Details.
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

    t1_amount_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="T1 amount in RM."
    )

    t2_amount_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="T2 amount in RM."
    )

    t3_amount_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="T3 amount in RM."
    )

    t4_amount_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="T4 amount in RM."
    )

    t5_amount_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="T5 amount in RM."
    )

    t1_usage_kwh = Column(
        Integer,
        nullable=True,
        doc="T1 usage in kilowatt hours (kWh)."
    )

    t2_usage_kwh = Column(
        Integer,
        nullable=True,
        doc="T2 usage in kilowatt hours (kWh)."
    )

    t3_usage_kwh = Column(
        Integer,
        nullable=True,
        doc="T3 usage in kilowatt hours (kWh)."
    )

    t4_usage_kwh = Column(
        Integer,
        nullable=True,
        doc="T4 usage in kilowatt hours (kWh)."
    )

    t5_usage_kwh = Column(
        Integer,
        nullable=True,
        doc="T5 usage in kilowatt hours (kWh)."
    )

    pdd_office_usage_kwh = Column(
        Integer,
        nullable=True,
        doc="PDD office usage in kilowatt hours (kWh)."
    )

    pdd_office_amount_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="PDD office amount in RM."
    )

    residential_usage_kwh = Column(
        Integer,
        nullable=True,
        doc="Residential usage in kilowatt hours (kWh)."
    )

    residential_amount_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Residential amount in RM."
    )

    common_usage_kwh = Column(
        Integer,
        nullable=True,
        doc="Common usage in kilowatt hours (kWh)."
    )

    common_amount_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Common amount in RM."
    )
