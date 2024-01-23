
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_name = Column(String(20), unique=True, nullable=False)
    email = Column(String(20), unique=False, nullable=False)
    hash_password = Column(Integer, nullable=False)

    def __repr__(self):
        return f"User(name={self.user_name}, email={self.email},password={self.hash_password})"
