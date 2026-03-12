from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


MYSQL_USER = "root"
MYSQL_PASSWORD = "BumbaIsGood24#"
MYSQL_LOCALHOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DB = "fastapi"

MYSQL_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_LOCALHOST}:{MYSQL_PORT}/{MYSQL_DB}"

engine = create_engine(MYSQL_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

base = declarative_base()

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()