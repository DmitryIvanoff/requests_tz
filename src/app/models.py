from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, JSON, Index, Integer
Base = declarative_base()


class Request(Base):
    __tablename__ = 'requests'

    key = Column(String, primary_key=True, index=True)
    body = Column(JSON, nullable=True)
    amount = Column(Integer, default=1)

    def __repr__(self):
       return f"Request(key={self.key!r}, body={self.body!r}, amount{self.amount!r})"
