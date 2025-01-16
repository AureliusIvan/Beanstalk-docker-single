from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Site(Base):
    """
    Model for sites table.
    Current sites:
    1. Puteri cove residence: PCR
    2. Sri Pulai Perdana: SPP
    3. East Ledang:	ELG
    4. Presint 8:	PR8
    5. Straits View Condominium:	SVC
    6 Salvation Army Malaysia:	SAM
    """
    __tablename__ = "sites"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        doc="Primary key for the site. (e.g. 1, 2, 3, 4, 5, 6)"
    )

    site_name = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
        doc="Name of the site, e.g. Puteri Cove Residence"
    )

    site_code = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
        doc="Code of the site, e.g. PCR"
    )

    # Relationship with utility accounts table
    utility_acct = relationship(
        "UtilityAcct",
        back_populates="site",
        cascade="all, delete"
    )

    # Relationship with bill details
    tnb_bill_details = relationship("TnbBillDetail", back_populates="site")
    malakoff_bill_details = relationship("MalakoffBillDetail", back_populates="site")
    se_bill_details = relationship("SeBillDetail", back_populates="site")
    saj_bill_details = relationship("SajBillDetail", back_populates="site")
    laku_bill_details = relationship("LakuBillDetail", back_populates="site")
    kuching_water_bill_details = relationship("KuchingWaterBillDetail", back_populates="site")
    iwk_bill_details = relationship("IwkBillDetail", back_populates="site")
    telecommunication_bill_details = relationship("TelecommunicationBillDetail", back_populates="site")
    # TODO: add more relationships as needed
