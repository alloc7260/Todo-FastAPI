from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("sqlite:///db.sqlite")

SessionLocal = sessionmaker(bind=engine)
# SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)