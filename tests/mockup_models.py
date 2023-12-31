from sqlalchemy import Column, Integer, String

from .mockup_database import Base


class Film(Base):
    __tablename__ = "films"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    year = Column(String)
    rating = Column(String)
