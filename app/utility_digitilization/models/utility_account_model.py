from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class UtilityAcct(Base):
    """
    Model for utility accounts.
    """
    __tablename__ = "utility_accts"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
        doc="Primary key for the utility account."
    )

    site_id = Column(
        Integer,
        ForeignKey("sites.id", ondelete="CASCADE"),
        nullable=False,
        doc="Foreign key to the sites table."
    )

    account_num = Column(
        String,
        nullable=False,
        doc="Account number."
    )

    utility_provider_id = Column(
        Integer,
        ForeignKey("utility_providers.id", ondelete="CASCADE"),
        nullable=False,
        doc="Foreign key to the utility providers table."
    )

    area_served = Column(
        String,
        nullable=True,
        doc="Area served."
    )

    contract_num = Column(
        String,
        nullable=True,
        doc="Contract number."
    )

    meter_num = Column(
        String,
        nullable=True,
        doc="Meter number."
    )

    deposit_rm = Column(
        Numeric(9, 2),
        nullable=True,
        doc="Deposit amount in RM."
    )

    tnb_malakoff_tariff_id = Column(
        Integer,
        ForeignKey("tnb_malakoff_tariff_details.id"),
        nullable=True,
        doc="Foreign key to the TNB tariff."
    )

    saj_tariff_id = Column(
        Integer,
        ForeignKey("saj_tariff_details.id"),
        nullable=True,
        doc="Foreign key to the SAJ tariff."
    )

    se_tariff_id = Column(
        Integer,
        ForeignKey("se_tariff_details.id"),
        nullable=True,
        doc="Foreign key to the Sarawak Energy tariff."
    )

    laku_bintulu_tariff_id = Column(
        Integer,
        ForeignKey("laku_bintulu_tariff_details.id"),
        nullable=True,
        doc="Foreign key to the LAKU Bintulu tariff."
    )

    kuching_tariff_id = Column(
        Integer,
        ForeignKey("kuching_tariff_details.id"),
        nullable=True,
        doc="Foreign key to the Kuching Water Board tariff."
    )

    iwk_tariff_id = Column(
        Integer,
        ForeignKey("iwk_tariff_details.id"),
        nullable=True,
        doc="Foreign key to the Indah Water Konsortium tariff."
    )

    telecommunication_tariff_id = Column(
        Integer,
        ForeignKey("telecommunication_tariff_details.id"),
        nullable=True,
        doc="Foreign key to the telecommunication tariff."
    )

    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # relationships
    site = relationship("Site", back_populates="utility_acct")
    utility_provider = relationship("UtilityProvider", back_populates="utility_acct")
    utility_bill = relationship("UtilityBill", back_populates="utility_acct")

    tnb_bill_details = relationship("TnbBillDetail", back_populates="utility_acct")
    malakoff_bill_details = relationship("MalakoffBillDetail", back_populates="utility_acct")
    se_bill_details = relationship("SeBillDetail", back_populates="utility_acct")
    saj_bill_details = relationship("SajBillDetail", back_populates="utility_acct")
    laku_bill_details = relationship("LakuBillDetail", back_populates="utility_acct")
    kuching_water_bill_details = relationship("KuchingWaterBillDetail", back_populates="utility_acct")
    iwk_bill_details = relationship("IwkBillDetail", back_populates="utility_acct")
    telecommunication_bill_details = relationship("TelecommunicationBillDetail", back_populates="utility_acct")

    tnb_malakoff_tariff_details = relationship("TnbMalakoffTariffDetail", back_populates="utility_acct")
    saj_tariff_details = relationship("SajTariffDetail", back_populates="utility_acct")
    se_tariff_details = relationship("SeTariffDetail", back_populates="utility_acct")
    laku_bintulu_tariff_details = relationship("LakuBintuluTariffDetail", back_populates="utility_acct")
    kuching_tariff_details = relationship("KuchingTariffDetail", back_populates="utility_acct")
    iwk_tariff_details = relationship("IwkTariffDetail", back_populates="utility_acct")
    telecommunication_tariff_details = relationship("TelecommunicationTariffDetail", back_populates="utility_acct")

    tnb_malakoff_tariff = relationship("TnbMalakoffTariffDetail", back_populates="utility_acct")
    saj_tariff = relationship("SajTariffDetail", back_populates="utility_acct")
    se_tariff = relationship("SeTariffDetail", back_populates="utility_acct")
    laku_bintulu_tariff = relationship("LakuBintuluTariffDetail", back_populates="utility_acct")
    kuching_tariff = relationship("KuchingTariffDetail", back_populates="utility_acct")
    iwk_tariff = relationship("IwkTariffDetail", back_populates="utility_acct")
    telecommunication_tariff = relationship("TelecommunicationTariffDetail", back_populates="utility_acct")
