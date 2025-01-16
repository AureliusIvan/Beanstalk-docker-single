from fastapi import APIRouter, UploadFile, File, Form
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import SQLAlchemyError
from fastapi import Depends
from fastapi.responses import JSONResponse
from app.database import get_db
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, inspect, Numeric, extract, String, cast, Date, Float, Integer
from app.common.utils.date_util.month_util import int_to_month_name
from app.utility_digitilization.models.utility_bill_model import UtilityBill
from app.utility_digitilization.models.utility_account_model import UtilityAcct
from app.utility_digitilization.models.bill_detail_model import (
    TnbBillDetail,
)
from app.utility_digitilization.models.tariff_detail_model import (
    TnbMalakoffTariffDetail,
)
from app.utility_digitilization.models.site_model import Site
from app.utility_digitilization.models.utility_provider_model import UtilityProvider
from app.utility_digitilization.utils.bill_calculation.bill_calculation_util import (
    get_bill_model,
    calculate_usage_off_peak_amount_rm,
    calculate_md_amount,
    calculate_icpt_rm,
    calculate_pf_penalty,
    calculate_kwtbb,
    calculate_usage_rm_amount,
    calculate_days,
    calculate_due_rm,
    calculate_total_due,
    calculate_usage_and_validate,
    calculate_total_bill,
    calculate_total_usage_kwh,
    calculate_total_amount_rm
)
from app.utility_digitilization.utils.conversions.convert_decimal import convert_float_to_decimal
from app.utility_digitilization.utils.date.date_util import parse_dates, parse_date
from app.utility_digitilization.utils.ocr_util.ocr_util import process_pdf
from decimal import Decimal
from app.common.utils.response_util.response_util import create_error_response
from typing import List, Optional
from datetime import date, datetime
import logging
import re
import uuid

router = APIRouter()

logger = logging.getLogger('uvicorn.error')


@router.get("/view/graph/{site_code}/{utility_provider_code}/", status_code=200)
async def view_bill_graph(
        site_code: str,
        utility_provider_code: str,
        from_date: str = None,
        to_date: str = None,
        db: Session = Depends(get_db)):
    """
    View bill details in graph format
    :param to_date:
    :param from_date:
    :param site_code:
    :param utility_provider_code:
    :param db:
    :return:
    """
    # validate params
    if not site_code:
        return JSONResponse(
            status_code=400,
            content={
                "code": 400,
                "message": "Site Code is required"
            }
        )

    if not utility_provider_code:
        return JSONResponse(
            status_code=400,
            content={
                "code": 400,
                "message": "Utility Provider Code is required"
            }
        )

    try:
        # Get all numeric/decimal fields from the TnbBillDetail model
        BillModel = get_bill_model(utility_provider_code)
        sum_expressions = [
            func.sum(getattr(BillModel.get('bill_detail'), field)).label(field)
            for field in inspect(BillModel.get('bill_detail')).c.keys()
            if isinstance(inspect(BillModel.get('bill_detail')).c[field].type, Numeric)
        ]

        # Query to get all Bill details
        query = (
            db.query(
                cast(func.extract('year', UtilityBill.bill_month_year), String).label('year'),
                func.extract('month', UtilityBill.bill_month_year).label('month'),
                func.sum(BillModel.get('bill_detail').total_usage_kwh).label('total_usage_kwh'),
                *sum_expressions
            )
            .join(UtilityAcct.site)
            .join(UtilityAcct.utility_provider)
            .filter(
                UtilityProvider.code == utility_provider_code,
                Site.site_code == site_code
            )
            .group_by(
                extract('month', UtilityBill.bill_month_year),
                extract('year', UtilityBill.bill_month_year),
            )
        )

        # Apply date filters if provided
        if from_date and to_date:
            from_date = parse_date(from_date)
            to_date = parse_date(to_date)
            query = query.filter(UtilityBill.bill_month_year.between(from_date, to_date))

        # Get the keys and values from the query, then convert the Decimal values to float
        keys = [column['name'] for column in query.column_descriptions]

        # Execute the query
        bill_query = query.all()

        # Convert Decimal values if present
        bill_query = [dict(zip(keys, row)) for row in bill_query]
        bill_query = convert_float_to_decimal(bill_query)

        # for the same year, make it nested dictionary
        year_array = []
        previous_year_bill = None
        for bill in bill_query:
            # calculate 'difference in kwh' from previous year
            if previous_year_bill:
                bill['differences_in_kwh_usage'] = bill['total_usage_kwh'] - previous_year_bill['total_usage_kwh']
            else:
                bill['differences_in_kwh_usage'] = 0

            # convert month (float) and year (string) to month-year string
            # convert month float to month name
            # cast month float to int
            bill['month'] = int(bill['month'])
            bill['month'] = date(1900, bill['month'], 1).strftime('%B')
            bill['month_year'] = f"{bill['month']} {bill['year']}"

            year_array.append(bill)
            previous_year_bill = bill

        return JSONResponse(
            status_code=200,
            content={
                "code": 200,
                "status": "success",
                "message": "Graph data retrieved successfully",
                "data": jsonable_encoder(bill_query)
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


@router.get("/view/{site_code}/{utility_provider_code}", status_code=200)
async def view_bill_details(
        site_code: str,
        utility_provider_code: str,
        db: Session = Depends(get_db)):
    """
    View bill details
    :return:
    """
    # validate params
    if not site_code:
        return JSONResponse(
            status_code=400,
            content={
                "code": 400,
                "message": "Site ID is required"
            }
        )

    if not utility_provider_code:
        return JSONResponse(
            status_code=400,
            content={
                "code": 400,
                "message": "Service Provider ID is required"
            }
        )

    try:
        # get bill detail model based on the provider code
        BillDetailModel = get_bill_model(utility_provider_code).get('bill_detail')
        if not BillDetailModel:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "message": "Invalid or unknown provider ID"
                }
            )

        # Query to get all Bill details
        bill_query = (
            db
            .query(BillDetailModel)
            .join(BillDetailModel.utility_acct)
            .join(UtilityAcct.site)
            .options(
                joinedload(BillDetailModel.utility_acct).joinedload(UtilityAcct.site)
            )
        )

        # if site_code is not "HQ", filter by site_code
        if site_code != "HQ":
            bill_query = bill_query.filter(Site.site_code == site_code)

        # Execute the query
        bill_query = bill_query.all()

        # Transform the results dynamically
        result = []
        for bill in bill_query:
            # Convert the main bill object to a dictionary
            bill_data = vars(bill) if hasattr(bill, '__dict__') else dict(bill)

            # Extract and flatten the utility_acct
            utility_acct_data = vars(bill.utility_acct) if bill.utility_acct and hasattr(bill.utility_acct,
                                                                                         '__dict__') else {}

            # Merge the utility_acct fields into the root level of bill_data
            bill_data.update(utility_acct_data)  # Unpack and merge utility_acct data

            # remove "utility_acct" key from the bill_data
            bill_data.pop('utility_acct', None)

            # Remove any SQLAlchemy-specific attributes (optional)
            bill_data.pop('_sa_instance_state', None)
            for key in utility_acct_data.keys():
                if '_sa_instance_state' in bill_data:
                    bill_data.pop('_sa_instance_state', None)

            bill_data['tariff'] = bill_data[get_bill_model(utility_provider_code).get('tariff_id')]
            bill_data['type'] = "Residential"
            bill_data['month'] = int_to_month_name(bill_data['month'])

            result.append(bill_data)

        return JSONResponse(
            status_code=200,
            content={
                "code": 200,
                "status": "success",
                "message": "Bill details retrieved successfully",
                "data": jsonable_encoder(result)
            }
        )
    except SQLAlchemyError as e:
        return create_error_response(
            status_code=500,
            message=f"Database Server Error, {e}",
        )

    except Exception as e:
        return create_error_response(
            status_code=500,
            message=f"Internal Server Error, {e}",
        )


@router.get(
    "/view/consolidate-graph/{site_code}/{utility_provider_code}",
    status_code=200
)
async def view_consolidate_bill_graph(
        site_code: str,
        utility_provider_code: str,
        from_date: str = None,
        to_date: str = None,
        db: Session = Depends(get_db)
):
    """
    View consolidated bill details in graph format
    :param site_code:
    :param utility_provider_code:
    :param from_date:
    :param to_date:
    :param db:
    """
    # validate params
    if not site_code:
        return JSONResponse(
            status_code=400,
            content={
                "code": 400,
                "message": "Site ID is required"
            }
        )

    if not utility_provider_code:
        return JSONResponse(
            status_code=400,
            content={
                "code": 400,
                "message": "Service Provider ID is required"
            }
        )

    try:
        # Get all numeric/decimal fields from the TnbBillDetail model
        BillModel = get_bill_model(utility_provider_code)
        sum_expressions = [
            func.sum(getattr(BillModel.get('bill_detail'), field)).label(field)
            for field in inspect(BillModel.get('bill_detail')).c.keys()
            if isinstance(inspect(BillModel.get('bill_detail')).c[field].type, Numeric)
        ]

        # Query to get all Bill details
        query = (
            db.query(
                cast(func.extract('year', UtilityBill.bill_month_year), String).label('year'),
                func.extract('month', UtilityBill.bill_month_year).label('month'),
                func.sum(BillModel.get('bill_detail').total_usage_kwh).label('total_usage_kwh'),
                *sum_expressions
            )
            .join(UtilityAcct.site)
            .join(UtilityAcct.utility_provider)
            .filter(
                UtilityProvider.code == utility_provider_code,
                # Site.site_code == site_code
            )
            .group_by(
                extract('month', UtilityBill.bill_month_year),
                extract('year', UtilityBill.bill_month_year),
            )
        )

        # Apply date filters if provided
        if from_date and to_date:
            from_date = parse_date(from_date)
            to_date = parse_date(to_date)
            query = query.filter(UtilityBill.bill_month_year.between(from_date, to_date))

        # Get the keys and values from the query, then convert the Decimal values to float
        keys = [column['name'] for column in query.column_descriptions]

        # Execute the query
        bill_query = query.all()

        # Convert Decimal values if present
        bill_query = [dict(zip(keys, row)) for row in bill_query]
        bill_query = convert_float_to_decimal(bill_query)

        # for the same year, make it nested dictionary
        year_array = []
        previous_year_bill = None
        for bill in bill_query:
            # calculate 'difference in kwh' from previous year
            if previous_year_bill:
                bill['differences_in_kwh_usage'] = bill['total_usage_kwh'] - previous_year_bill['total_usage_kwh']
            else:
                bill['differences_in_kwh_usage'] = 0

            # convert month (float) and year (string) to month-year string
            # convert month float to month name
            # cast month float to int
            bill['month'] = int(bill['month'])
            bill['month'] = date(1900, bill['month'], 1).strftime('%B')
            bill['month_year'] = f"{bill['month']} {bill['year']}"

            year_array.append(bill)
            previous_year_bill = bill

        return JSONResponse(
            status_code=200,
            content={
                "code": 200,
                "status": "success",
                "message": "Graph data retrieved successfully",
                "data": jsonable_encoder(bill_query)
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


@router.get("/view/consolidate/{site_code}/{utility_provider_code}/{tariff_id}/{account_number}", status_code=200)
async def view_consolidate_bill_details(
        site_code: str,
        utility_provider_code: str,
        tariff_id: str,
        account_number: str,
        db: Session = Depends(get_db)):
    """
    Show Consolidated bill details by site_code, utility_provider_code, tariff_id and account_number
    :param site_code:
    :param utility_provider_code:
    :param tariff_id:
    :param account_number:
    :param db:
    :return:
    """
    # validate params
    if not site_code:
        return JSONResponse(
            status_code=400,
            content={
                "code": 400,
                "message": "Site Code is required"
            }
        )

    if not utility_provider_code:
        return JSONResponse(
            status_code=400,
            content={
                "code": 400,
                "message": "Utility Provider Code is required"
            }
        )

    try:
        # get the account tariff ID foreign key based on the provider ID
        BillDetailModel = get_bill_model(utility_provider_code).get('bill_detail')
        if not BillDetailModel:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "status": "error",
                    "message": "Invalid or unknown provider ID"
                }
            )

        ACCOUNT_TARIFF_ID_FK = get_bill_model(utility_provider_code).get('acct_tariff_id_fk')
        if not ACCOUNT_TARIFF_ID_FK:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "status": "error",
                    "message": "Invalid or unknown provider ID"
                }
            )

        # Get all numeric/decimal fields from the bill model
        numeric_fields = [
            column.name for column in inspect(BillDetailModel).c
            if isinstance(column.type, Numeric)
        ]

        integer_fields = [
            column.name for column in inspect(BillDetailModel).c
            if isinstance(column.type, Integer)
        ]

        # Dynamically create the sum expressions
        sum_numeric_expressions = [func.sum(getattr(BillDetailModel, field)).label(field) for field in numeric_fields]
        sum_integer_expressions = [func.sum(getattr(BillDetailModel, field)).label(field) for field in integer_fields]

        # Query to get all accounts
        query = (
            db.query(
                ACCOUNT_TARIFF_ID_FK.label('tariff_id'),
                func.count(UtilityBill.utility_accts_id).label('count_id'),
                func.sum(UtilityAcct.deposit_rm).label('deposit_rm'),
                *sum_numeric_expressions,
                *sum_integer_expressions
            )
            .group_by(
                ACCOUNT_TARIFF_ID_FK,
            )
        )

        # if utility provider code is not "ALL", filter by utility provider code
        if utility_provider_code != "ALL":
            query = query.join(UtilityBill, UtilityBill.id == BillDetailModel.utility_bills_id)

        # if account number is provided, filter by account number
        if account_number != "ALL":
            query = query.filter(UtilityAcct.account_num == account_number)

        # if site code is not "HQ", filter by site code
        if site_code != "HQ":
            query = query.filter(Site.site_code == site_code)

        # if tariff ID is not "ALL", filter by tariff ID
        if tariff_id != "ALL":
            query = query.filter(ACCOUNT_TARIFF_ID_FK == tariff_id)

        # Execute the query
        accounts_query = query.all()

        # Get column names
        column_names = [desc['name'] for desc in query.column_descriptions]

        # Convert Decimal values if present
        account_dicts = [dict(zip(column_names, row)) for row in accounts_query]
        account_dicts = convert_float_to_decimal(account_dicts)

        if not accounts_query:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "status": "error",
                    "message": "No accounts found for the provided provider ID"
                }
            )

        # Transform the data to match the response format of `view_bill_graph`
        consolidated_data = []
        for account in account_dicts:
            try:
                # Ensure the month is an integer
                # account['month'] = int(account['month'])
                # # Skip if the month is not in the range 1-12
                # if 1 <= account['month'] <= 12:
                #     # Convert the month number to a name (optional)
                #     account['month_name'] = date(1900, account['month'], 1).strftime('%B')
                #     # Optional: Create a "month_year" field if needed
                #     account['month_year'] = f"{account['month_name']}"
                consolidated_data.append(account)
            except (ValueError, KeyError, TypeError):
                # Skip accounts with invalid month values or missing fields
                continue

        return JSONResponse(
            status_code=200,
            content={
                "code": 200,
                "status": "success",
                "message": "Consolidated data retrieved successfully",
                "data": jsonable_encoder(consolidated_data)
            }
        )

    except SQLAlchemyError as e:
        return create_error_response(
            status_code=500,
            message=f"Internal Server Error, {e}"
        )

    except Exception as e:
        return create_error_response(
            status_code=500,
            message=f"Internal Server Error, {e}"
        )


# upload file
@router.post("/add", status_code=201)
async def add_bill(
        file: UploadFile = File(...)
):
    """
    Add bill details
    :param file:
    :return:
    """
    try:
        content = await file.read()
        result = await process_pdf(content)
        return JSONResponse(
            status_code=201,
            content={
                "code": 201,
                "status": "success",
                "message": "Bill details added successfully",
                "data": result
            }
        )
    except re.error as regex_error:
        logger.error(f"Regex Error: {regex_error}")
        return JSONResponse(
            status_code=400,
            content={
                "code": 400,
                "status": "error",
                "message": f"Regex error: {regex_error}"
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


@router.post("/calculate", status_code=200)
async def upload_and_calculate_bill(
        utility_provider_code: str = Form(..., description="Provider code for the billing model"),
        month: Optional[str] = Form(None),
        account_no: Optional[str] = Form(None),
        contract_no: Optional[str] = Form(None),
        deposit: Optional[float] = Form(None),
        meter_no: Optional[str] = Form(None),
        type: Optional[str] = Form(None),
        invoice_no: Optional[str] = Form(None),
        tariff: Optional[str] = Form(None),
        bill_date: Optional[str] = Form(None),
        bill_period_to: Optional[str] = Form(None),
        current_reading_kwh: Optional[int] = Form(None),
        current_reading_off_peak_kwh: Optional[int] = Form(None),
        md_usage: Optional[int] = Form(None),
        pf: Optional[Decimal] = Form(None),
        lf: Optional[Decimal] = Form(None),
        late_payment_charge_rm: Optional[Decimal] = Form(None),
        monthly_minimum_charges_rm: Optional[Decimal] = Form(None),
        clc_amount: Optional[Decimal] = Form(None),
        adjustment_or_discount_rm: Optional[Decimal] = Form(None),
        rounding_rm: Optional[Decimal] = Form(None),
        arrears_rm: Optional[Decimal] = Form(None),
        date_of_last_payment: Optional[str] = Form(None),
        amount_of_last_payment_rm: Optional[Decimal] = Form(None),
        file: Optional[UploadFile] = File(None),
        db: Session = Depends(get_db)
):
    """
    Upload and calculate bill details for TNB
    :param clc_amount:
    :param month:
    :param account_no:
    :param contract_no:
    :param deposit:
    :param meter_no:
    :param type:
    :param invoice_no:
    :param tariff: e.g., tariff_B, tariff_C1
    :param bill_date:
    :param bill_period_to:
    :param current_reading_kwh:
    :param current_reading_off_peak_kwh:
    :param md_usage:
    :param pf:
    :param lf:
    :param late_payment_charge_rm:
    :param monthly_minimum_charges_rm:
    :param adjustment_or_discount_rm:
    :param rounding_rm:
    :param arrears_rm:
    :param date_of_last_payment:
    :param amount_of_last_payment_rm:
    :param file:
    :param db:
    :return:
    """

    def format_response_data(bill: TnbBillDetail, additional_data):
        data = {
            "invoice_no": bill.invoice_number,
            "bill_date": bill.bill_date.strftime("%Y-%m-%d"),
            "bill_period_from": bill.bill_period_from.strftime("%Y-%m-%d"),
            "bill_period_to": bill.bill_period_to.strftime("%Y-%m-%d"),
            "days": bill.days,
            "previous_reading_kwh": bill.prev_reading_kwh,
            "current_reading_kwh": bill.curr_reading_kwh,
            "peak_usage_kwh": bill.peak_usage_kwh,
            "peak_amount_rm": float(bill.peak_amount_rm),
            "non_peak_usage_kwh": bill.non_peak_usage_kwh,
            "non_peak_amount_rm": float(bill.non_peak_amount_rm),
            "total_usage_kwh": bill.total_usage_kwh,
            "total_amount_rm": float(bill.total_amount_rm),
            "max_demand": float(bill.max_demand),
            "max_demand_amount_rm": float(bill.max_demand_amount_rm),
            "icpt_amount_rm": float(bill.icpt_amount_rm),
            "clc_amount_rm": float(bill.clc_amount_rm),
            "kwtbb_rm": float(bill.kwtbb_rm),
            "power_factor": float(bill.power_factor),
            "power_factor_penalty_rm": float(bill.power_factor_penalty_rm),
            "load_factor_rm": float(bill.load_factor_rm),
            "late_payment_charge_rm": float(bill.late_payment_charge_rm),
            "discount_rm": float(bill.discount_rm),
            "current_due_rm": float(bill.current_due_rm),
            "rounding_rm": float(bill.rounding_rm),
            "total_due_rm": float(bill.total_due_rm),
            "date_of_last_payment": bill.date_of_last_payment.strftime("%Y-%m-%d"),
            "amount_of_last_payment_rm": float(bill.amount_of_last_payment_rm),
            "arrears_rm": float(bill.arrears_rm),
            "total_bill_rm": float(bill.total_bill_rm),
        }
        return {**additional_data, **data}

    if not month:
        return create_error_response(400, "Month is required")

    try:
        # Retrieve the billing models based on provider_id
        bill_model_info = get_bill_model(utility_provider_code)
        if not bill_model_info:
            return create_error_response(404, f"Provider with ID {utility_provider_code} not found")

        BillDetailModel = bill_model_info["bill_detail"]
        TariffRateModel = bill_model_info["tariff_rate"]
        TariffDetailModel = bill_model_info["tariff_detail"]
        AcctTariffFK = bill_model_info["acct_tariff_id_fk"]

        if file:
            content = await file.read()
            result = await process_pdf(content)
            return JSONResponse(
                status_code=201,
                content={
                    "code": 201,
                    "status": "success",
                    "message": "Bill details added successfully via file upload",
                    "data": result
                }
            )

        # if no file is uploaded, calculate bill details
        query_bill_info = (
            db.query(
                BillDetailModel.bill_period_from,
                BillDetailModel.prev_reading_kwh,
                BillDetailModel.non_peak_usage_kwh
            )
            .order_by(BillDetailModel.bill_date.desc())  # get the latest bill
            .first()  # get the first result
        )

        if not query_bill_info:
            return create_error_response(404, "Bill not found")

        # Get all tariff info needed
        query_tariff_info = (
            db.query(TariffDetailModel)
            .options(joinedload(TariffDetailModel.rates))
            .filter(TariffDetailModel.tariff_name == tariff)
            .all()
        )

        if not query_tariff_info:
            return create_error_response(404, f"Tariff with name {tariff} not found")

        # Check if there is a previous bill info
        bill_period_from, previous_reading, non_peak_usage_kwh = query_bill_info

        if not query_tariff_info:
            return create_error_response(404, "Tariff not found")

        tariff_config = query_tariff_info[0]
        bill_period_from = bill_period_from.strftime("%Y-%m-%d") if bill_period_from else None
        previous_reading = previous_reading or 0
        previous_reading_off_peak_kwh = non_peak_usage_kwh

        dates: dict = parse_dates({
            "bill_date": bill_date,
            "bill_period_to": bill_period_to,
            "date_of_last_payment": date_of_last_payment,
            "bill_period_from": bill_period_from
        })

        days: int = calculate_days(
            start_date=dates["bill_period_from"],
            end_date=dates["bill_period_to"]
        )

        usage_kwh: int = calculate_usage_and_validate(
            current_reading=current_reading_kwh,
            previous_reading=previous_reading
        )

        usage_off_peak_kwh: int = calculate_usage_and_validate(
            current_reading=current_reading_off_peak_kwh,
            previous_reading=previous_reading_off_peak_kwh
        )

        rates: List[dict] = [
            {
                "min_usage_kwh": rate.min_usage_kwh,
                "max_usage_kwh": rate.max_usage_kwh,
                "rate_sen_per_kwh": rate.rate_sen_per_kwh
            }
            for rate in tariff_config.rates
        ]

        off_peak_rate: Decimal = Decimal(str(tariff_config.off_peak))
        md_rate: Decimal = Decimal(str(tariff_config.md))
        icpt_rate: Decimal = Decimal(str(tariff_config.icpt))
        clc_low_pf_rate: Decimal = Decimal(str(tariff_config.clc))
        clc_high_pf_rate: Decimal = Decimal(str(tariff_config.clc))
        pf_penalty_rate = Decimal(str(tariff_config.pf_0_75))
        kwtbb_rate_percentage: Decimal = Decimal(str(tariff_config.kwtbb)) / 100
        tariff_name = str(tariff_config.tariff_name)

        # Replace dictionary-style access with variable names
        usage_amount_rm: Decimal = calculate_usage_rm_amount(
            rates=rates,
            usage_kwh=usage_kwh
        )

        usage_off_peak_amount_rm: Decimal = calculate_usage_off_peak_amount_rm(
            usage_off_peak_kwh=usage_off_peak_kwh,
            off_peak_rate=off_peak_rate
        )

        md_amount: Decimal = calculate_md_amount(
            md_usage=md_usage,
            md_rate=md_rate
        )

        icpt_amount_rm: Decimal = calculate_icpt_rm(
            usage=usage_kwh,
            usage_off_peak=usage_off_peak_kwh,
            icpt_rate=Decimal(icpt_rate)
        )

        pf_penalty_rm: Decimal = calculate_pf_penalty(
            pf=pf,
            usage_amount=usage_amount_rm,
            pf_penalty_rate=pf_penalty_rate
        )

        kwtbb_rm: Decimal = calculate_kwtbb(
            total_usage_amount=usage_amount_rm,
            kwtbb_rate=kwtbb_rate_percentage
        )

        due_rm: Decimal = calculate_due_rm(
            usage_amount=usage_amount_rm,
            usage_amount_off_peak=usage_off_peak_amount_rm,
            kwtbb=kwtbb_rm,
            md_amount=md_amount,
            icpt=icpt_amount_rm,
            clc_amount=clc_amount,
            pf_penalty=pf_penalty_rm
        )

        total_due_rm: Decimal = calculate_total_due(
            due=due_rm,
            late_payment_charge_rm=late_payment_charge_rm,
            rounding_rm=rounding_rm,
        )

        total_bill: Decimal = calculate_total_bill(
            total_due_rm=total_due_rm,
            arrears_rm=arrears_rm
        )

        total_usage_kwh: int = calculate_total_usage_kwh(
            usage_kwh=usage_kwh,
            usage_off_peak_kwh=usage_off_peak_kwh
        )

        total_amount_rm: Decimal = calculate_total_amount_rm(
            usage_amount_rm=usage_amount_rm,
            usage_off_peak_amount_rm=usage_off_peak_amount_rm
        )

        new_bill: TnbBillDetail = TnbBillDetail(
            invoice_number=invoice_no,
            bill_date=dates["bill_date"],
            bill_period_from=dates["bill_period_from"],
            bill_period_to=dates["bill_period_to"],
            days=days,
            prev_reading_kwh=previous_reading,
            curr_reading_kwh=current_reading_kwh,
            peak_usage_kwh=usage_kwh,  # usage kwh
            peak_amount_rm=usage_amount_rm,  # usage amount
            non_peak_usage_kwh=usage_off_peak_kwh,
            non_peak_amount_rm=usage_off_peak_amount_rm,
            total_usage_kwh=total_usage_kwh,
            total_amount_rm=total_amount_rm,
            max_demand=Decimal(md_usage),
            max_demand_amount_rm=md_amount,
            icpt_amount_rm=icpt_amount_rm,
            clc_amount_rm=clc_amount,
            kwtbb_rm=kwtbb_rm,
            power_factor=Decimal(pf),
            power_factor_penalty_rm=pf_penalty_rm,
            load_factor_rm=Decimal(lf),
            late_payment_charge_rm=Decimal(late_payment_charge_rm),
            discount_rm=Decimal(adjustment_or_discount_rm),
            current_due_rm=due_rm,
            rounding_rm=Decimal(rounding_rm),
            total_due_rm=total_due_rm,
            date_of_last_payment=dates["date_of_last_payment"],
            amount_of_last_payment_rm=Decimal(amount_of_last_payment_rm),
            arrears_rm=Decimal(arrears_rm),
            total_bill_rm=total_bill
        )

        additional_data: dict = {
            "account_no": account_no,
            "contract_no": contract_no,
            "deposit": float(deposit),
            "meter_no": meter_no,
            "type": type,
            "previous_reading_off_peak_kwh": previous_reading_off_peak_kwh,
        }

        response_data: dict = format_response_data(
            bill=new_bill,
            additional_data=additional_data
        )

        return JSONResponse(
            status_code=200,
            content={
                "code": 200,
                "status": "success",
                "message": "Bill details calculated and stored successfully",
                "data": response_data
            }
        )
    except ValueError as ve:
        return create_error_response(
            400,
            str(ve)
        )
    except SQLAlchemyError as e:
        return create_error_response(
            500,
            f"Database Server Error: {str(e)}"
        )
    except Exception as e:
        return create_error_response(
            500,
            f"Internal Server Error: {str(e)}"
        )


@router.post("/submit", status_code=201)
async def submit_bill_details(
        utility_provider_code: str = Form(...),
        site_id: int = Form(...),
        account_num: str = Form(...),
        month: int = Form(...),
        contract_no: str = Form(...),
        deposit: float = Form(...),
        meter_no: str = Form(...),
        type: str = Form(...),
        previous_reading_off_peak_kwh: int = Form(...),
        invoice_no: str = Form(...),
        bill_date: str = Form(...),
        bill_period_from: str = Form(...),
        bill_period_to: str = Form(...),
        days: int = Form(...),
        previous_reading_kwh: int = Form(...),
        current_reading_kwh: int = Form(...),
        peak_usage_kwh: int = Form(...),
        peak_amount_rm: float = Form(...),
        non_peak_usage_kwh: int = Form(...),
        non_peak_amount_rm: float = Form(...),
        total_usage_kwh: int = Form(...),
        total_amount_rm: float = Form(...),
        max_demand: float = Form(...),
        max_demand_amount_rm: float = Form(...),
        icpt_amount_rm: float = Form(...),
        clc_amount_rm: float = Form(...),
        kwtbb_rm: float = Form(...),
        power_factor: float = Form(...),
        power_factor_penalty_rm: float = Form(...),
        load_factor_rm: float = Form(...),
        late_payment_charge_rm: float = Form(...),
        discount_rm: float = Form(...),
        current_due_rm: float = Form(...),
        rounding_rm: float = Form(...),
        total_due_rm: float = Form(...),
        date_of_last_payment: str = Form(...),
        amount_of_last_payment_rm: float = Form(...),
        arrears_rm: float = Form(...),
        total_bill_rm: float = Form(...),
        file: UploadFile = File(None),
        db: Session = Depends(get_db)
):
    """
    Submit bill details to the database
    """
    try:
        if file:
            content = await file.read()
        else:
            content = None

        # get utility account ID
        utility_account_id = db.query(UtilityAcct.id).filter(UtilityAcct.account_num == account_num).first()

        # convert utility account ID to int
        utility_account_id: int = utility_account_id[0] if utility_account_id else None

        # validate utility account ID
        if not utility_account_id:
            return JSONResponse(
                status_code=404,
                content={
                    "code": 404,
                    "status": "error",
                    "message": "Utility account not found",
                }
            )

        # Get the bill detail model based on the provider ID
        BillModel = get_bill_model(utility_provider_code)
        BillDetailModel = BillModel.get('bill_detail')

        if not BillDetailModel:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "message": "Invalid or unknown provider ID"
                }
            )

        bill_id = str(uuid.uuid4())
        bill = UtilityBill(
            id=bill_id,
            utility_accts_id=utility_account_id,
            bill_month_year=parse_date(bill_date)
        )

        # Add the bill to the session and commit to ensure it gets an ID
        db.add(bill)
        db.commit()
        db.refresh(bill)

        bill_detail_id = str(uuid.uuid4())
        new_bill_detail = BillDetailModel(
            id=bill_detail_id,
            month=month,
            site_id=site_id,
            utility_bills_id=bill_id,
            utility_accts_id=utility_account_id,
            invoice_number=invoice_no,
            bill_date=parse_date(bill_date),
            bill_period_from=parse_date(bill_period_from),
            bill_period_to=parse_date(bill_period_to),
            days=days,
            prev_reading_kwh=previous_reading_kwh,
            curr_reading_kwh=current_reading_kwh,
            peak_usage_kwh=peak_usage_kwh,
            peak_amount_rm=peak_amount_rm,
            non_peak_usage_kwh=non_peak_usage_kwh,
            non_peak_amount_rm=non_peak_amount_rm,
            total_usage_kwh=total_usage_kwh,
            total_amount_rm=total_amount_rm,
            max_demand=max_demand,
            max_demand_amount_rm=max_demand_amount_rm,
            icpt_amount_rm=icpt_amount_rm,
            clc_amount_rm=clc_amount_rm,
            kwtbb_rm=kwtbb_rm,
            power_factor=power_factor,
            power_factor_penalty_rm=power_factor_penalty_rm,
            load_factor_rm=load_factor_rm,
            late_payment_charge_rm=late_payment_charge_rm,
            discount_rm=discount_rm,
            current_due_rm=current_due_rm,
            rounding_rm=rounding_rm,
            total_due_rm=total_due_rm,
            date_of_last_payment=parse_date(date_of_last_payment),
            amount_of_last_payment_rm=amount_of_last_payment_rm,
            arrears_rm=arrears_rm,
            total_bill_rm=total_bill_rm
        )
        db.add(new_bill_detail)
        db.commit()

        return JSONResponse(
            status_code=201,
            content={
                "code": 201,
                "status": "success",
                "message": "Bill details submitted successfully"
            }
        )

    except SQLAlchemyError as e:
        db.rollback()
        return create_error_response(500, f"Database Server Error: {e}")

    except Exception as e:
        db.rollback()
        return create_error_response(500, f"Internal Server Error: {e}")
