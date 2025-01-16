from sqlalchemy import Column, String, Numeric
from app.database import Base
from .base_tariff_detail_model import BaseTariffDetail


class KuchingTariffDetail(Base, BaseTariffDetail):
    """
    Model for Kuching tariff detail.
    """

    tariff_name = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
        doc="The name of the tariff (e.g., tariff_B, tariff_C1)."
    )

    min_amount = Column(
        Numeric(10, 2),
        nullable=False,
        doc="Minimum amount charged in RM, with 2 decimal precision."
    )

    average_rate = Column(
        Numeric(10, 2),
        nullable=True,
        doc="Average rate in RM/m^3."
    )
