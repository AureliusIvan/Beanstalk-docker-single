from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError
from fastapi import Depends
from fastapi.responses import JSONResponse
from app.database import get_db
from app.utility_digitilization.models.tariff_detail_model import (
    TnbMalakoffTariffDetail,
    SeTariffDetail,
    SajTariffDetail,
    KuchingTariffDetail,
    LakuBintuluTariffDetail
)
from app.utility_digitilization.models.tariff_rate_model import (
    TnbMalakoffTariffRate,
    SeTariffRate,
    SajTariffRate,
    KuchingTariffRate,
    LakuBintuluTariffRate
)
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
import logging

router = APIRouter()

logger = logging.getLogger('uvicorn.error')


@router.get("/view")
async def view_tariff(db: Session = Depends(get_db)):
    """
    View Tariff Details
    Service Provider ID: Unique identifier for the service provider (0 = All Service Providers)
    :param db: Database Session
    :return: Tariff Details
    """
    tariff_model = {
        1: {
            "tariff_name": "Tenaga Nasional Berhad",
            "tariff_detail": TnbMalakoffTariffDetail,
            "tariff_rate": TnbMalakoffTariffRate,
            "rate_foreign_key": "tnb_tariff_id"
        },
        2: {
            "tariff_name": "Malakoff",
            "tariff_detail": TnbMalakoffTariffDetail,
            "tariff_rate": TnbMalakoffTariffRate,
            "rate_foreign_key": "tnb_tariff_id"
        },
        3: {
            "tariff_name": "Sarawak Energy",
            "tariff_detail": SeTariffDetail,
            "tariff_rate": SeTariffRate,
            "rate_foreign_key": "se_tariff_id"
        },
        4: {
            "tariff_name": "Syarikat Air Johor",
            "tariff_detail": SajTariffDetail,
            "tariff_rate": SajTariffRate,
            "rate_foreign_key": "saj_tariff_id"
        },
        5: {
            "tariff_name": "LAKU Bintulu",
            "tariff_detail": LakuBintuluTariffDetail,
            "tariff_rate": LakuBintuluTariffRate,
            "rate_foreign_key": "laku_bintulu_tariff_details_id"
        },
        6: {
            "tariff_name": "Kuching",
            "tariff_detail": KuchingTariffDetail,
            "tariff_rate": KuchingTariffRate,
            "rate_foreign_key": "kuching_tariff_details_id"
        }
        # TODO: add IWK and telecommunication service providers
    }

    try:
        tariff_list = []
        for key, value in tariff_model.items():
            # Fetch all tariff details for the current tariff
            tariff_details = db.query(value["tariff_detail"]).all()
            tariff_details_list = []

            for detail in tariff_details:
                # Convert the tariff_detail ORM object to a dictionary
                detail_dict = detail.__dict__.copy()
                detail_dict.pop('_sa_instance_state', None)  # Remove SQLAlchemy internal attribute

                # Dynamically get the foreign key field name
                rate_fk = value["rate_foreign_key"]

                # Fetch all tariff rates associated with the current tariff_detail
                tariff_rate_query = db.query(value["tariff_rate"]).filter(
                    getattr(value["tariff_rate"], rate_fk) == detail.id
                ).all()

                # Convert tariff_rate ORM objects to dictionaries
                rates_list = []
                for rate in tariff_rate_query:
                    rate_dict = rate.__dict__.copy()
                    rate_dict.pop('_sa_instance_state', None)
                    rates_list.append(rate_dict)

                # Nest the tariff_rates inside the tariff_detail
                detail_dict["tariff_rates"] = rates_list
                tariff_details_list.append(detail_dict)

            # Append the tariff with nested tariff_details to the tariff_list
            tariff_list.append({
                "tariff_name": value["tariff_name"],
                "tariff_details": tariff_details_list
            })

        return JSONResponse(
            status_code=200,
            content={
                "message": "Tariff details retrieved successfully.",
                "status": "success",
                "code": 200,
                "data": jsonable_encoder(tariff_list)
            }
        )

    except SQLAlchemyError as e:
        return create_error_response(
            status_code=500,
            message=f"Database Server Error, {e}"
        )
    except Exception as e:
        return create_error_response(
            status_code=500,
            message=f"Internal Server Error, {e}"
        )


class ModifyTariffRequest(BaseModel):
    new_tariff_rate: float = Field(..., description="New tariff rate in sen per kWh.")


@router.put("/modify/{service_provider}/{tariff_rate_id}")
async def modify_tariff(service_provider: int,
                        tariff_rate_id: int,
                        request: ModifyTariffRequest,
                        db: Session = Depends(get_db)):
    """
    Update Tariff Details
    :return: Updated Tariff Details
    """

    # based on the service provider id, the tariff details will be fetched from the database
    try:
        if service_provider == 1 or service_provider == 2:
            tariff_rate = db.query(TnbMalakoffTariffRate).filter(TnbMalakoffTariffRate.id == tariff_rate_id).first()
            # modify the tariff rate
            tariff_rate.rate_sen_per_kwh = request.new_tariff_rate
            db.commit()
        elif service_provider == 3:
            tariff_rate = db.query(SeTariffRate).filter(SeTariffRate.id == tariff_rate_id).first()
            tariff_rate.rate_sen_per_kwh = request.new_tariff_rate
            db.commit()
        elif service_provider == 4:
            tariff_rate = db.query(SajTariffRate).filter(SajTariffRate.id == tariff_rate_id).first()
            tariff_rate.rate_sen_per_kwh = request.new_tariff_rate
            db.commit()
        elif service_provider == 5:
            tariff_rate = db.query(LakuBintuluTariffRate).filter(LakuBintuluTariffRate.id == tariff_rate_id).first()
            tariff_rate.rate_sen_per_kwh = request.new_tariff_rate
            db.commit()
        elif service_provider == 6:
            tariff_rate = db.query(KuchingTariffRate).filter(KuchingTariffRate.id == tariff_rate_id).first()
            tariff_rate.rate_sen_per_kwh = request.new_tariff_rate
            db.commit()
        else:
            return JSONResponse(
                status_code=400,
                content={
                    "message": "Invalid service provider.",
                    "status": "error",
                    "code": 400
                }
            )
        return JSONResponse(
            status_code=200,
            content={
                "message": "Tariff details updated successfully.",
                "status": "success",
                "code": 200
            }
        )

    except SQLAlchemyError as e:
        return create_error_response(
            status_code=500,
            message=f"Database Server Error, {e}"
        )
    except Exception as e:
        return create_error_response(
            status_code=500,
            message=f"Internal Server Error, {e}"
        )
