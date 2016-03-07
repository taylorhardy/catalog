import os
import sys
import datetime
# include sqlalchemy
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# User class to create new users


class User(Base):
    __tablename__ = 'Users'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    github_access_token = Column(String(255))

# Category class to create new categories


class Category(Base):
    __tablename__ = 'Categories'

    name = Column(String(255), nullable = False)
    id = Column(Integer, primary_key = True)

# Item class to create new items


class Item(Base):
    __tablename__ = 'Items'

    name = Column(String(255), nullable = False)
    id = Column(Integer, primary_key = True)
    category_id = Column(Integer, ForeignKey('Categories.id'))
    category = relationship(Category)
    description = Column(String(255))
    created = Column(DateTime, default=datetime.datetime.utcnow)


engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)
