import os

from sqlalchemy import create_engine, URL, Column, Integer, String, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from constants import message
from tools.tool import getHash
from exceptions import exception

dbUrl = URL.create(
    "postgresql+psycopg2",
    username=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT"),
    database=os.getenv("POSTGRES_DBNAME"),
)
engine = create_engine(dbUrl)
conn = engine.connect()
SessionFactory = sessionmaker(bind=engine)
Base = declarative_base()

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(32))
    password = Column(String(32))
    password_retry = Column(Integer)
    updated_on = Column(DATETIME)

def findUser(username):
    try:
        with SessionFactory() as session:
            result = session.query(Users).filter_by(username=username).first()
            session.commit()
            return result and result.username
    except Exception:
        raise exception.DatabaseError(message.DATABASE_ERROR)

def getUserPassword(username):
    try:
        with SessionFactory() as session:
            user = session.query(Users).filter_by(username=username).first()
            session.commit()
            return (True, user) if user and user.password else (False, None)
    except Exception:
        raise exception.DatabaseError(message.DATABASE_ERROR)

def saveUser(username, password, updated):
    try:
        hash = getHash(password)
        new = Users(username=username, password=hash, password_retry=0, updated_on=updated)
        with SessionFactory() as session:
            session.add(new)
            session.commit()
    except Exception:
        raise exception.DatabaseError(message.DATABASE_ERROR)

def updateUser(userId, passwordRetry, updatedOn):
    try:
        updateContent = {"password_retry": passwordRetry}
        if updatedOn:
            updateContent.setdefault("updated_on", updatedOn)
        with SessionFactory() as session:
            session.query(Users).filter_by(id=userId)\
                .update(updateContent)
            session.commit()
    except Exception:
        raise exception.DatabaseError(message.DATABASE_ERROR)
