from typing import List, Union, Optional
from datetime import date
from decimal import Decimal, ROUND_UP
from typing import List, Union, Dict
from app.utility_digitilization.models.bill_detail_model import (
    TnbBillDetail,
    MalakoffBillDetail,
    SeBillDetail,
    SajBillDetail,
    LakuBillDetail,
    KuchingWaterBillDetail,
    IwkBillDetail,
    TelecommunicationBillDetail,
)
from app.utility_digitilization.models.tariff_rate_model import (
    TnbMalakoffTariffRate,
    SeTariffRate,
    SajTariffRate,
    LakuBintuluTariffRate,
    KuchingTariffRate,
    IwkTariffRate,
    TelecommunicationTariffRate,
)
from app.utility_digitilization.models.tariff_detail_model import (
    TnbMalakoffTariffDetail,
    SeTariffDetail,
    SajTariffDetail,
    LakuBintuluTariffDetail,
    KuchingTariffDetail,
    IwkTariffDetail,
    TelecommunicationTariffDetail,

)
from app.utility_digitilization.models.utility_account_model import UtilityAcct
from app.utility_digitilization.utils.seeding.seed_utility import utility_bills

BILL_MODELS = {
    "TNB": {
        "name": "Tenaga Nasional Berhad",
        "bill_detail": TnbBillDetail,
        "tariff_rate": TnbMalakoffTariffRate,
        "tariff_detail": TnbMalakoffTariffDetail,
        "acct_tariff_id_fk": UtilityAcct.tnb_malakoff_tariff_id,
        "tariff_id": "tnb_malakoff_tariff_id"
    },
    "MALA": {
        "name": "Malakoff",
        "bill_detail": MalakoffBillDetail,
        "tariff_rate": TnbMalakoffTariffRate,
        "tariff_detail": TnbMalakoffTariffDetail,
        "acct_tariff_id_fk": UtilityAcct.tnb_malakoff_tariff_id,
        "tariff_id": "tnb_malakoff_tariff_id"
    },
    "SKE": {
        "name": "Sarawak Energy",
        "bill_detail": SeBillDetail,
        "tariff_rate": SeTariffRate,
        "tariff_detail": SeTariffDetail,
        "acct_tariff_id_fk": UtilityAcct.se_tariff_id,
        "tariff_id": "se_tariff_id"
    },
    "SAJ": {
        "name": "Syarikat Air Johor",
        "bill_detail": SajBillDetail,
        "tariff_rate": SajTariffRate,
        "tariff_detail": SajTariffDetail,
        "acct_tariff_id_fk": UtilityAcct.saj_tariff_id,
        "tariff_id": "saj_tariff_id"
    },
    "LAKUB": {
        "name": "Laku Bintulu",
        "bill_detail": LakuBillDetail,
        "tariff_rate": LakuBintuluTariffRate,
        "tariff_detail": LakuBintuluTariffDetail,
        "acct_tariff_id_fk": UtilityAcct.laku_bintulu_tariff_id,
        "tariff_id": "laku_bintulu_tariff_id"
    },
    "KW": {
        "name": "Kuching Water",
        "bill_detail": KuchingWaterBillDetail,
        "tariff_rate": KuchingTariffRate,
        "tariff_detail": KuchingTariffDetail,
        "acct_tariff_id_fk": UtilityAcct.kuching_tariff_id,
        "tariff_id": "kuching_tariff_id"
    },
    "IWK": {
        "name": "Indah Water Konsortium",
        "bill_detail": IwkBillDetail,
        "tariff_rate": IwkTariffRate,
        "tariff_detail": IwkTariffDetail,
        "acct_tariff_id_fk": UtilityAcct.iwk_tariff_id,
        "tariff_id": "iwk_tariff_id"
    },
    "TELECOM": {
        "name": "Telecommunication",
        "bill_detail": TelecommunicationBillDetail,
        "tariff_rate": TelecommunicationTariffRate,
        "tariff_detail": TelecommunicationTariffDetail,
        "acct_tariff_id_fk": UtilityAcct.telecommunication_tariff_id,
        "tariff_id": "telecommunication_tariff_id"
    }
}


def get_bill_model(utility_provider_code: str) -> Union[None, dict]:
    """
    Get bill model based on the provider_id from BILL_MODELS.
    :param utility_provider_code: Utility Provider Code
    :return: Dict of bill model
    """
    bill_model = BILL_MODELS.get(utility_provider_code)
    if not bill_model:
        return None
    return bill_model


def calculate_usage_rm_amount(
        usage_kwh: Union[float, int],
        kwh_static_rate: Decimal = None,
        rates: List[Dict[str, int]] = None
) -> Decimal:
    """
   Calculate the total billing amount based on electricity usage and pricing tiers.

   This function computes the total billing amount either using a static rate or
   a tiered rate structure. Only one pricing method (static rate or tiered rates)
   can be applied at a time.

   Parameters:
       usage_kwh (Union[float, int]):
           The total electricity usage in kilowatt-hours (kWh). Must be non-negative.

       kwh_static_rate (Optional[Decimal]):
           A flat rate in sen per kWh. If provided, `rate_tiers` must not be used.

       rates (Optional[List[Dict[str, Union[int, Decimal]]]]):
           A list of dictionaries representing tiered pricing. Each dictionary should contain:
               - 'min_usage_kwh' (int): The minimum kWh for the tier (inclusive).
               - 'max_usage_kwh' (int): The maximum kWh for the tier (exclusive). Use 0 for no upper limit.
               - 'rate_sen_per_kwh' (Decimal): The rate in sen per kWh for this tier.
           Tiers should be ordered by ascending `min_usage_kwh`.

   Returns:
       Decimal:
           The total billing amount in the local currency, rounded to two decimal places.

   Raises:
       ValueError:
           - If both `kwh_static_rate` and `rates` are provided.
           - If `usage_kwh` is negative.
           - If neither `static_rate_sen_per_kwh` nor `rate_tiers` is provided.

   Example:
       >>> calculate_usage_rm_amount(
       ...     usage_kwh=250,
       ...     rates=[
       ...         {'min_usage_kwh': 0, 'max_usage_kwh': 100, 'rate_sen_per_kwh': Decimal('15.0')},
       ...         {'min_usage_kwh': 101, 'max_usage_kwh': 200, 'rate_sen_per_kwh': Decimal('20.0')},
       ...         {'min_usage_kwh': 201, 'max_usage_kwh': 0, 'rate_sen_per_kwh': Decimal('25.0')}
       ...     ]
       ... )
       Decimal('475.00')
   """
    # make sure either usage_kwh or kwh_static_rate that is passed
    if rates and kwh_static_rate:
        raise ValueError("rates and kwh_static_rate cannot be passed together.")

    # make sure rates types are list of dictionary
    if rates and not isinstance(rates, list):
        raise ValueError("Invalid rate format. Expected a list of dictionaries.")

    usage_kwh = Decimal(str(usage_kwh))  # Convert usage to Decimal for precision
    kwh_static_rate = kwh_static_rate  # Convert usage to Decimal for precision
    total_amount = Decimal('0')

    # validate usage
    if usage_kwh < 0:
        raise ValueError("Usage (RM) cannot be negative.")

    # Calculate the total amount based on the static rate
    if kwh_static_rate:  # Calculate the total amount based on the static rate
        return round(usage_kwh * kwh_static_rate / 100, 2)

    if not rates:  # Return 0 if no rates are provided
        return total_amount

    for rate in rates:  # Iterate through the rates and calculate the amount for each tier
        # check whether rate is instance of dict
        if not isinstance(rate, dict):
            raise ValueError(f"Invalid rate format. Expected a dictionary. Current format: {type(rate)}")
            # Extract the rate attributes and convert to Decimal
        min_usage: int = rate.get('min_usage_kwh', 0)
        max_usage: int = rate.get('max_usage_kwh', 0)
        rate_per_kwh: Decimal = Decimal(rate.get('rate_sen_per_kwh', 0)) / 100

        if Decimal(max_usage) == Decimal('0'):  # No upper limit, applies to all remaining usage
            if usage_kwh >= min_usage:
                total_amount += (
                        (
                                usage_kwh
                                # Subtract the minimum usage to get the applicable usage
                                # (fix the case where the usage is 201 and min_usage is 201, which then skips the tier, resulting in incorrect calculation)
                                - (min_usage - 1)
                        )
                        * rate_per_kwh
                )

        elif usage_kwh >= min_usage:
            # If usage is within the tier, calculate applicable usage
            applicable_usage = min(usage_kwh, Decimal(max_usage)) - min_usage
            total_amount += max(Decimal(0), applicable_usage) * rate_per_kwh

    # Apply rounding at the final step to avoid rounding errors in intermediate steps
    return round(total_amount, 2)  # Return the total rounded to two decimal places


def calculate_usage_off_peak_amount_rm(usage_off_peak_kwh, off_peak_rate) -> Decimal:
    """
    Calculate the off-peak amount based on the usage in kWh.
    :param usage_off_peak_kwh: Off-peak usage in kWh.
    :param off_peak_rate: Off-peak rate in RM per kWh.
    :return: Off-peak amount.
    """
    return round(Decimal(usage_off_peak_kwh) * Decimal(off_peak_rate), 2)


def calculate_md_amount(md_usage: int, md_rate: Decimal) -> Decimal:
    """
    Calculate the Maximum Demand amount based on the MD usage.
    :param md_usage: Maximum Demand usage in kW.
    :param md_rate: Rate for Maximum Demand in RM per kW.
    :return: MD amount
    """
    return round(Decimal(md_usage) * Decimal(md_rate), 2)


def calculate_icpt_rm(
        usage: int,
        icpt_rate: Decimal,  # in sen
        usage_off_peak: Optional[int] = 0
) -> Decimal:
    """
    Calculate the ICPT amount based on the total usage amount.
    :param usage: Total usage amount in kWh.
    :param usage_off_peak: Off-peak usage amount in kWh.
    :param icpt_rate: ICPT rate as a decimal percentage.
    :return: ICPT amount (Decimal, 2).

    Usage:
    >>> calculate_icpt_rm(100, Decimal('0.02'))
    Decimal('2.00')
    """
    # convert rate from sen to rm
    icpt_rate /= 100
    return round((usage + usage_off_peak) * Decimal(icpt_rate), 2)


def calculate_clc_percentage(
        pf: Union[float, Decimal],
        clc_low_pf_rate: Union[float, Decimal],
        clc_high_pf_rate: Union[float, Decimal]
) -> Decimal:
    """
    Calculate the Customer Load Control (CLC) percentage based on the Power Factor (PF).

    The CLC percentage is determined by the following criteria:

    - **PF between 0.75 (inclusive) and 0.85 (exclusive):**
        \[
        \text{CLC Percentage} = \left(\frac{0.85 - \text{PF}}{0.01}\right) \times \text{clc_low_pf_rate}
        \]

    - **PF below 0.75:**
        \[
        \text{CLC Percentage} = \left(\frac{0.75 - \text{PF}}{0.01}\right) \times \text{clc_high_pf_rate}
        \]

    - **PF of 0.85 or higher:**
        \[
        \text{CLC Percentage} = 0.00
        \]

    All calculations utilize the `Decimal` type to ensure precision in financial computations.

    Parameters:
        pf (Union[float, Decimal]):
            The Power Factor value. It should be a decimal between 0 and 1.

        clc_low_pf_rate (Union[float, Decimal]):
            The rate applied when the PF is between 0.75 (inclusive) and 0.85 (exclusive).

        clc_high_pf_rate (Union[float, Decimal]):
            The rate applied when the PF is below 0.75.

    Returns:
        Decimal:
            The calculated CLC percentage, rounded to two decimal places.

    Raises:
        ValueError:
            If `pf`, `clc_low_pf_rate`, or `clc_high_pf_rate` are outside expected ranges.
    """
    # Convert inputs to Decimal for precise arithmetic
    try:
        pf_decimal = Decimal(pf)
        clc_low_rate_decimal = Decimal(clc_low_pf_rate)
        clc_high_rate_decimal = Decimal(clc_high_pf_rate)
    except Exception as e:
        raise ValueError(f"Invalid input type: {e}")

    # Validate PF range
    if not (Decimal('0') <= pf_decimal <= Decimal('1')):
        raise ValueError("Power factor (pf) must be between 0 and 1.")

    if clc_low_rate_decimal < Decimal('0') or clc_high_rate_decimal < Decimal('0'):
        raise ValueError("CLC rates must be non-negative.")

    # Initialize CLC percentage
    clc_percentage = Decimal('0.00')

    if Decimal('0.75') <= pf_decimal < Decimal('0.85'):
        # Calculate CLC percentage for PF between 0.75 and 0.85
        adjustment_factor = (Decimal('0.85') - pf_decimal) / Decimal('0.01')
        clc_percentage = (adjustment_factor.quantize(Decimal('1.00'))) * clc_low_rate_decimal
    elif pf_decimal < Decimal('0.75'):
        # Calculate CLC percentage for PF below 0.75
        adjustment_factor = (Decimal('0.75') - pf_decimal) / Decimal('0.01')
        clc_percentage = (adjustment_factor.quantize(Decimal('1.00'))) * clc_high_rate_decimal
    # If PF >= 0.85, CLC percentage remains 0.00

    # Round the result to two decimal places
    return clc_percentage.quantize(Decimal('0.01'))


def calculate_clc_amount(clc_percentage, total_usage_amount):
    """
    Calculate the CLC amount based on the CLC percentage and total usage amount.
    :param clc_percentage: CLC percentage.
    :param total_usage_amount: Total usage amount.
    :return: CLC amount.
    """
    return round(clc_percentage * total_usage_amount)


def calculate_pf_penalty(pf, usage_amount, pf_penalty_rate):
    """
    Calculate the power factor penalty amount based on the power factor and usage amount.
    :param pf: Power factor.
    :param usage_amount: Total usage amount.
    :param pf_penalty_rate: Penalty rate for PF below 0.9.
    :return: PF penalty amount.
    """
    if pf < Decimal('0.90'):
        result = usage_amount * Decimal(pf_penalty_rate)
    else:
        result = Decimal('0.00')
    return round(result)


def calculate_kwtbb(
        total_usage_amount: Decimal,
        kwtbb_rate: Decimal
) -> Decimal:
    """
    Calculate the Kumpulan Wang Tenaga Boleh Baharu (KWTBB) amount based on the tariff and total usage amount.
    :param total_usage_amount: Total usage amount.
    :param kwtbb_rate: KWTBB rate as a decimal percentage.
    :return: KWTBB amount (Decimal, 2).
    """
    result = Decimal(total_usage_amount) * Decimal(kwtbb_rate)
    rounded_up = result.quantize(Decimal('0.01'), rounding=ROUND_UP)
    return rounded_up


def calculate_days(
        start_date: Union[date, str],
        end_date: Union[date, str]) -> int:
    """
    Calculate the number of days between two dates.
    :param start_date: Start date.
    :param end_date: End date.
    :return: Number of days.

    ``start_date`` and ``end_date`` can be either a date object or a string in the format 'YYYY-MM-DD'.
    """
    start_date = start_date if isinstance(start_date, date) else date.fromisoformat(start_date)
    end_date = end_date if isinstance(end_date, date) else date.fromisoformat(end_date)
    return abs((end_date - start_date).days)


def calculate_due_rm(
        usage_amount: Union[Decimal, float, int, str],
        usage_amount_off_peak: Union[Decimal, float, int, str],
        md_amount: Union[Decimal, float, int, str],
        icpt: Union[Decimal, float, int, str],
        clc_amount: Union[Decimal, float, int, str],
        pf_penalty: Union[Decimal, float, int, str],
        kwtbb: Union[Decimal, float, int, str]
) -> Decimal:
    """
    due = usage_amount + md_amount + icpt + clc_amount + pf_penalty - kwtbb
    :return:
    """
    # Convert to Decimal
    usage_amount = Decimal(usage_amount)
    usage_amount_off_peak = Decimal(usage_amount_off_peak)
    md_amount = Decimal(md_amount)
    icpt = Decimal(icpt)
    clc_amount = Decimal(clc_amount)
    pf_penalty = Decimal(pf_penalty)
    kwtbb = Decimal(kwtbb)
    return round(usage_amount + usage_amount_off_peak + md_amount + icpt + clc_amount + pf_penalty + kwtbb, 2)


def calculate_total_due(
        due: Decimal,
        late_payment_charge_rm: Decimal,
        rounding_rm: Decimal,
) -> Decimal:
    """
    Calculate the total due amount for a bill.
    :param due: Due amount.
    :param late_payment_charge_rm: Late payment charge in RM.
    :param rounding_rm: Rounding adjustment in RM.
    """
    total_bill = round(late_payment_charge_rm + due + rounding_rm, 2)
    return total_bill


def calculate_usage_and_validate(current_reading, previous_reading) -> int:
    """
    Calculate usage and validate the current readings
    `Formula: current_reading (KWH) - previous_reading (KWH)`
    :param current_reading:
    :param previous_reading:
    :return: usage_kwh
    """
    # cast to Decimal
    current_reading = int(round(current_reading))
    previous_reading = int(round(previous_reading))
    usage: int = current_reading - previous_reading
    return usage


def calculate_total_bill(
        total_due_rm: Decimal,
        arrears_rm: Decimal,
) -> Decimal:
    """
    Calculate the total bill amount.
    :param total_due_rm:
    :param arrears_rm:
    :return:
    """
    return round(total_due_rm + arrears_rm, 2)


def calculate_total_usage_kwh(
        usage_kwh: int,
        usage_off_peak_kwh: int):
    """
    Calculate total usage in kWh
    :return:
    """
    return usage_kwh + usage_off_peak_kwh


def calculate_total_amount_rm(
        usage_amount_rm,
        usage_off_peak_amount_rm
) -> Decimal:
    """
    Calculate total amount in RM
    :return:
    """
    return usage_amount_rm + usage_off_peak_amount_rm
