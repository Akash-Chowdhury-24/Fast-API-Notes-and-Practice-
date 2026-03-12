from database import base
from sqlalchemy import Column, Integer, String

class Book(base):
    __tablename__ = 'book_table'
    
    id = Column(String(255), primary_key=True)
    title = Column(String(255))
    author = Column(String(255))
    description = Column(String(255))
    
