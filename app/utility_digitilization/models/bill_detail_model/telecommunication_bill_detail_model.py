from sqlalchemy import Column, Integer, Numeric, Date
from app.database import Base
from .base_bill_detail_model import BaseBillDetail


class TelecommunicationBillDetail(Base, BaseBillDetail):
    """
    Model for Telecommunication Bill Details.
    """
    internet_wifi_charges_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Internet/WiFi charges in RM."
    )

    phone_charges_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Phone charges in RM."
    )

    monthly_charges_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Monthly charges in RM."
    )

    service_tax_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Service tax in RM."
    )

    discount_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Discount in RM."
    )

    date_of_last_payment = Column(
        Date,
        nullable=True,
        doc="Date of the last payment."
    )

    amount_of_last_payment_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Amount of the last payment in RM."
    )
