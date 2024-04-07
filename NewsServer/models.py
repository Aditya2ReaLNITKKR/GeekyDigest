from sqlalchemy import Boolean,Column,ForeignKey,Integer,String
from sqlalchemy.orm import relationship

from NewsServer.database import Base
class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True)
    email=Column(String,unique=True,index=True)
    is_active=Column(Boolean,default=True)
    