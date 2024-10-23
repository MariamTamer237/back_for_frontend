import logging

from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import settings

logger = logging.getLogger(__name__)

RealEstateBase = declarative_base()
RealEstate_URL = URL.create(
    settings.database_type,
    username=settings.database_username,
    password=settings.database_password,
    port=1433,
    database=settings.database_name,
    host=settings.database_host,
    query={"charset": "utf8"},
)
logger.info(f"Connection string created for admin: {RealEstate_URL}")
realEstate_engine = create_engine(RealEstate_URL)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    binds={
        RealEstateBase: realEstate_engine,
    },
)
