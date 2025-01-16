from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class UtilityProvider(Base):
    """
    Model for Utility Provider.
    1.	Tenaga Nasional Berhad (Electricity) -> Code: TNB
    2.	Malakoff (Electricity) -> Code: MALA
    3.	Sarawak Energy (Electricity) -> Code: SKE
    4.	Syarikat Air Johor (Water) -> Code: SAJ
    5.	LAKU(Bintulu) (Water) -> Code: LAKUB
    6.	Kuching Water (Water) -> Code: KW
    7.	Indah Water Konsortium (Sewerage) -> Code: IWK
    8.	Telecommunication (Telecommunication) -> Code: TELECOM
    """
    __tablename__ = "utility_providers"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
        doc="Primary key for the utility provider. e.g. 1"
    )

    name = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
        doc="Name of the utility provider. (e.g. Tenaga Nasional Berhad)"
    )

    service_type = Column(
        String,
        index=True,
        nullable=False,
        doc="Type of service provided by the utility provider. (e.g. Electricity, Water, Telecommunication)"
    )

    code = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
        doc="Code of the utility provider. (e.g. TNB, MALA, SKE, SAJ, LAKUB, KW, IWK, TELECOM)"
    )

    utility_acct = relationship(
        "UtilityAcct",
        back_populates="utility_provider"
    )
