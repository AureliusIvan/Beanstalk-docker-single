from pydantic import BaseModel, field_validator, Field, model_validator
from typing import Optional, List


class Account(BaseModel):
    utility_provider_id: int
    account_num: str = Field(..., min_length=1, description="Account number is required")
    tariff_id: int
    contract_num: Optional[str] = None
    meter_num: Optional[str] = None
    area_served: Optional[str] = None

    @field_validator("account_num")
    def validate_account_num(cls, value):
        if not value.strip():  # Ensure account_num is not empty or just whitespace
            raise ValueError("Account number is required.")
        return value


class AddUtilityAccountRequest(BaseModel):
    site_id: int
    account: List[Account]

    @model_validator(mode="before")
    def validate_single_tariff_per_account(cls, values):
        for account in values.get("account", []):
            tariff_id_keys = ["tnb_malakoff_tariff_id", "saj_tariff_id", "se_tariff_id", "laku_bintulu_tariff_id"]
            if sum(1 for key in tariff_id_keys if account.get(key) is not None) > 1:
                raise ValueError("Only one tariff ID should be provided per account.")
        return values
