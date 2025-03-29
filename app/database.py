from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


db_driver = "postgresql"
db_host = settings.DATABASE_HOSTNAME
db_port = settings.DATABASE_PORT
db_username = settings.DATABASE_USERNAME
db_password = settings.DATABASE_PASSWORD
db_name = settings.DATABASE_NAME



SQLALCHEMY_DATABASE_URL = f"{db_driver}://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()