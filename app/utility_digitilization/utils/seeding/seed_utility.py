from app.utility_digitilization.models.bill_detail_model import SeBillDetail
from app.utility_digitilization.models.utility_bill_model import UtilityBill
from app.utility_digitilization.models.utility_provider_model import UtilityProvider
from app.utility_digitilization.models.site_model import Site
from app.utility_digitilization.models.tariff_detail_model.tnb_malakoff_tariff_detail_model import (
    TnbMalakoffTariffDetail
)
from app.utility_digitilization.models.tariff_rate_model.tnb_malakoff_tariff_rate_model import TnbMalakoffTariffRate
from app.utility_digitilization.models.tariff_detail_model.saj_tariff_detail_model import SajTariffDetail
from app.utility_digitilization.models.tariff_rate_model.saj_tariff_rate_model import SajTariffRate
from app.utility_digitilization.models.tariff_detail_model.se_tariff_detail_model import SeTariffDetail
from app.utility_digitilization.models.tariff_rate_model.se_tariff_rate_model import SeTariffRate
from app.utility_digitilization.models.tariff_detail_model.kuching_tariff_detail_model import KuchingTariffDetail
from app.utility_digitilization.models.tariff_rate_model.kuching_tariff_rate_model import KuchingTariffRate
from app.utility_digitilization.models.tariff_detail_model.laku_bintulu_tariff_detail_model import \
    LakuBintuluTariffDetail
from app.utility_digitilization.models.tariff_rate_model.laku_bintulu_tariff_rate_model import LakuBintuluTariffRate
from app.utility_digitilization.models.utility_account_model import UtilityAcct
from app.utility_digitilization.models.bill_detail_model import (
    TnbBillDetail,
    MalakoffBillDetail,
    SeBillDetail,
    SajBillDetail,
    LakuBillDetail,
    KuchingWaterBillDetail,
    IwkBillDetail,
    TelecommunicationBillDetail
)
from datetime import date
from sqlalchemy.orm import Session
from typing import List, Dict
from app.common.utils.seeder_util.seeder_util import add_records_to_db
from datetime import date
from decimal import Decimal
import uuid

# Define site data separately
site_data = [
    {"id": 1, "site_name": "Puteri Cove Residence", "site_code": "PCR"},
    {"id": 2, "site_name": "Sri Pulai Perdana", "site_code": "SPP"},
    {"id": 3, "site_name": "East Ledang", "site_code": "ELG"},
    {"id": 4, "site_name": "Presint 8", "site_code": "PR8"},
    {"id": 5, "site_name": "Straits View Condominium", "site_code": "SVC"},
    {"id": 6, "site_name": "Salvation Army Malaysia", "site_code": "SAM"}
]

# Define utility providers data separately
utility_providers_data = [
    {"id": 1, "name": "Tenaga Nasional Berhad", "service_type": "Electricity", "code": "TNB"},
    {"id": 2, "name": "Malakoff", "service_type": "Electricity", "code": "MALA"},
    {"id": 3, "name": "Sarawak Energy", "service_type": "Electricity", "code": "SKE"},
    {"id": 4, "name": "Syarikat Air Johor", "service_type": "Water", "code": "SAJ"},
    {"id": 5, "name": "LAKU(Bintulu)", "service_type": "Water", "code": "LAKUB"},
    {"id": 6, "name": "Kuching Water", "service_type": "Water", "code": "KW"},
    {"id": 7, "name": "Indah Water Konsortium", "service_type": "Sewerage", "code": "IWK"},
    {"id": 8, "name": "Telecommunication", "service_type": "Telecommunication", "code": "TELECOM"}
]

# Sub-site data, (removed)
# sub_site_data = [
#     {"id": 1, "sub_site_name": "T1", "site_id": 1, "utility_providers_id": 1},
#     {"id": 2, "sub_site_name": "T2", "site_id": 1, "utility_providers_id": 1},
#     {"id": 3, "sub_site_name": "T3", "site_id": 1, "utility_providers_id": 1},
#     {"id": 4, "sub_site_name": "SOHO", "site_id": 1, "utility_providers_id": 1},
#     {"id": 5, "sub_site_name": "RETAIL", "site_id": 1, "utility_providers_id": 1},
#     {"id": 6, "sub_site_name": "PDD", "site_id": 1, "utility_providers_id": 1},
#     {"id": 7, "sub_site_name": "COMMON_AREA", "site_id": 1, "utility_providers_id": 1},
#     {"id": 8, "sub_site_name": "CLUBHOUSE", "site_id": 2, "utility_providers_id": 1},
#     {"id": 9, "sub_site_name": "MSB", "site_id": 2, "utility_providers_id": 1},
#     {"id": 10, "sub_site_name": "MAIN GUARD HOUSE", "site_id": 3, "utility_providers_id": 1},
#     {"id": 11, "sub_site_name": "FEEDER PILLAR PHASE 1 LEKIR", "site_id": 3, "utility_providers_id": 1},
#     # Continue adding entries following the structure up to 39...
#     {"id": 36, "sub_site_name": "Bintulu Corps", "site_id": 6, "utility_providers_id": 3},
#     {"id": 37, "sub_site_name": "Bintulu Quarters", "site_id": 6, "utility_providers_id": [3, 5]},
#     {"id": 38, "sub_site_name": "Kuching Children's Home", "site_id": 6, "utility_providers_id": [3, 5]},
#     {"id": 39, "sub_site_name": "Kuching Quarters", "site_id": 6, "utility_providers_id": "c"},
# ]


# Define tnb/malakoff tariff details
tnb_malakoff_tariff_details = [
    {"id": 1, "tariff_name": "tariff_B", "type": "Low Voltage Commercial Tariff", "min_amount": 7.20,
     "all_charge": 0.00,
     "all_incl_maintenance": 0.00, "all_excl_maintenance": 0.00, "md": 0.00, "md_peak": 0.00, "peak": 0.00,
     "off_peak": 0.00, "clc": 0.00, "icpt": 2.70, "kwtbb": 1.60, "disc": 0.00, "optr": 0.00, "pf_0_75": 3.00,
     "pf_0_85": 1.50},
    {"id": 2, "tariff_name": "tariff_C1", "type": "Medium Voltage General Commercial Tariff", "min_amount": 600.00,
     "all_charge": 36.50, "all_incl_maintenance": 0.00, "all_excl_maintenance": 0.00, "md": 30.30, "md_peak": 0.00,
     "peak": 0.00, "off_peak": 0.00, "clc": 8.50, "icpt": 16.00, "kwtbb": 1.60, "disc": 0.00, "optr": 20.00,
     "pf_0_75": 3.00, "pf_0_85": 1.50},
    {"id": 3, "tariff_name": "tariff_C2", "type": "Medium Voltage Peak/Off-Peak Commercial Tariff",
     "min_amount": 600.00, "all_charge": 0.00, "all_incl_maintenance": 0.00, "all_excl_maintenance": 0.00, "md": 0.00,
     "md_peak": 45.10, "peak": 36.50, "off_peak": 22.40, "clc": 8.50, "icpt": 16.00, "kwtbb": 1.60, "disc": 0.00,
     "optr": 0.00, "pf_0_75": 3.00, "pf_0_85": 1.50},
    {"id": 4, "tariff_name": "tariff_D", "type": "Low Voltage Industrial Tariff", "min_amount": 7.20,
     "all_charge": 0.00,
     "all_incl_maintenance": 0.00, "all_excl_maintenance": 0.00, "md": 0.00, "md_peak": 0.00, "peak": 0.00,
     "off_peak": 0.00, "clc": 0.00, "icpt": 2.70, "kwtbb": 1.60, "disc": 0.00, "optr": 0.00, "pf_0_75": 3.00,
     "pf_0_85": 1.50},
    {"id": 5, "tariff_name": "tariff_Ds", "type": "Special Industrial Tariff", "min_amount": 7.20, "all_charge": 42.70,
     "all_incl_maintenance": 0.00, "all_excl_maintenance": 0.00, "md": 0.00, "md_peak": 0.00, "peak": 0.00,
     "off_peak": 0.00, "clc": 0.00, "icpt": 0.00, "kwtbb": 1.60, "disc": 0.00, "optr": 0.00, "pf_0_75": 3.00,
     "pf_0_85": 1.50},
    {"id": 6, "tariff_name": "tariff_E1", "type": "Medium Voltage General Industrial Tariff", "min_amount": 600.00,
     "all_charge": 33.70, "all_incl_maintenance": 0.00, "all_excl_maintenance": 0.00, "md": 29.60, "md_peak": 0.00,
     "peak": 0.00, "off_peak": 0.00, "clc": 8.50, "icpt": 16.00, "kwtbb": 1.60, "disc": 0.00, "optr": 20.00,
     "pf_0_75": 3.00, "pf_0_85": 1.50},
    {"id": 7, "tariff_name": "tariff_E1s", "type": "Special Industrial Tariff", "min_amount": 600.00,
     "all_charge": 33.60,
     "all_incl_maintenance": 0.00, "all_excl_maintenance": 0.00, "md": 23.70, "md_peak": 0.00, "peak": 0.00,
     "off_peak": 0.00, "clc": 0.00, "icpt": 0.00, "kwtbb": 1.60, "disc": 0.00, "optr": 20.00, "pf_0_75": 3.00,
     "pf_0_85": 1.50},
    {"id": 8, "tariff_name": "tariff_E2", "type": "Medium Voltage Peak/Off-Peak Industrial Tariff",
     "min_amount": 600.00, "all_charge": 0.00, "all_incl_maintenance": 0.00, "all_excl_maintenance": 0.00, "md": 0.00,
     "md_peak": 37.00, "peak": 35.50, "off_peak": 21.90, "clc": 8.50, "icpt": 16.00, "kwtbb": 1.60, "disc": 0.00,
     "optr": 0.00, "pf_0_75": 3.00, "pf_0_85": 1.50},
    {"id": 9, "tariff_name": "tariff_E2s", "type": "Special Industrial Tariff", "min_amount": 600.00,
     "all_charge": 0.00,
     "all_incl_maintenance": 0.00, "all_excl_maintenance": 0.00, "md": 0.00, "md_peak": 32.90, "peak": 33.60,
     "off_peak": 19.10, "clc": 0.00, "icpt": 0.00, "kwtbb": 1.60, "disc": 0.00, "optr": 0.00, "pf_0_75": 3.00,
     "pf_0_85": 1.50},
    {"id": 10, "tariff_name": "tariff_E3", "type": "High Voltage Peak/Off-Peak Industrial Tariff", "min_amount": 600.00,
     "all_charge": 0.00, "all_incl_maintenance": 0.00, "all_excl_maintenance": 0.00, "md": 0.00, "md_peak": 35.50,
     "peak": 33.70, "off_peak": 20.20, "clc": 8.50, "icpt": 16.00, "kwtbb": 1.60, "disc": 0.00, "optr": 0.00,
     "pf_0_75": 3.00, "pf_0_85": 1.50},
    {"id": 11, "tariff_name": "tariff_F", "type": "Low Voltage Mining Tariff", "min_amount": 120.00,
     "all_charge": 38.10,
     "all_incl_maintenance": 0.00, "all_excl_maintenance": 0.00, "md": 0.00, "md_peak": 0.00, "peak": 0.00,
     "off_peak": 0.00, "clc": 16.00, "icpt": 1.60, "kwtbb": 25.00, "disc": 0.00, "optr": 3.00, "pf_0_75": 1.50,
     "pf_0_85": 1.50},
    {"id": 12, "tariff_name": "tariff_F1", "type": "Medium Voltage General Mining Tariff", "min_amount": 120.00,
     "all_charge": 31.30, "all_incl_maintenance": 0.00, "all_excl_maintenance": 0.00, "md": 21.10, "md_peak": 0.00,
     "peak": 0.00, "off_peak": 0.00, "clc": 8.50, "icpt": 16.00, "kwtbb": 1.60, "disc": 25.00, "optr": 0.00,
     "pf_0_75": 3.00, "pf_0_85": 1.50},
    {"id": 13, "tariff_name": "tariff_F2", "type": "Medium Voltage Peak/Off-Peak Mining Tariff", "min_amount": 120.00,
     "all_charge": 0.00, "all_incl_maintenance": 0.00, "all_excl_maintenance": 0.00, "md": 0.00, "md_peak": 29.80,
     "peak": 31.30, "off_peak": 17.20, "clc": 8.50, "icpt": 16.00, "kwtbb": 1.60, "disc": 25.00, "optr": 0.00,
     "pf_0_75": 3.00, "pf_0_85": 1.50},
    {"id": 14, "tariff_name": "tariff_G", "type": "Street Lighting Tariff", "min_amount": 7.20, "all_charge": 0.00,
     "all_incl_maintenance": 30.50, "all_excl_maintenance": 19.20, "md": 0.00, "md_peak": 0.00, "peak": 0.00,
     "off_peak": 0.00, "clc": 16.00, "icpt": 1.60, "kwtbb": 0.00, "disc": 0.00, "optr": 3.00, "pf_0_75": 1.50,
     "pf_0_85": 1.50},
    {"id": 15, "tariff_name": "tariff_G1", "type": "Neon & Floodlight Tariff", "min_amount": 7.20, "all_charge": 20.80,
     "all_incl_maintenance": 0.00, "all_excl_maintenance": 0.00, "md": 0.00, "md_peak": 0.00, "peak": 0.00,
     "off_peak": 0.00, "clc": 16.00, "icpt": 1.60, "kwtbb": 0.00, "disc": 0.00, "optr": 3.00, "pf_0_75": 1.50,
     "pf_0_85": 1.50},
    {"id": 16, "tariff_name": "tariff_H", "type": "Low Voltage Specific Agriculture Tariff", "min_amount": 7.20,
     "all_charge": 0.00, "all_incl_maintenance": 0.00, "all_excl_maintenance": 0.00, "md": 0.00, "md_peak": 0.00,
     "peak": 0.00, "off_peak": 0.00, "clc": 2.70, "icpt": 1.60, "kwtbb": 0.00, "disc": 0.00, "optr": 3.00,
     "pf_0_75": 1.50, "pf_0_85": 1.50},
    {"id": 17, "tariff_name": "tariff_H1", "type": "Medium Voltage General Specific Agriculture Tariff",
     "min_amount": 600.00, "all_charge": 35.10, "all_incl_maintenance": 0.00, "all_excl_maintenance": 0.00, "md": 30.30,
     "md_peak": 0.00, "peak": 0.00, "off_peak": 0.00, "clc": 8.50, "icpt": 2.70, "kwtbb": 1.60, "disc": 0.00,
     "optr": 0.00, "pf_0_75": 3.00, "pf_0_85": 1.50},
    {"id": 18, "tariff_name": "tariff_H2", "type": "Medium Voltage Peak/Off-Peak Specific Agriculture Tariff",
     "min_amount": 600.00, "all_charge": 0.00, "all_incl_maintenance": 0.00, "all_excl_maintenance": 0.00, "md": 0.00,
     "md_peak": 40.80, "peak": 36.50, "off_peak": 22.40, "clc": 8.50, "icpt": 2.70, "kwtbb": 1.60, "disc": 0.00,
     "optr": 0.00, "pf_0_75": 3.00, "pf_0_85": 1.50}
]

tnb_malakoff_tariff_rates = [
    {"id": 1, "tnb_tariff_id": 1, "tier_name": "0_200kWh", "min_usage_kwh": 0, "max_usage_kwh": 200,
     "rate_sen_per_kwh": 43.50},
    {"id": 2, "tnb_tariff_id": 1, "tier_name": ">201kWh", "min_usage_kwh": 201, "max_usage_kwh": 0,
     "rate_sen_per_kwh": 50.90},
    {"id": 3, "tnb_tariff_id": 4, "tier_name": "0_200kWh", "min_usage_kwh": 0, "max_usage_kwh": 200,
     "rate_sen_per_kwh": 38.00},
    {"id": 4, "tnb_tariff_id": 4, "tier_name": ">201kWh", "min_usage_kwh": 201, "max_usage_kwh": 0,
     "rate_sen_per_kwh": 44.10},
    {"id": 5, "tnb_tariff_id": 16, "tier_name": "0_200kWh", "min_usage_kwh": 0, "max_usage_kwh": 200,
     "rate_sen_per_kwh": 39.00},
    {"id": 6, "tnb_tariff_id": 16, "tier_name": ">201kWh", "min_usage_kwh": 201, "max_usage_kwh": 0,
     "rate_sen_per_kwh": 47.20}
]

# Define saj tariff details
saj_tariff_details = [
    {"id": 1, "tariff_name": "Domestic", "min_amount": 10.50, "average_rate": 0.00},
    {"id": 2, "tariff_name": "Religious institutions / Welfare Approved", "min_amount": 16.50, "average_rate": 1.65},
    {"id": 3, "tariff_name": "Domestic Bulk", "min_amount": 25.50, "average_rate": 2.55},
    {"id": 4, "tariff_name": "Non Domestic", "min_amount": 31.50, "average_rate": 0.00},
    {"id": 5, "tariff_name": "Shipping", "min_amount": 70.50, "average_rate": 7.05},
    {"id": 6, "tariff_name": "Water Treatment Company (Water Kiosk)", "min_amount": 50.00, "average_rate": 7.00}
]

saj_tariff_rates = [
    {"id": 1, "saj_tariff_id": 1, "tier_name": "0 m³ - 20 m³", "min_usage_m3": 0, "max_usage_m3": 20,
     "rate_rm_per_m3": 1.05},
    {"id": 2, "saj_tariff_id": 1, "tier_name": "21 m³ – 35 m³", "min_usage_m3": 21, "max_usage_m3": 35,
     "rate_rm_per_m3": 2.35},
    {"id": 3, "saj_tariff_id": 1, "tier_name": "> 35 m³", "min_usage_m3": 36, "max_usage_m3": 0,
     "rate_rm_per_m3": 3.15},
    {"id": 4, "saj_tariff_id": 4, "tier_name": "0 m³ – 35 m³", "min_usage_m3": 0, "max_usage_m3": 35,
     "rate_rm_per_m3": 3.15},
    {"id": 5, "saj_tariff_id": 4, "tier_name": "> 35 m³", "min_usage_m3": 36, "max_usage_m3": 0, "rate_rm_per_m3": 3.55}
]

# Define Sarawak Energy (SE) tariff details
se_tariff_details = [
    {
        "id": 1,
        "tariff_name": "tariff_C1",
        "type": "Commercial",
        "min_amount": 10.00,
        "all_rate": 0.00,
        "late_payment_charge": 1.00,
        "late_payment_surcharge": 10.00,
        "md": 0.00,
        "md_peak": 0.00,
        "peak_rate": 0.00,
        "off_peak_rate": 0.00,
        "clc": None,
        "icpt": None,
        "kwtbb": None,
        "disc": None,
        "optr": 3.00,
        "pf_0_75": 1.50,
        "pf_0_85": None
    },
    {
        "id": 2,
        "tariff_name": "tariff_C2",
        "type": "Commercial Demand",
        "min_amount": 16.00,
        "all_rate": 24.50,
        "late_payment_charge": 1.00,
        "late_payment_surcharge": 10.00,
        "md": 16.00,
        "md_peak": 0.00,
        "peak_rate": 0.00,
        "off_peak_rate": 0.00,
        "clc": None,
        "icpt": None,
        "kwtbb": None,
        "disc": None,
        "optr": 3.00,
        "pf_0_75": 1.50,
        "pf_0_85": None
    },
    {
        "id": 3,
        "tariff_name": "tariff_C3",
        "type": "Commercial Peak/Off-Peak Demand",
        "min_amount": 20.00,
        "all_rate": 0.00,
        "late_payment_charge": 1.00,
        "late_payment_surcharge": 10.00,
        "md": 0.00,
        "md_peak": 20.00,
        "peak_rate": 24.50,
        "off_peak_rate": 13.90,
        "clc": None,
        "icpt": None,
        "kwtbb": None,
        "disc": None,
        "optr": 3.00,
        "pf_0_75": 1.50,
        "pf_0_85": None
    },
    {
        "id": 4,
        "tariff_name": "tariff_D",
        "type": "Domestic",
        "min_amount": 5.00,
        "all_rate": 0.00,
        "late_payment_charge": 1.00,
        "late_payment_surcharge": 10.00,
        "md": 0.00,
        "md_peak": 0.00,
        "peak_rate": 0.00,
        "off_peak_rate": 0.00,
        "clc": None,
        "icpt": None,
        "kwtbb": None,
        "disc": None,
        "optr": 3.00,
        "pf_0_75": 1.50,
        "pf_0_85": None
    },
    {
        "id": 5,
        "tariff_name": "tariff_I1",
        "type": "Industrial",
        "min_amount": 10.00,
        "all_rate": 0.00,
        "late_payment_charge": 1.00,
        "late_payment_surcharge": 10.00,
        "md": 0.00,
        "md_peak": 0.00,
        "peak_rate": 0.00,
        "off_peak_rate": 0.00,
        "clc": None,
        "icpt": None,
        "kwtbb": None,
        "disc": None,
        "optr": 3.00,
        "pf_0_75": 1.50,
        "pf_0_85": None
    },
    {
        "id": 6,
        "tariff_name": "tariff_I2",
        "type": "Industrial Demand",
        "min_amount": 16.00,
        "all_rate": 21.70,
        "late_payment_charge": 1.00,
        "late_payment_surcharge": 10.00,
        "md": 16.00,
        "md_peak": 0.00,
        "peak_rate": 0.00,
        "off_peak_rate": 0.00,
        "clc": None,
        "icpt": None,
        "kwtbb": None,
        "disc": None,
        "optr": 3.00,
        "pf_0_75": 1.50,
        "pf_0_85": None
    },
    {
        "id": 7,
        "tariff_name": "tariff_I3",
        "type": "Industrial Peak/Off-Peak Demand",
        "min_amount": 20.00,
        "all_rate": 0.00,
        "late_payment_charge": 1.00,
        "late_payment_surcharge": 10.00,
        "md": 0.00,
        "md_peak": 20.00,
        "peak_rate": 22.90,
        "off_peak_rate": 13.90,
        "clc": None,
        "icpt": None,
        "kwtbb": None,
        "disc": None,
        "optr": 3.00,
        "pf_0_75": 1.50,
        "pf_0_85": None
    }
]

se_tariff_rates = [
    {"id": 1, "tier_name": "1-100", "min_usage_kwh": 1, "max_usage_kwh": 100, "rate_sen_per_kwh": 20.00,
     "se_tariff_id": 1},
    {"id": 2, "tier_name": "1-200", "min_usage_kwh": 1, "max_usage_kwh": 200, "rate_sen_per_kwh": 24.00,
     "se_tariff_id": 1},
    {"id": 3, "tier_name": "1-300", "min_usage_kwh": 1, "max_usage_kwh": 300, "rate_sen_per_kwh": 26.00,
     "se_tariff_id": 1},
    {"id": 4, "tier_name": "1-400", "min_usage_kwh": 1, "max_usage_kwh": 400, "rate_sen_per_kwh": 28.00,
     "se_tariff_id": 1},
    {"id": 5, "tier_name": "1-500", "min_usage_kwh": 1, "max_usage_kwh": 500, "rate_sen_per_kwh": 30.00,
     "se_tariff_id": 1},
    {"id": 6, "tier_name": "1-3000", "min_usage_kwh": 1, "max_usage_kwh": 3000, "rate_sen_per_kwh": 31.50,
     "se_tariff_id": 1},
    {"id": 7, "tier_name": "1-10000", "min_usage_kwh": 1, "max_usage_kwh": 10000, "rate_sen_per_kwh": 32.00,
     "se_tariff_id": 1},
    {"id": 8, "tier_name": "1-20000", "min_usage_kwh": 1, "max_usage_kwh": 20000, "rate_sen_per_kwh": 31.00,
     "se_tariff_id": 1},
    {"id": 9, "tier_name": "1->20000", "min_usage_kwh": 1, "max_usage_kwh": 0, "rate_sen_per_kwh": 30.00,
     "se_tariff_id": 1},
    {"id": 10, "tier_name": "1-100", "min_usage_kwh": 1, "max_usage_kwh": 100, "rate_sen_per_kwh": 18.00,
     "se_tariff_id": 4},
    {"id": 11, "tier_name": "1-150", "min_usage_kwh": 1, "max_usage_kwh": 150, "rate_sen_per_kwh": 18.00,
     "se_tariff_id": 4},
    {"id": 12, "tier_name": "1-200", "min_usage_kwh": 1, "max_usage_kwh": 200, "rate_sen_per_kwh": 22.00,
     "se_tariff_id": 4},
    {"id": 13, "tier_name": "1-300", "min_usage_kwh": 1, "max_usage_kwh": 300, "rate_sen_per_kwh": 25.00,
     "se_tariff_id": 4},
    {"id": 14, "tier_name": "1-400", "min_usage_kwh": 1, "max_usage_kwh": 400, "rate_sen_per_kwh": 27.00,
     "se_tariff_id": 4},
    {"id": 15, "tier_name": "1-500", "min_usage_kwh": 1, "max_usage_kwh": 500, "rate_sen_per_kwh": 29.50,
     "se_tariff_id": 4},
    {"id": 16, "tier_name": "1-700", "min_usage_kwh": 1, "max_usage_kwh": 700, "rate_sen_per_kwh": 30.00,
     "se_tariff_id": 4},
    {"id": 17, "tier_name": "1-800", "min_usage_kwh": 1, "max_usage_kwh": 800, "rate_sen_per_kwh": 30.50,
     "se_tariff_id": 4},
    {"id": 18, "tier_name": "1-1300", "min_usage_kwh": 1, "max_usage_kwh": 1300, "rate_sen_per_kwh": 31.00,
     "se_tariff_id": 4},
    {"id": 19, "tier_name": ">1300", "min_usage_kwh": 1300, "max_usage_kwh": 0, "rate_sen_per_kwh": 31.50,
     "se_tariff_id": 4},
    {"id": 20, "tier_name": "1-100", "min_usage_kwh": 1, "max_usage_kwh": 100, "rate_sen_per_kwh": 24.00,
     "se_tariff_id": 5},
    {"id": 21, "tier_name": "1-3000", "min_usage_kwh": 1, "max_usage_kwh": 3000, "rate_sen_per_kwh": 25.00,
     "se_tariff_id": 5},
    {"id": 22, "tier_name": "1->3000", "min_usage_kwh": 1, "max_usage_kwh": 0, "rate_sen_per_kwh": 26.00,
     "se_tariff_id": 5},
]

# Define Kuching Water
kuching_tariff_details = [
    {"id": 1, "tariff_name": "Domestic Rate", "min_amount": 4.40, "average_rate": 0.00},
    {"id": 2, "tariff_name": "Domestic/ Commercial Rate", "min_amount": 18.70, "average_rate": 0.00},
    {"id": 3, "tariff_name": "Commercial Rate", "min_amount": 22.00, "average_rate": 0.00},
    {"id": 4, "tariff_name": "Special Commercial Rate For Water Processed for Sale", "min_amount": 27.50,
     "average_rate": 0.00},
    {"id": 5, "tariff_name": "Public Standpipes", "min_amount": 0.00, "average_rate": 0.43},
    {"id": 6, "tariff_name": "Water Collected at Depot (Customer’s Transport)", "min_amount": 0.00,
     "average_rate": 0.43},
    {"id": 7, "tariff_name": "Water to Ships", "min_amount": 0.00, "average_rate": 1.70},
]

kuching_tariff_rates = [
    {"id": 1, "tier_name": "1000l-15000l", "min_usage_l": 1000, "max_usage_l": 15000, "rate_rm_per_1000l": 0.48,
     "kuching_tariff_details_id": 1},
    {"id": 2, "tier_name": "15000l-50000l", "min_usage_l": 15000, "max_usage_l": 50000, "rate_rm_per_1000l": 0.72,
     "kuching_tariff_details_id": 1},
    {"id": 3, "tier_name": "> 50000l", "min_usage_l": 50000, "max_usage_l": 0, "rate_rm_per_1000l": 0.76,
     "kuching_tariff_details_id": 1},
    {"id": 4, "tier_name": "1000l-25000l", "min_usage_l": 1000, "max_usage_l": 25000, "rate_rm_per_1000l": 0.83,
     "kuching_tariff_details_id": 2},
    {"id": 5, "tier_name": ">25000l", "min_usage_l": 25000, "max_usage_l": 0, "rate_rm_per_1000l": 0.95,
     "kuching_tariff_details_id": 2},
    {"id": 6, "tier_name": "1000l-25000l", "min_usage_l": 1000, "max_usage_l": 25000, "rate_rm_per_1000l": 0.97,
     "kuching_tariff_details_id": 3},
    {"id": 7, "tier_name": ">25000l", "min_usage_l": 25000, "max_usage_l": 0, "rate_rm_per_1000l": 1.06,
     "kuching_tariff_details_id": 3},
    {"id": 8, "tier_name": "1000l-25000l", "min_usage_l": 1000, "max_usage_l": 25000, "rate_rm_per_1000l": 1.21,
     "kuching_tariff_details_id": 4},
    {"id": 9, "tier_name": ">25000l", "min_usage_l": 25000, "max_usage_l": 0, "rate_rm_per_1000l": 1.33,
     "kuching_tariff_details_id": 4},
]

# Define Laku (Bintulu)
laku_bintulu_tariff_details = [
    {"id": 1, "tariff_name": "Domestic Rate(W1)", "min_amount": 6.60, "average_rate": 0.00},
    {"id": 2, "tariff_name": "Domestic/ Commercial Rate(W2)", "min_amount": 18.70, "average_rate": 0.00},
    {"id": 3, "tariff_name": "Commercial Rate(W3)", "min_amount": 20.90, "average_rate": 0.00},
    {"id": 4, "tariff_name": "Industrial Rate(W4)", "min_amount": 24.20, "average_rate": 0.00},
    {"id": 5, "tariff_name": "Special Commercial Rate(W5)", "min_amount": 27.50, "average_rate": 0.00},
    {"id": 6, "tariff_name": "Schools(W6)", "min_amount": 0.00, "average_rate": 0.66},
    {"id": 7, "tariff_name": "Public Standpipes(W7)", "min_amount": 0.00, "average_rate": 0.36},
    {"id": 8, "tariff_name": "Water to Ships(W8)", "min_amount": 0.00, "average_rate": 1.70},
]

laku_bintulu_tariff_rates = [
    {"id": 1, "tier_name": "1-14000", "min_usage_l": 1, "max_usage_l": 14000, "rate_rm_per_1000l": 0.00,
     "laku_bintulu_tariff_details_id": 1},
    {"id": 2, "tier_name": "14000-45000", "min_usage_l": 14000, "max_usage_l": 45000, "rate_rm_per_1000l": 0.61,
     "laku_bintulu_tariff_details_id": 1},
    {"id": 3, "tier_name": ">45000", "min_usage_l": 45000, "max_usage_l": 0, "rate_rm_per_1000l": 0.66,
     "laku_bintulu_tariff_details_id": 1},
    {"id": 4, "tier_name": "1-25000", "min_usage_l": 1, "max_usage_l": 25000, "rate_rm_per_1000l": 0.83,
     "laku_bintulu_tariff_details_id": 2},
    {"id": 5, "tier_name": ">25000", "min_usage_l": 25000, "max_usage_l": 0, "rate_rm_per_1000l": 0.95,
     "laku_bintulu_tariff_details_id": 2},
    {"id": 6, "tier_name": "1-23000", "min_usage_l": 1, "max_usage_l": 23000, "rate_rm_per_1000l": 0.00,
     "laku_bintulu_tariff_details_id": 3},
    {"id": 7, "tier_name": ">23000", "min_usage_l": 23000, "max_usage_l": 0, "rate_rm_per_1000l": 0.99,
     "laku_bintulu_tariff_details_id": 3},
    {"id": 8, "tier_name": "1-23000", "min_usage_l": 1, "max_usage_l": 23000, "rate_rm_per_1000l": 0.00,
     "laku_bintulu_tariff_details_id": 4},
    {"id": 9, "tier_name": ">23000", "min_usage_l": 23000, "max_usage_l": 0, "rate_rm_per_1000l": 1.21,
     "laku_bintulu_tariff_details_id": 4},
    {"id": 10, "tier_name": "1-25000", "min_usage_l": 1, "max_usage_l": 25000, "rate_rm_per_1000l": 1.21,
     "laku_bintulu_tariff_details_id": 5},
    {"id": 11, "tier_name": ">25000", "min_usage_l": 25000, "max_usage_l": 0, "rate_rm_per_1000l": 1.33,
     "laku_bintulu_tariff_details_id": 5},
]

# utility account (development only)
utility_acct_data = [
    {
        "id": 1,
        "site_id": 1,
        "account_num": "A12345678",
        "utility_provider_id": 1,
        "area_served": "Kuala Lumpur",
        "contract_num": "C1001",
        "meter_num": "M10001",
        "deposit_rm": 500.00,
        "tnb_malakoff_tariff_id": 1,
        "saj_tariff_id": None
    },
    {
        "id": 2,
        "site_id": 2,
        "account_num": "B23456789",
        "utility_provider_id": 2,
        "area_served": "Penang",
        "contract_num": "C2002",
        "meter_num": "M20002",
        "deposit_rm": 750.00,
        "tnb_malakoff_tariff_id": None,
        "saj_tariff_id": 2
    },
    {
        "id": 3,
        "site_id": 3,
        "account_num": "C34567890",
        "utility_provider_id": 3,
        "area_served": "Johor Bahru",
        "contract_num": "C3003",
        "meter_num": "M30003",
        "deposit_rm": 620.00,
        "tnb_malakoff_tariff_id": 3,
        "saj_tariff_id": 3
    },
    {
        "id": 4,
        "site_id": 4,
        "account_num": "D45678901",
        "utility_provider_id": 4,
        "area_served": "Shah Alam",
        "contract_num": "C4004",
        "meter_num": "M40004",
        "deposit_rm": 1000.00,
        "tnb_malakoff_tariff_id": None,
        "saj_tariff_id": None
    },
    {
        "id": 5,
        "site_id": 5,
        "account_num": "E56789012",
        "utility_provider_id": 5,
        "area_served": "Kuching",
        "contract_num": "C5005",
        "meter_num": "M50005",
        "deposit_rm": 870.00,
        "tnb_malakoff_tariff_id": None,
        "saj_tariff_id": 4
    },
    {
        "id": 6,
        "site_id": 1,
        "account_num": "E56789012",
        "utility_provider_id": 5,
        "area_served": "Sarawak",
        "contract_num": "C5005",
        "meter_num": "M50005",
        "deposit_rm": 870.00,
        "se_tariff_id": 1
    },
]

# bill (development only)
utility_bills = [
    {
        "id": "TNB1",  # Unique UUID for each record
        "utility_accts_id": 1,
        "uploaded_at": date(2023, 8, 1),
        "bill_month_year": date(2023, 7, 1),
        "file": 1  # Replace with actual blob or identifier for the file
    },
    {
        "id": "TNB2",
        "utility_accts_id": 1,
        "uploaded_at": date(2023, 9, 1),
        "bill_month_year": date(2023, 8, 1),
        "file": 2  # Replace with actual blob or identifier for the file
    },
    {
        "id": "TNB3",
        "utility_accts_id": 2,
        "uploaded_at": date(2023, 8, 15),
        "bill_month_year": date(2023, 7, 15),
        "file": 3  # Replace with actual blob or identifier for the file
    },
    {
        "id": "TNB4",
        "utility_accts_id": 2,
        "uploaded_at": date(2023, 10, 1),
        "bill_month_year": date(2023, 9, 1),
        "file": 4  # Replace with actual blob or identifier for the file
    },
    {
        "id": "TNB5",
        "utility_accts_id": 3,
        "uploaded_at": date(2023, 9, 1),
        "bill_month_year": date(2023, 8, 1),
        "file": 5  # Replace with actual blob or identifier for the file
    },
    {
        "id": "MALA1",
        "utility_accts_id": 6,
        "uploaded_at": date(2023, 10, 15),
        "bill_month_year": date(2023, 9, 15),
        "file": 6  # Replace with actual blob or identifier for the file
    },
]

# bill details (development only)
tnb_bill_detail_data = [
    {
        "id": "tnbbilldetail1",
        "site_id": 1,
        "utility_accts_id": 1,
        "utility_bills_id": "TNB1",
        "invoice_number": "INV001",
        "bill_date": "2024-01-01",
        "bill_period_from": "2023-12-01",
        "bill_period_to": "2023-12-31",
        "days": 31,
        "prev_reading_kwh": 1436,
        "curr_reading_kwh": 1436,
        "peak_usage_kwh": 250,
        "peak_amount_rm": 120.50,
        "non_peak_usage_kwh": 250,
        "non_peak_amount_rm": 80.75,
        "total_usage_kwh": 500,
        "total_amount_rm": 201.25,
        "max_demand": 75.00,
        "max_demand_amount_rm": 15.00,
        "icpt_amount_rm": -5.00,
        "clc_amount_rm": 0.00,
        "kwtbb_rm": 3.00,
        "power_factor": 0.95,
        "power_factor_penalty_rm": 0.00,
        "load_factor_rm": 0.00,
        "late_payment_charge_rm": 0.00,
        "discount_rm": -10.00,
        "rounding_rm": 0.75,
        "current_due_rm": 201.25,
        "total_due_rm": 192.00,
        "date_of_last_payment": "2023-12-15",
        "amount_of_last_payment_rm": 190.00,
        "arrears_rm": 0.00,
        "total_bill_rm": 201.25,
        "usage": 500,
        "usage_incl_maintenance": 510,
        "usage_excl_maintenance": 500,
        "amount_rm": 201.25,
        "amount_incl_maintenance_rm": 205.00,
        "amount_excl_maintenance_rm": 201.25,
        "min_monthly_charge_rm": 20.00,
        "month": 12
    },
    {
        "id": "tnbbilldetail2",
        "site_id": 1,
        "utility_accts_id": 1,
        "utility_bills_id": "TNB2",
        "invoice_number": "INV001",
        "bill_date": "2024-01-01",
        "bill_period_from": "2023-12-01",
        "bill_period_to": "2023-12-31",
        "days": 31,
        "prev_reading_kwh": 1436,
        "curr_reading_kwh": 1436,
        "peak_usage_kwh": 250,
        "peak_amount_rm": 120.50,
        "non_peak_usage_kwh": 250,
        "non_peak_amount_rm": 80.75,
        "total_usage_kwh": 500,
        "total_amount_rm": 201.25,
        "max_demand": 75.00,
        "max_demand_amount_rm": 15.00,
        "icpt_amount_rm": -5.00,
        "clc_amount_rm": 0.00,
        "kwtbb_rm": 3.00,
        "power_factor": 0.95,
        "power_factor_penalty_rm": 0.00,
        "load_factor_rm": 0.00,
        "late_payment_charge_rm": 0.00,
        "discount_rm": -10.00,
        "current_due_rm": 201.25,
        "rounding_rm": 0.75,
        "total_due_rm": 192.00,
        "date_of_last_payment": "2023-12-15",
        "amount_of_last_payment_rm": 190.00,
        "arrears_rm": 0.00,
        "total_bill_rm": 201.25,
        "usage": 500,
        "usage_incl_maintenance": 510,
        "usage_excl_maintenance": 500,
        "amount_rm": 201.25,
        "amount_incl_maintenance_rm": 205.00,
        "amount_excl_maintenance_rm": 201.25,
        "min_monthly_charge_rm": 20.00,
        "month": 12
    },
    {
        "id": "tnbbilldetail3",
        "site_id": 1,
        "utility_accts_id": 1,
        "utility_bills_id": "TNB3",
        "invoice_number": "INV001",
        "bill_date": "2024-01-01",
        "bill_period_from": "2023-12-01",
        "bill_period_to": "2023-12-31",
        "days": 31,
        "prev_reading_kwh": 1436,
        "curr_reading_kwh": 1436,
        "peak_usage_kwh": 250,
        "peak_amount_rm": 120.50,
        "non_peak_usage_kwh": 250,
        "non_peak_amount_rm": 80.75,
        "total_usage_kwh": 500,
        "total_amount_rm": 201.25,
        "max_demand": 75.00,
        "max_demand_amount_rm": 15.00,
        "icpt_amount_rm": -5.00,
        "clc_amount_rm": 0.00,
        "kwtbb_rm": 3.00,
        "power_factor": 0.95,
        "power_factor_penalty_rm": 0.00,
        "load_factor_rm": 0.00,
        "late_payment_charge_rm": 0.00,
        "discount_rm": -10.00,
        "current_due_rm": 201.25,
        "rounding_rm": 0.75,
        "total_due_rm": 192.00,
        "date_of_last_payment": "2023-12-15",
        "amount_of_last_payment_rm": 190.00,
        "arrears_rm": 0.00,
        "total_bill_rm": 201.25,
        "usage": 500,
        "usage_incl_maintenance": 510,
        "usage_excl_maintenance": 500,
        "amount_rm": 201.25,
        "amount_incl_maintenance_rm": 205.00,
        "amount_excl_maintenance_rm": 201.25,
        "min_monthly_charge_rm": 20.00,
        "month": 12
    }
]

# bill details (development only)
mala_bill_detail_data = [
    {
        "id": 1,
        "site_id": 1,
        "utility_accts_id": 1,
        "utility_bills_id": 2,
        "invoice_number": "INV001",
        "bill_date": "2024-01-01",
        "bill_period_from": "2023-12-01",
        "bill_period_to": "2023-12-31",
        "days": 31,
        "prev_reading_kwh": 521436,
        "curr_reading_kwh": 521436,
        "peak_usage_kwh": 250,
        "peak_amount_rm": 120.50,
        "non_peak_usage_kwh": 250,
        "non_peak_amount_rm": 80.75,
        "total_usage_kwh": 500,
        "total_amount_rm": 201.25,
        "max_demand": 75.00,
        "max_demand_amount_rm": 15.00,
        "icpt_amount_rm": -5.00,
        "clc_amount_rm": 0.00,
        "kwtbb_rm": 3.00,
        "power_factor": 0.95,
        "power_factor_penalty_rm": 0.00,
        "load_factor_rm": 0.00,
        "late_payment_charge_rm": 0.00,
        "discount_rm": -10.00,
        "current_due_rm": 201.25,
        "rounding_rm": 0.75,
        "total_due_rm": 192.00,
        "date_of_last_payment": "2023-12-15",
        "amount_of_last_payment_rm": 190.00,
        "arrears_rm": 0.00,
        "total_bill_rm": 201.25,
        "usage": 500,
        "usage_incl_maintenance": 510,
        "usage_excl_maintenance": 500,
        "amount_rm": 201.25,
        "amount_incl_maintenance_rm": 205.00,
        "amount_excl_maintenance_rm": 201.25,
        "min_monthly_charge_rm": 20.00,
        "month": 12
    },
    {
        "id": 2,
        "site_id": 1,
        "utility_accts_id": 1,
        "utility_bills_id": 2,
        "invoice_number": "INV001",
        "bill_date": "2024-01-01",
        "bill_period_from": "2023-12-01",
        "bill_period_to": "2023-12-31",
        "days": 31,
        "prev_reading_kwh": 521436,
        "curr_reading_kwh": 521436,
        "peak_usage_kwh": 250,
        "peak_amount_rm": 120.50,
        "non_peak_usage_kwh": 250,
        "non_peak_amount_rm": 80.75,
        "total_usage_kwh": 500,
        "total_amount_rm": 201.25,
        "max_demand": 75.00,
        "max_demand_amount_rm": 15.00,
        "icpt_amount_rm": -5.00,
        "clc_amount_rm": 0.00,
        "kwtbb_rm": 3.00,
        "power_factor": 0.95,
        "power_factor_penalty_rm": 0.00,
        "load_factor_rm": 0.00,
        "late_payment_charge_rm": 0.00,
        "discount_rm": -10.00,
        "current_due_rm": 201.25,
        "rounding_rm": 0.75,
        "total_due_rm": 192.00,
        "date_of_last_payment": "2023-12-15",
        "amount_of_last_payment_rm": 190.00,
        "arrears_rm": 0.00,
        "total_bill_rm": 201.25,
        "usage": 500,
        "usage_incl_maintenance": 510,
        "usage_excl_maintenance": 500,
        "amount_rm": 201.25,
        "amount_incl_maintenance_rm": 205.00,
        "amount_excl_maintenance_rm": 201.25,
        "min_monthly_charge_rm": 20.00,
        "month": 12
    },
    {
        "id": 3,
        "site_id": 1,
        "utility_accts_id": 1,
        "utility_bills_id": 2,
        "invoice_number": "INV001",
        "bill_date": "2024-01-01",
        "bill_period_from": "2023-12-01",
        "bill_period_to": "2023-12-31",
        "days": 31,
        "prev_reading_kwh": 521436,
        "curr_reading_kwh": 521436,
        "peak_usage_kwh": 250,
        "peak_amount_rm": 120.50,
        "non_peak_usage_kwh": 250,
        "non_peak_amount_rm": 80.75,
        "total_usage_kwh": 500,
        "total_amount_rm": 201.25,
        "max_demand": 75.00,
        "max_demand_amount_rm": 15.00,
        "icpt_amount_rm": -5.00,
        "clc_amount_rm": 0.00,
        "kwtbb_rm": 3.00,
        "power_factor": 0.95,
        "power_factor_penalty_rm": 0.00,
        "load_factor_rm": 0.00,
        "late_payment_charge_rm": 0.00,
        "discount_rm": -10.00,
        "current_due_rm": 201.25,
        "rounding_rm": 0.75,
        "total_due_rm": 192.00,
        "date_of_last_payment": "2023-12-15",
        "amount_of_last_payment_rm": 190.00,
        "arrears_rm": 0.00,
        "total_bill_rm": 201.25,
        "usage": 500,
        "usage_incl_maintenance": 510,
        "usage_excl_maintenance": 500,
        "amount_rm": 201.25,
        "amount_incl_maintenance_rm": 205.00,
        "amount_excl_maintenance_rm": 201.25,
        "min_monthly_charge_rm": 20.00,
        "month": 12
    }
]

se_bill_detail_data = [
    {
        "id": 1,
        "site_id": 1,
        "utility_accts_id": 1,
        "utility_bills_id": 2,
        "invoice_number": "SEINV001",
        "bill_date": "2024-01-01",
        "bill_period_from": "2023-12-01",
        "bill_period_to": "2023-12-31",
        "days": 31,
        "prev_reading_kwh": 521436,
        "curr_reading_kwh": 521436,
        "peak_usage_kwh": 250,
        "peak_amount_rm": 115.50,  # adjusted amount
        "non_peak_usage_kwh": 250,
        "non_peak_amount_rm": 90.75,  # adjusted amount
        "total_usage_kwh": 500,
        "total_amount_rm": 206.25,  # adjusted total amount
        "max_demand": 80.00,  # adjusted max demand
        "max_demand_amount_rm": 20.00,  # adjusted amount
        "icpt_amount_rm": -5.50,  # adjusted ICPT amount
        "clc_amount_rm": 1.50,  # added CLC amount
        "kwtbb_rm": 3.50,  # adjusted kwtbb
        "power_factor": 0.95,
        "power_factor_penalty_rm": 0.00,
        "load_factor_rm": 0.00,
        "late_payment_charge_rm": 0.00,
        "discount_rm": -12.00,  # adjusted discount
        "current_due_rm": 206.25,  # adjusted due amount
        "rounding_rm": 0.75,
        "total_due_rm": 196.50,  # adjusted total due
        "date_of_last_payment": "2023-12-15",
        "amount_of_last_payment_rm": 190.00,
        "arrears_rm": 0.00,
        "total_bill_rm": 206.25,  # adjusted total bill
        "usage": 500,
        "usage_incl_maintenance": 510,
        "usage_excl_maintenance": 500,
        "amount_rm": 206.25,  # adjusted amount
        "amount_incl_maintenance_rm": 210.00,  # adjusted amount
        "amount_excl_maintenance_rm": 206.25,  # adjusted amount
        "min_monthly_charge_rm": 20.00,
        "month": 12
    },
    {
        "id": 2,
        "site_id": 1,
        "utility_accts_id": 6,
        "utility_bills_id": 2,
        "invoice_number": "SEINV002",
        "bill_date": "2024-01-01",
        "bill_period_from": "2023-12-01",
        "bill_period_to": "2023-12-31",
        "days": 31,
        "prev_reading_kwh": 521436,
        "curr_reading_kwh": 521436,
        "peak_usage_kwh": 260,  # adjusted peak usage
        "peak_amount_rm": 120.00,  # adjusted peak amount
        "non_peak_usage_kwh": 240,  # adjusted non-peak usage
        "non_peak_amount_rm": 85.00,  # adjusted non-peak amount
        "total_usage_kwh": 500,
        "total_amount_rm": 210.00,  # adjusted total amount
        "max_demand": 78.00,  # adjusted max demand
        "max_demand_amount_rm": 18.00,  # adjusted amount
        "icpt_amount_rm": -6.00,  # adjusted ICPT amount
        "clc_amount_rm": 2.00,  # added CLC amount
        "kwtbb_rm": 4.00,  # adjusted kwtbb
        "power_factor": 0.94,  # adjusted power factor
        "power_factor_penalty_rm": 1.00,  # added power factor penalty
        "load_factor_rm": 0.00,
        "late_payment_charge_rm": 0.00,
        "discount_rm": -12.00,  # adjusted discount
        "current_due_rm": 210.00,  # adjusted due amount
        "rounding_rm": 0.50,  # adjusted rounding
        "total_due_rm": 201.00,  # adjusted total due
        "date_of_last_payment": "2023-12-15",
        "amount_of_last_payment_rm": 190.00,
        "arrears_rm": 0.00,
        "total_bill_rm": 210.00,  # adjusted total bill
        "usage": 500,
        "usage_incl_maintenance": 510,
        "usage_excl_maintenance": 500,
        "amount_rm": 210.00,  # adjusted amount
        "amount_incl_maintenance_rm": 214.00,  # adjusted amount
        "amount_excl_maintenance_rm": 210.00,  # adjusted amount
        "min_monthly_charge_rm": 20.00,
        "month": 12
    },
    {
        "id": 3,
        "site_id": 1,
        "utility_accts_id": 1,
        "utility_bills_id": 2,
        "invoice_number": "SEINV003",
        "bill_date": "2024-01-01",
        "bill_period_from": "2023-12-01",
        "bill_period_to": "2023-12-31",
        "days": 31,
        "prev_reading_kwh": 521436,
        "curr_reading_kwh": 521436,
        "peak_usage_kwh": 255,  # adjusted peak usage
        "peak_amount_rm": 118.00,  # adjusted peak amount
        "non_peak_usage_kwh": 245,  # adjusted non-peak usage
        "non_peak_amount_rm": 82.50,  # adjusted non-peak amount
        "total_usage_kwh": 500,
        "total_amount_rm": 200.50,  # adjusted total amount
        "max_demand": 76.00,  # adjusted max demand
        "max_demand_amount_rm": 17.50,  # adjusted amount
        "icpt_amount_rm": -5.25,  # adjusted ICPT amount
        "clc_amount_rm": 1.75,  # added CLC amount
        "kwtbb_rm": 3.25,  # adjusted kwtbb
        "power_factor": 0.96,  # adjusted power factor
        "power_factor_penalty_rm": 0.00,
        "load_factor_rm": 0.00,
        "late_payment_charge_rm": 0.00,
        "discount_rm": -11.50,  # adjusted discount
        "current_due_rm": 200.50,  # adjusted due amount
        "rounding_rm": 0.75,  # adjusted rounding
        "total_due_rm": 191.25,  # adjusted total due
        "date_of_last_payment": "2023-12-15",
        "amount_of_last_payment_rm": 190.00,
        "arrears_rm": 0.00,
        "total_bill_rm": 200.50,  # adjusted total bill
        "usage": 500,
        "usage_incl_maintenance": 510,
        "usage_excl_maintenance": 500,
        "amount_rm": 200.50,  # adjusted amount
        "amount_incl_maintenance_rm": 204.00,  # adjusted amount
        "amount_excl_maintenance_rm": 200.50,  # adjusted amount
        "min_monthly_charge_rm": 20.00,
        "month": 12
    }
]

saj_bill_detail_data = [
    {
        "id": 1,
        "site_id": 2,
        "utility_accts_id": 2,
        "utility_bills_id": 3,
        "invoice_number": "SAJINV001",
        "bill_date": "2023-12-01",
        "bill_period_from": "2023-11-01",
        "bill_period_to": "2023-11-30",
        "days": 30,
        "month": 11,
        "reading_m3": 1100,
        "prev_reading_m3": 1000,
        "curr_reading_m3": 1100,
        "usage_m3": 100,
        "sub_meter_usage_m3": None,
        "total_usage_rm": 105.00,
        "pf": None,
        "late_payment_rm": 0.00,
        "discount_rm": 0.00,
        "current_due_rm": 105.00,
        "total_due_rm": 105.00,
        "date_of_last_payment": "2023-11-15",
        "amount_of_last_payment_rm": 98.50,
        "arrears_rm": 0.00,
        "total_bill_rm": 105.00
    },
    {
        "id": 2,
        "site_id": 2,
        "utility_accts_id": 2,
        "utility_bills_id": 4,
        "invoice_number": "SAJINV002",
        "bill_date": "2024-01-01",
        "bill_period_from": "2023-12-01",
        "bill_period_to": "2023-12-31",
        "days": 31,
        "month": 12,
        "reading_m3": 1220,
        "prev_reading_m3": 1100,
        "curr_reading_m3": 1220,
        "usage_m3": 120,
        "sub_meter_usage_m3": None,
        "total_usage_rm": 126.00,
        "pf": None,
        "late_payment_rm": 0.00,
        "discount_rm": 0.00,
        "current_due_rm": 126.00,
        "total_due_rm": 126.00,
        "date_of_last_payment": "2023-12-15",
        "amount_of_last_payment_rm": 105.00,
        "arrears_rm": 0.00,
        "total_bill_rm": 126.00
    }
]

# Mock data for LakuBillDetail
laku_bill_detail_data = [
    {
        "id": 1,
        "site_id": 2,
        "utility_accts_id": 2,
        "utility_bills_id": 3,
        "invoice_number": "INV-1001",
        "month": 12,
        "days": 31,
        "bill_date": date(2024, 12, 1),
        "bill_period_from": date(2024, 11, 1),
        "bill_period_to": date(2024, 11, 30),
        "late_payment_charge_rm": Decimal("15.00"),
        "discount_rm": Decimal("10.00"),
        "arrears_rm": Decimal("50.00"),
        "rounding_rm": Decimal("0.50"),
        "total_bill_rm": Decimal("250.00"),
        "area_served": "Zone A",
        "category": "Residential",
        "account_number": "ACC-12345",
        "meter_no": "MTR-98765",
        "bill_no": "BL-56789",
        "usage_below_23000_litres": Decimal("18000.00"),
        "usage_above_23000_litres": Decimal("5000.00"),
        "amount_below_23000_litres": Decimal("100.00"),
        "amount_above_23000_litres": Decimal("50.00"),
        "meter_rent": Decimal("5.00"),
        "curr_reading": Decimal("25000.00"),
        "prev_reading": Decimal("20000.00"),
        "total_usage": Decimal("5000.00"),
        "minimum_charge": Decimal("20.00"),
        "current_due_rm": 201.25,
        "total_due_rm": 192.00,
        "date_of_last_payment": "2023-12-15",
        "amount_of_last_payment_rm": 190.00,
    },
    {
        "id": 2,
        "site_id": 2,
        "utility_accts_id": 2,
        "utility_bills_id": 3,
        "invoice_number": "INV-1002",
        "month": 11,
        "days": 30,
        "bill_date": date(2024, 11, 1),
        "bill_period_from": date(2024, 10, 1),
        "bill_period_to": date(2024, 10, 31),
        "late_payment_charge_rm": Decimal("10.00"),
        "discount_rm": Decimal("5.00"),
        "arrears_rm": Decimal("30.00"),
        "rounding_rm": Decimal("0.20"),
        "total_bill_rm": Decimal("150.00"),
        "area_served": "Zone B",
        "category": "Commercial",
        "account_number": "ACC-54321",
        "meter_no": "MTR-12345",
        "bill_no": "BL-98765",
        "usage_below_23000_litres": Decimal("20000.00"),
        "usage_above_23000_litres": Decimal("4000.00"),
        "amount_below_23000_litres": Decimal("120.00"),
        "amount_above_23000_litres": Decimal("40.00"),
        "meter_rent": Decimal("8.00"),
        "curr_reading": Decimal("24000.00"),
        "prev_reading": Decimal("19000.00"),
        "total_usage": Decimal("5000.00"),
        "minimum_charge": Decimal("25.00"),
        "current_due_rm": 201.25,
        "total_due_rm": 192.00,
        "date_of_last_payment": "2023-12-15",
        "amount_of_last_payment_rm": 190.00,
    }
]

# Mock data for IWKBillDetail
iwk_bill_detail_data = [
    {
        "id": 1,
        "site_id": 2,
        "utility_accts_id": 2,
        "utility_bills_id": 3,
        "invoice_number": "INV-1001",
        "month": 12,
        "days": 31,
        "bill_date": date(2024, 12, 1),
        "bill_period_from": date(2024, 11, 1),
        "bill_period_to": date(2024, 11, 30),
        "late_payment_charge_rm": Decimal("15.00"),
        "discount_rm": Decimal("10.00"),
        "arrears_rm": Decimal("50.00"),
        "rounding_rm": Decimal("0.50"),
        "total_bill_rm": Decimal("250.00"),
        "current_due_rm": 201.25,
        "total_due_rm": 192.00,
        "date_of_last_payment": "2023-12-15",
        "amount_of_last_payment_rm": 190.00,
        "reading_m3": Decimal("10.00"),
    },
    {
        "id": 2,
        "site_id": 2,
        "utility_accts_id": 2,
        "utility_bills_id": 3,
        "invoice_number": "INV-1001",
        "month": 12,
        "days": 31,
        "bill_date": date(2024, 12, 1),
        "bill_period_from": date(2024, 11, 1),
        "bill_period_to": date(2024, 11, 30),
        "late_payment_charge_rm": Decimal("15.00"),
        "discount_rm": Decimal("10.00"),
        "arrears_rm": Decimal("50.00"),
        "rounding_rm": Decimal("0.50"),
        "total_bill_rm": Decimal("250.00"),
        "current_due_rm": 201.25,
        "total_due_rm": 192.00,
        "date_of_last_payment": "2023-12-15",
        "amount_of_last_payment_rm": 190.00,
        "reading_m3": Decimal("10.00"),
    },
]


def seed_sites(db: Session, site_data: List[Dict]):
    add_records_to_db(db, Site, site_data, 'site_name')


def seed_utility_providers(db: Session, utility_providers_data: List[Dict]):
    add_records_to_db(db, UtilityProvider, utility_providers_data, 'name')


def seed_tariff_details(db: Session, tariff_data: List[Dict], model, unique_field: str):
    add_records_to_db(db, model, tariff_data, unique_field)


def seed_tariff_rates(db: Session, tariff_rate_data: List[Dict], model, unique_field: str):
    add_records_to_db(db, model, tariff_rate_data, unique_field)


def seed_utility_accts(db: Session, utility_acct_data: List[Dict]):
    add_records_to_db(db, UtilityAcct, utility_acct_data, 'account_num')


def seed_utility_bills(db: Session, utility_bills: List[Dict]):
    add_records_to_db(db, UtilityBill, utility_bills, 'id')


def seed_tnb_bill_details(db: Session, tnb_bill_detail_data: List[Dict]):
    add_records_to_db(db, TnbBillDetail, tnb_bill_detail_data, 'id')


def seed_malakoff_bill_details(db: Session, malakoff_bill_detail_data: List[Dict]):
    add_records_to_db(db, MalakoffBillDetail, malakoff_bill_detail_data, 'id')


def seed_se_bill_details(db: Session, se_bill_detail_data: List[Dict]):
    add_records_to_db(db, SeBillDetail, se_bill_detail_data, 'id')


def seed_saj_bill_details(db: Session, saj_bill_detail_data: List[Dict]):
    add_records_to_db(db, SajBillDetail, saj_bill_detail_data, 'id')


def seed_kuching_bill_details(db: Session, kuching_bill_detail_data: List[Dict]):
    add_records_to_db(db, KuchingBillDetail, kuching_bill_detail_data, 'id')


def seed_laku_bill_details(db: Session, laku_bill_detail_data: List[Dict]):
    add_records_to_db(db, LakuBillDetail, laku_bill_detail_data, 'id')


def seed_iwk_bill_details(db: Session, iwk_bill_detail_data: List[Dict]):
    add_records_to_db(db, IwkBillDetail, iwk_bill_detail_data, 'id')


def seed_all(db: Session, env):
    seed_sites(db, site_data)
    seed_utility_providers(db, utility_providers_data)
    seed_tariff_details(db, tnb_malakoff_tariff_details, TnbMalakoffTariffDetail, 'tariff_name')
    seed_tariff_rates(db, tnb_malakoff_tariff_rates, TnbMalakoffTariffRate, 'tier_name')
    seed_tariff_details(db, saj_tariff_details, SajTariffDetail, 'tariff_name')
    seed_tariff_rates(db, saj_tariff_rates, SajTariffRate, 'tier_name')
    seed_tariff_details(db, se_tariff_details, SeTariffDetail, 'tariff_name')
    seed_tariff_rates(db, se_tariff_rates, SeTariffRate, 'tier_name')
    seed_tariff_details(db, kuching_tariff_details, KuchingTariffDetail, 'tariff_name')
    seed_tariff_rates(db, kuching_tariff_rates, KuchingTariffRate, 'tier_name')
    seed_tariff_details(db, laku_bintulu_tariff_details, LakuBintuluTariffDetail, 'tariff_name')
    seed_tariff_rates(db, laku_bintulu_tariff_rates, LakuBintuluTariffRate, 'tier_name')

    if env == 'development':
        seed_utility_accts(db, utility_acct_data)
        seed_utility_bills(db, utility_bills)
        seed_tnb_bill_details(db, tnb_bill_detail_data)
        # seed_malakoff_bill_details(db, mala_bill_detail_data)
        # seed_se_bill_details(db, se_bill_detail_data)
        # seed_saj_bill_details(db, saj_bill_detail_data)
        # seed_laku_bill_details(db, laku_bill_detail_data)
        # # seed_kuching_bill_details(db, kuching_bill_detail_data)
        # seed_iwk_bill_details(db, iwk_bill_detail_data)
    else:
        print('Environment not supported for seeding data')
