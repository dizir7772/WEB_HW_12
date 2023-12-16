from typing import List

from fastapi import Depends, HTTPException, status, Path, APIRouter, Query
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User, Role
from src.repository import contacts as repository_contacts
from src.schemas import ContactResponse, ContactModel, ContactFavoriteModel
from src.services.auth import auth_service
from src.services.role import RoleAccess


router = APIRouter(prefix="/api/contacts", tags=['contacts'])

allowed_operation_get = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_create = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_update = RoleAccess([Role.admin, Role.moderator])
allowed_operation_remove = RoleAccess([Role.admin])


@router.get("/", response_model=List[ContactResponse], dependencies=[Depends(allowed_operation_get)])
async def get_contacts(limit: int = Query(10, le=500), offset: int = 0, db: Session = Depends(get_db),
                       current_user: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(current_user, limit, offset, db)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(allowed_operation_get)])
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_id(current_user, contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(allowed_operation_create)])
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.create(current_user, body, db)
    return contact


@router.put("/{contact_id}", response_model=ContactResponse, dependencies=[Depends(allowed_operation_update)],
            description='Only moderators and admin')
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update(current_user, contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(allowed_operation_remove)])
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove(current_user, contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact


@router.patch("/{contact_id}/favorite", response_model=ContactResponse,
              dependencies=[Depends(allowed_operation_update)])
async def favorite_contact(body: ContactFavoriteModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                           current_user: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.set_favorite(current_user, contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    return contact
