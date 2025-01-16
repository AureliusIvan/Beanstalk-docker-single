from pydantic import BaseModel, Field, constr, condecimal, conint
from typing import Optional
from datetime import date
from fastapi import UploadFile, Form, File


class UploadAndCalculateBillRequest(BaseModel):
    """
    Request model for uploading and calculating bill as form data.
    """
    month: str = Form(..., description="Billing month")
    account_no: str = Form(..., description="Account number")
    contract_no: str = Form(..., description="Contract number")
    deposit: float = Form(..., description="Deposit amount")
    meter_no: str = Form(..., description="Meter number")
    type: str = Form(..., description="Bill type")
    invoice_no: str = Form(..., description="Invoice number")
    tariff: str = Form(..., description="Tariff type, e.g., tariff_B, tariff_C1")
    bill_date: date = Form(..., description="Bill date")
    bill_period_to: date = Form(..., description="End date of the billing period")
    current_reading_kwh: conint(ge=0) = Form(..., description="Current meter reading in kWh")
    current_reading_off_peak_kwh: conint(ge=0) = Form(..., description="Current off-peak meter reading in kWh")
    previous_reading_off_peak_kwh: conint(ge=0) = Form(..., description="Previous off-peak meter reading in kWh")
    md_declared: condecimal(gt=0) = Form(..., description="Maximum demand declared")
    pf: condecimal(ge=0, le=1) = Form(..., description="Power factor (0 to 1)")
    lf: condecimal(ge=0) = Form(..., description="Load factor")
    late_payment_charge_rm: condecimal(ge=0) = Form(..., description="Late payment charge in RM")
    monthly_minimum_charges_rm: condecimal(ge=0) = Form(..., description="Monthly minimum charges in RM")
    adjustment_or_discount_rm: condecimal(ge=0) = Form(..., description="Adjustment or discount in RM")
    rounding_rm: condecimal(ge=-1, le=1) = Form(..., description="Rounding adjustment in RM")
    arrears_rm: condecimal(ge=0) = Form(..., description="Arrears amount in RM")
    date_of_last_payment: date = Form(..., description="Date of the last payment")
    amount_of_last_payment_rm: condecimal(ge=0) = Form(..., description="Amount of the last payment in RM")
    file: Optional[UploadFile] = File(None, description="Optional uploaded file")
