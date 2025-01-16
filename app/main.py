from typing import Union
from fastapi import FastAPI
from app.email_whatsapp_AI.routers import email_router
from app.utility_digitilization.routers import router as utility_router

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# Email Whatsapp AI routers
app.include_router(email_router, prefix="/email", tags=["email"])


# Utility Digitilization routers
app.include_router(utility_router, prefix="/utility", tags=["utility"])
