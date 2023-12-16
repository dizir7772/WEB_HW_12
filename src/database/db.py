import configparser
import pathlib

from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError


env = "DEV_DB"
# URI:  postgresql://username:password@domain:port/database
file_config = pathlib.Path(__file__).parent.parent.parent.joinpath("config.ini")
config = configparser.ConfigParser()
config.read(file_config)

username = config.get(env, 'USER')
password = config.get(env, 'PASSWORD')
domain = config.get(env, 'HOST')
port = config.get(env, 'PORT')
database = config.get(env, 'DB_NAME')

URI = f"postgresql://{username}:{password}@{domain}:{port}/{database}"

engine = create_engine(URI, echo=True)
DBSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# Dependency
def get_db():
    db = DBSession()
    try:
        yield db
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    finally:
        db.close()
