from app.common.utils.response_util.response_util import create_error_response
from app.utility_digitilization.models.site_model import Site
from app.utility_digitilization.models.utility_provider_model import UtilityProvider
from app.utility_digitilization.schemas.add_utility_account_schema import AddUtilityAccountRequest
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.utility_digitilization.models.utility_account_model import UtilityAcct
from app.utility_digitilization.models.site_model import Site
from sqlalchemy.orm import Session
from collections import defaultdict
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError
import logging
from enum import Enum

router = APIRouter()

logger = logging.getLogger('uvicorn.error')


@router.get("/view-utility-account/{site_code}/{utility_provider_code}")
async def view_utility_account(
        site_code: str,
        utility_provider_code: str,
        db: Session = Depends(get_db)
):
    """
    View Utility Account Details
    Site ID: Unique identifier for the site (0 = All Sites)
    :param utility_provider_code: Utility Provider Code
    :param site_code: Site Code
    :param db: Database Session
    :return: Utility Account Details
    """
    try:
        # Query utility accounts
        query = (
            db
            .query(UtilityAcct)
            .options(
                joinedload(UtilityAcct.site),
                joinedload(UtilityAcct.utility_provider)
            )
            .filter(UtilityAcct.tnb_malakoff_tariff_id.isnot(None))
        )

        # Filter by site_code if provided ("HQ" = All Sites are selected)
        if site_code != "HQ":
            query = query.filter(UtilityAcct.site.has(site_code=site_code))

        # Filter by utility_provider_code if provided
        if utility_provider_code != "ALL":
            query = query.filter(UtilityAcct.utility_provider.has(code=utility_provider_code))

        utility_accounts = query.all()

        # Initialize a dictionary to hold the transformed structure
        sites_dict = defaultdict(lambda: {"ProductName": "", "children": []})

        # Build nested structure
        for account in utility_accounts:
            site_name: str = account.site.site_name
            provider_name: str = account.utility_provider.name
            account_num: str = str(account.account_num)

            # Initialize the site entry if it doesn't exist
            if sites_dict[site_name]["ProductName"] == "":
                sites_dict[site_name]["ProductName"] = site_name

            # Check if provider already added under this site
            provider_entry = next(
                (provider for provider in sites_dict[site_name]["children"] if
                 provider["ProductName"] == provider_name),
                None
            )

            # If provider not found, add a new one
            if not provider_entry:
                provider_entry = {
                    "ProductName": provider_name,
                    "children": []
                }
                sites_dict[site_name]["children"].append(provider_entry)

            # Add account details under the provider
            provider_entry["children"].append({"ProductName": account_num})

        # Convert sites_dict to a list for the final response
        structured_data = list(sites_dict.values())
        return JSONResponse(
            status_code=200,
            content={
                "code": 200,
                "status": "success",
                "message": "Successfully retrieved utility account details.",
                "data": jsonable_encoder(structured_data)
            }
        )
    except SQLAlchemyError as e:
        return create_error_response(
            status_code=500,
            message="An error occurred while retrieving utility account details. Please try again later."
        )
    except Exception as e:
        return create_error_response(
            status_code=500,
            message="An unexpected error occurred while retrieving utility account details. Please try again later."
        )


@router.post("/add-utility-account/", status_code=201)
async def add_utility_account(
        utility_request: AddUtilityAccountRequest,
        db: Session = Depends(get_db)
):
    """
    Add one or multiple Utility Accounts based on the provided accounts list.
    Since tariff_id will substitute the actual tariff_id table such as tnb_malakoff_tariff_id, saj_tariff_id, etc (based on the provider)
    we can use the following code to check if the tariff_id is valid:
    1	Tenaga Nasional Berhad -> tnb_malakoff_tariff_id
    2	Malakoff -> tnb_malakoff_tariff_id
    3	Sarawak Energy -> se_tariff_id
    4	Syarikat Air Johor -> saj_tariff_id
    5	LAKU(Bintulu) -> laku_bintulu_tariff_id
    6	Kuching Water -> kuching_tariff_id
    7	Indah Water Konsortium -> iwk_tariff_id
    8	Telecommunication -> telecom_tariff_id
    """
    site_id = utility_request.site_id

    # Check if the site exists
    site = db.query(Site).filter(Site.id == site_id).first()
    if not site:
        return JSONResponse(
            status_code=404,
            content={
                "data": None,
                "message": f"Site with ID {site_id} not found.",
                "status": "error",
                "code": 404
            }
        )

    # Validate if account number is unique (for each utility provider in the same site)
    for account_data in utility_request.account:
        account_num = account_data.account_num
        utility_provider_id = account_data.utility_provider_id
        account = db.query(UtilityAcct).filter(
            UtilityAcct.site_id == site_id,
            UtilityAcct.account_num == account_num,
            UtilityAcct.utility_provider_id == utility_provider_id
        ).first()

        if account:
            return JSONResponse(
                status_code=400,
                content={
                    "data": None,
                    "message": f"Account number {account_num} already exists for the provider in the site.",
                    "status": "error",
                    "code": 400
                }
            )

    accounts_added = []
    for account_data in utility_request.account:
        utility_provider_id = account_data.utility_provider_id
        account_num = account_data.account_num

        # Check if utility provider exists
        provider = db.query(UtilityProvider).filter(UtilityProvider.id == utility_provider_id).first()
        if not provider:
            return JSONResponse(
                status_code=404,
                content={
                    "data": None,
                    "message": f"Utility Provider with ID {utility_provider_id} not found.",
                    "status": "error",
                    "code": 404
                }
            )

        tariff_id_dict = {
            "tnb_malakoff_tariff_id": None,
            "saj_tariff_id": None,
            "se_tariff_id": None,
            "laku_bintulu_tariff_id": None,
            "kuching_tariff_id": None,
            # "iwk_tariff_id" : None,
            # "telecom_tariff_id" : None
        }

        if account_data.utility_provider_id == 1 or account_data.utility_provider_id == 2:
            tariff_id_dict["tnb_malakoff_tariff_id"] = account_data.tariff_id
        elif account_data.utility_provider_id == 3:
            tariff_id_dict["se_tariff_id"] = account_data.tariff_id
        elif account_data.utility_provider_id == 4:
            tariff_id_dict["saj_tariff_id"] = account_data.tariff_id
        elif account_data.utility_provider_id == 5:
            tariff_id_dict["laku_bintulu_tariff_id"] = account_data.tariff_id
        elif account_data.utility_provider_id == 6:
            tariff_id_dict["kuching_tariff_id"] = account_data.tariff_id
        # elif account_data.utility_provider_id == 7:
        #     tariff_id_dict["iwk_tariff_id"] = account_data.tariff_id
        # elif account_data.utility_provider_id == 8:
        #     tariff_id_dict["telecom_tariff_id"] = account_data.tariff_id

        try:
            # Create and add new utility account
            new_account = UtilityAcct(
                site_id=site_id,
                utility_provider_id=utility_provider_id,
                account_num=account_num,
                contract_num=account_data.contract_num,
                meter_num=account_data.meter_num,
                area_served=account_data.area_served,
                **tariff_id_dict
            )
            db.add(new_account)
            db.commit()
            accounts_added.append({"account_num": account_num, "status": "success"})

        except SQLAlchemyError as e:
            db.rollback()
            logger.error("Database error occurred while adding account.", exc_info=e)
            return JSONResponse(
                status_code=500,
                content={
                    "data": None,
                    "message": "Database error occurred while adding account.",
                    "status": "error",
                    "code": 500
                }
            )

        except Exception as e:
            db.rollback()
            logger.error("Unexpected error occurred while adding account.", exc_info=e)
            return JSONResponse(
                status_code=500,
                content={
                    "data": None,
                    "message": "An unexpected error occurred while adding account.",
                    "status": "error",
                    "code": 500
                }
            )

    return JSONResponse(
        status_code=201,
        content={
            "data": accounts_added,
            "message": "Utility accounts added successfully.",
            "status": "success",
            "code": 201
        }
    )