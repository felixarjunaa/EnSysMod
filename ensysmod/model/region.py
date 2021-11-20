from sqlalchemy import Column, Integer, String

from ensysmod.database.base_class import Base


class Region(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    parent_region = Column(String, nullable=True)
