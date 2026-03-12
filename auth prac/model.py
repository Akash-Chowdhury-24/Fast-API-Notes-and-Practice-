from database import Base
from sqlalchemy import Column, Integer, String


class User(Base):
  __tablename__ = 'users'
  
  name = Column(String(255), nullable=False)
  email = Column(String(255), nullable=False, unique=True)
  password = Column(String(255), nullable=False)
  role = Column(String(255), nullable=False, default='user')
  id = Column(String(255), primary_key=True, index=True)