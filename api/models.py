#models.py
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Enum
from database import Base



# Define To Do class inheriting from Base
class usersInfo(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True)
    password = Column(String)
    email = Column(String)
    institution = Column(String)
    
    
    
    
# Define To Do class inheriting from Base
class componentsInfo(Base):
    __tablename__ = "component"

    component_id = Column(Integer, index=True, primary_key=True)
    type = Column(String)
    hostname = Column(String)
    URL_access = Column(String)
    username = Column(String)
    state = Column(String)
