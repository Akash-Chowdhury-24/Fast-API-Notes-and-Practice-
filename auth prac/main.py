from fastapi import FastAPI
from utils.http_exception_handle import http_exception_handler
from fastapi.exceptions import HTTPException
import model
from database import engine,Base
from routes import router

app = FastAPI()
app.add_exception_handler(HTTPException, http_exception_handler)
app.include_router(router)
Base.metadata.create_all(bind=engine)
