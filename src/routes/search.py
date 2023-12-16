from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.repository import search as repository_contacts
from src.schemas import ContactResponse
from src.services.auth import auth_service

search = APIRouter(prefix="/api/search", tags=['search'])


@search.get("/firstname/{firstname}", response_model=ContactResponse)
async def get_contact_firstname(firstname: str = Path(), db: Session = Depends(get_db),
                                current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_firstname(current_user, firstname, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@search.get("/lastname/{lastname}", response_model=ContactResponse)
async def get_contact_lastname(lastname: str = Path(), db: Session = Depends(get_db),
                               current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_lastname(current_user, lastname, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@search.get("/email/{email}", response_model=ContactResponse)
async def get_contact_email(email: str = Path(), db: Session = Depends(get_db),
                            current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_email(current_user, email, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@search.get("/phone/{phone}", response_model=ContactResponse)
async def get_contact_email(phone: str = Path(), db: Session = Depends(get_db),
                            current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_phone(current_user, phone, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@search.get("/shift/{shift}", response_model=List[ContactResponse])
async def get_birthday_list(shift: int, db: Session = Depends(get_db),
                            current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_birthday_list(current_user, shift, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contacts
