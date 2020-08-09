import os
import json
from pprint import pprint
from datetime import datetime

from sqlalchemy import ForeignKey, desc, create_engine, func, Column, BigInteger, Integer, Float, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect

if os.environ.get('DISON_DATABASE') is not None:
  connectionString = os.environ.get('DISON_DATABASE')

engine = create_engine(connectionString, echo=False)

Base = declarative_base()

class SearchURL(Base):
  __tablename__ = 'searchURL'

  Id = Column('id', Integer, primary_key=True)
  Value = Column('value', String)

class Marketplace(Base):
  __tablename__ = 'marketplace'

  Id = Column('id', Integer, primary_key=True)
  Value = Column('value', String)

class Department(Base):
  __tablename__ = 'department'

  Id = Column('id', Integer, primary_key=True)
  Value = Column('value', String)

class Category(Base):
  __tablename__ = 'category'

  Id = Column('id', Integer, primary_key=True)
  Value = Column('value', String)

class eBookCategory(Base):
  __tablename__ = 'ebookcategory'

  Id = Column('id', Integer, primary_key=True)
  Value = Column('value', String)

class Language(Base):
  __tablename__ = 'language'

  Id = Column('id', Integer, primary_key=True)
  Value = Column('value', String)


class Book(Base):
  __tablename__ = 'book'

  ASIN = Column('isbn', String, primary_key=True)
  Title = Column('title', String)
  URL = Column('url', String)
  Author = Column('author', String)
  PaperbackURL = Column('paperbackURL', String)
  PaperbackISBN = Column('paperbackISBN', String)

  # Foreign keys

  # This is inside book page
  eBookCategory_1 = Column('ebookcategory_1', Integer, ForeignKey('ebookcategory.id'))
  eBookCategory_2 = Column('ebookcategory_2', Integer, ForeignKey('ebookcategory.id'))
  eBookCategory_3 = Column('ebookcategory_3', Integer, ForeignKey('ebookcategory.id'))
  LanguageID = Column('language', Integer, ForeignKey('language.id'))

  # This is manually put into db
  SearchURLID = Column('searchURL', Integer, ForeignKey('searchURL.id'))

  # This is on list page
  MarketplaceID = Column('marketplace', Integer, ForeignKey('marketplace.id'), primary_key=True)
  DepartmentID = Column('department', Integer, ForeignKey('department.id'))
  CategoryID = Column('category', Integer, ForeignKey('category.id'))
  SubCategoryID = Column('subcategory', Integer, ForeignKey('category.id'), primary_key=True)
  SubSubCategoryID = Column('subsubcategory', Integer, ForeignKey('category.id'))
  SubSubSubCategoryID = Column('subsubsubcategory', Integer, ForeignKey('category.id'))



Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

class Operations:
  def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

  def GetBooks():
    return [Operations.object_as_dict(x) for x in session.query(Book).all()]

  def GetEBookCategories():
    return [Operations.object_as_dict(x) for x in session.query(eBookCategory).all()]


if __name__ == "__main__":
  pprint(Operations.GetBooks())
  pprint(Operations.GetCategories())
