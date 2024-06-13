from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Company(Base):
    __tablename__ = "companies"

    cid = Column(Integer, primary_key=True)
    cname = Column(String)
    clogo = Column(LargeBinary)  # Use LargeBinary for storing logos as blobs
    caddress = Column(String)
    username = Column(String)
    password = Column(String)

    def __repr__(self):
        return f"Company(cid={self.cid}, cname='{self.cname}')"
