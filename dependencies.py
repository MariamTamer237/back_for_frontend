from collections import defaultdict
from typing import Annotated
from uuid import UUID
from webbrowser import get

from fastapi import Depends, Header, HTTPException, Security, status
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import constants
from .config import settings
from .database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
