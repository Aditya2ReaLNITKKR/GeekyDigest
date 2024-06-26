from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

sqlalchemy_db_url="sqlite:///./NewsServer.db"
engine=create_engine(
    sqlalchemy_db_url,connect_args={"check_same_thread":False}

)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()