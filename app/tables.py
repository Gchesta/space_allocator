from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class PersonDB(Base):
	"""The class Person will be used to create a table that will store the information
	regarding fellows and staff"""

	__tablename__ = "persons"

	idno = Column(String(3), primary_key=True, autoincrement=False)
	name = Column(String(250),  nullable=False)
	office = Column(String(250),  nullable=False)
	accomodation = Column(String(250),  nullable=True)
	category = Column(String(250),  nullable=False)

class RoomDB(Base):
	"""The class Room will be used to create a table that will store the information
	regarding the rooms that are in the dojo."""

	__tablename__ = "rooms"

	name = Column(String(250), primary_key=True, nullable=False)
	category = Column(String(250),  nullable=False)
	available_capacity = Column(Integer,  nullable=False)
