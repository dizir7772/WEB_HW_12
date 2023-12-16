from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Contact, User
from src.schemas import ContactModel, ContactFavoriteModel


async def get_contacts(user: User, limit: int, offset: int, db: Session):
    contacts = db.query(Contact).filter(Contact.user_id == user.id).limit(limit).offset(offset).all()
    return contacts


async def get_contact_by_id(user: User, contact_id: int, db: Session):
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.id==contact_id)).first()
    return contact


async def create(user: User, body: ContactModel, db: Session):
    contact = Contact(**body.dict(), user_id=user.id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update(user: User, contact_id: int, body: ContactModel, db: Session):
    contact = await get_contact_by_id(user, contact_id, db)
    if contact:
        contact.firstname = body.firstname
        contact.lastname = body.lastname
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.additional_info = body.additional_info
        contact.is_favorite = body.is_favorite
        db.commit()
    return contact


async def remove(user: User, contact_id: int, db: Session):
    contact = await get_contact_by_id(user, contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def set_favorite(user: User, contact_id: int, body: ContactFavoriteModel, db: Session):
    contact = await get_contact_by_id(user, contact_id, db)
    if contact:
        contact.is_favorite = body.is_favorite
        db.commit()
    return contact
