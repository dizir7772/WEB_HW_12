from datetime import date, datetime

from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Contact, User


async def get_contact_by_firstname(user: User, firstname: str, db: Session):
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.firstname==firstname)).first()
    return contact


async def get_contact_by_lastname(user: User, lastname: str, db: Session):
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.lastname==lastname)).first()
    return contact


async def get_contact_by_email(user: User, email: str, db: Session):
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.email==email)).first()
    return contact


async def get_contact_by_phone(user: User, phone: str, db: Session):
    contact = db.query(Contact).filter(and_(Contact.user_id == user.id, Contact.phone==phone)).first()
    return contact


async def get_birthday_list(user: User, shift: int, db: Session):
    contacts = []
    all_contacts = db.query(Contact).filter_by(user_id=user.id).all()
    today = date.today()
    for contact in all_contacts:
        birthday = contact.birthday
        evaluated_date = (datetime(today.year, birthday.month, birthday.day).date() - today).days
        if evaluated_date < 0:
            evaluated_date = (datetime(today.year + 1, birthday.month, birthday.day).date() - today).days
        if evaluated_date <= shift:
            contacts.append(contact)
    return contacts
