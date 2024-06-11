from sqlalchemy import create_engine
from sqlalchemy import DateTime
from sqlalchemy import Column, Integer,Double, Sequence, String, Text, PrimaryKeyConstraint, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlalchemy import and_
from datetime import datetime
from datetime import timedelta
from pydantic import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()
connection_string = "mysql+pymysql://root:mechanix93@localhost/fastapi_db_memes"
engine = create_engine(connection_string)
Session = sessionmaker(bind=engine)

class MemesList(Base):
    __tablename__ = "memes_list"
    id_memes = Column(Integer)
    name_memes = Column(String(100))
    description_memes = Column(String(250))
    __table_args__ = (PrimaryKeyConstraint(id_memes), {},)

Base.metadata.create_all(engine)