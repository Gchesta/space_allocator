
from os import remove
from os.path import isfile
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from termcolor import cprint

from .room import LivingSpace, Office
from .person import Fellow, Staff
from space_allocator.app import dojo
from .tables import RoomDB, PersonDB, Base

#dojo = Dojo()
class Database:

	def __init__(self):
		self.dojo = dojo

	def save_state(self, db_name="dojo.db"):
		if db_name:
			db_name = db_name
		else:
			db_name = "dojo.db"
		try:
			remove(db_name)
		except Exception:
			pass
		engine = create_engine("sqlite:///" + db_name, echo = False)
		Base.metadata.bind = engine
		Base.metadata.create_all(engine)
		DBSession = sessionmaker(bind=engine)
		session = DBSession()

		for room in self.dojo.rooms:
			room_to_persist = RoomDB(name = room.name, category = room.category,
			available_capacity = room.available_capacity)
			session.add(room_to_persist)
		session.commit()
		for person in self.dojo.persons:
			person_to_persist = PersonDB(idno = person.idno, name = person.name, office = str(person.office),
			accomodation = str(person.accomodation), category = person.category)
			session.add(person_to_persist)
		session.commit()
		cprint("\nSuccessfully saved the session\n", "yellow")

	def load_state(self, db_name):
		if not isfile(db_name):
			msg = "\nThe database you have specified does not exist\n"
			cprint(msg, "magenta")
			return msg

		engine = create_engine("sqlite:///" + db_name, echo = False)
		Base.metadata.bind = engine
		DBSession = sessionmaker(bind=engine)
		session = DBSession()
		self.dojo.persons = []
		self.dojo.rooms = []
		dbpersons = session.query(PersonDB).all()
		dbrooms = session.query(RoomDB).all()

		for person in dbpersons:
			name = person.name
			office = person.office
			idno = person.idno
			category = person.category
			accomodation = person.accomodation

			if category == "Fellow":
				person_to_load = Fellow(name, office, idno, accomodation)
			else:
				person_to_load = Staff(name, office, idno)
			if office != "Unallocated":
				try:
					db_office = [room for room in dbrooms if room.name == office][0]
					office_to_load = Office(office)
					person_to_load.office = office_to_load
					office_to_load.available_capacity = db_office.available_capacity
					office_to_load.occupants.append(person_to_load)
					self.dojo.rooms.append(office_to_load)
					dbrooms.remove(db_office)
				except IndexError:
					already_loaded_office = [room for room in dojo.rooms if room.name == office][0]
					person_to_load.office = already_loaded_office
					already_loaded_office.occupants.append(person_to_load)

			if accomodation != "Unallocated" and accomodation != "":
				try:
					db_livingspace = [room for room in dbrooms if room.name == accomodation][0]
					livingspace_to_load = LivingSpace(accomodation)
					person_to_load.accomodation = livingspace_to_load
					livingspace_to_load.available_capacity = db_livingspace.available_capacity
					livingspace_to_load.occupants.append(person_to_load)
					self.dojo.rooms.append(livingspace_to_load)
					dbrooms.remove(db_livingspace)
				except IndexError:
					already_loaded_livingspace = [room for room in dojo.rooms if room.name == accomodation][0]
					person_to_load.accomodation = already_loaded_livingspace
					already_loaded_livingspace.occupants.append(person_to_load)
			self.dojo.persons.append(person_to_load)

		for room in dbrooms:
			if room.category == "Office":
				self.dojo.append(Office(room.name))
			else:
				self.dojo.append(LivingSpace(room.name))
		cprint("\nSuccessfully loaded state\n", "yellow")





	