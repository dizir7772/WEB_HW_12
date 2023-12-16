import enum

from sqlalchemy import Boolean, Column, Integer, String, DateTime, Date, func, event, Enum, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Role(enum.Enum):
    admin: str = 'admin'
    moderator: str = 'moderator'
    user: str = 'user'


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    firstname = Column(String(50), index=True)
    lastname = Column(String(50), index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String(15), unique=True, index=True, nullable=False)
    birthday = Column(Date, default=func.now())
    additional_info = Column(String(150), nullable=True)
    is_favorite = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), default=1)
    user = relationship('User', backref='contacts')


@event.listens_for(Contact, 'before_insert')
def updated_favorite(mapper, conn, target):
    if target.firstname.startswith('My'):
        target.is_favorite = True


@event.listens_for(Contact, 'before_update')
def updated_favorite(mapper, conn, target):
    if target.firstname.startswith('My'):
        target.is_favorite = True


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(150), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    refresh_token = Column(String(255), nullable=True)
    avatar = Column(String(255), nullable=True)
    roles = Column('roles', Enum(Role), default=Role.moderator)
