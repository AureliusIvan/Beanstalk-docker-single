from .bill.bill_routes import router as bill_router
from .tariff_routes import router as tariff_router
from .utility_account_routes import router as utility_account_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(bill_router, tags=["Utility Digitilization"], prefix="/bill")
router.include_router(tariff_router, tags=["Utility Digitilization"], prefix="/tariff")
router.include_router(utility_account_router, tags=["Utility Digitilization"], prefix="/account")
