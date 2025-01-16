from fastapi import APIRouter

router = APIRouter()


@router.get("/test")
def test_utility():
    return {"router": "email"}
