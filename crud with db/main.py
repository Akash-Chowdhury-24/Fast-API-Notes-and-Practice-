from fastapi import FastAPI
import model
from database import base, engine
from controllers import http_exception_handler
from fastapi.exceptions import HTTPException
from routes import router


app = FastAPI()

base.metadata.create_all(bind=engine)

app.add_exception_handler(HTTPException, http_exception_handler)

app.include_router(router)