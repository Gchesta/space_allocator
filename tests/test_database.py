from os import remove
from os.path import isfile

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from space_allocator.app import (dojo, database, Staff, Fellow,
	LivingSpace, Office, Base, RoomDB, PersonDB)

class TestSaveState(unittest.TestCase):

	def setUp(self):
		self.dojo = dojo
		self.database = database
		self.offices = ["Dede", "Didi", "Dodo", "Dudu", "Fafa", "Fefe"]
		self.livingspaces = ["Bebe", "Bibi", "Bobo", "Bubu", "Caca", "Cefe"]
	
	def test_save_state_creates_file_when_db_is_defined(self):
		self.database.save_state("trial.db")
		self.assertTrue(isfile("trial.db"))
		remove("trial.db")

	def test_save_state_saves_data_succesfully_with_defined_db(self):
		#First, create two rooms with guaranteed allocations
		self.dojo.create_room("Dada", "Office")
		self.dojo.create_room("Baba", "livingspace")
		self.dojo.load_people("dummy.txt")
		#create more rooms of which Fefe and Cece will be unallocated so...
		#...that we can test whether the function works for empty rooms
		for office in self.offices:
			self.dojo.create_room(office, "Office")
		for livingspace in self.livingspaces:
			self.dojo.create_room(livingspace, "livingspace")
		self.database.save_state("trial.db")
		engine = create_engine("sqlite:///trial.db", echo = False)
		Base.metadata.bind = engine
		DBSession = sessionmaker(bind=engine)
		session = DBSession()
		dbrooms = session.query(RoomDB).all()
		self.assertEqual(len(dbrooms), 14)
		dbpersons = session.query(PersonDB).all()
		self.assertEqual(len(dbpersons), 35)
		self.assertEqual(dbpersons[17].name, "Skip Cheru")

	def test_save_state_saves_data_succesfully_with_undefined_db(self):
		self.dojo.load_people("dummy.txt")
		self.database.save_state()
		engine = create_engine("sqlite:///dojo.db", echo = False)
		Base.metadata.bind = engine
		DBSession = sessionmaker(bind=engine)
		session = DBSession()
		dbrooms = session.query(RoomDB).all()
		dbpersons = session.query(PersonDB).all()
		self.assertEqual(len(dbpersons), 35)
		self.assertEqual(len(dbrooms), 14)
		#Assert that the objects keep their attributes even... 
		#...when transferd to  the DB
		self.assertEqual(dbpersons[17].name, "Skip Cheru")
		self.assertEqual(dbrooms[1].name, "Baba")
		dbpersons = session.query(PersonDB).all()
		self.assertEqual(len(dbpersons), 35)
		self.assertEqual(dbpersons[17].name, "Skip Cheru")

class LoadState(unittest.TestCase):

	def setUp(self):
		self.dojo = dojo
		self.database = database
		self.dojo.persons = []
		self.dojo.rooms = []
		
	def test_notification_on_lack_of_db(self):
		fake_db = self.database.load_state("fake.db")
		self.assertEqual(fake_db, "\nThe database you have specified does not exist\n")

	def test_load_state_succesfully(self):
		print(self.dojo.persons)
		no_of_persons1 = len(self.dojo.persons)
		self.assertTrue(no_of_persons1 == 0)
		self.database.load_state("trial.db")
		no_of_persons2 = len(self.dojo.persons)
		self.assertEqual(no_of_persons2 - no_of_persons1, 35)
		#Assert that objects retained their attributes
		self.assertEqual(self.dojo.persons[8].category, "Staff")
		#Assert that objects revert back to their instance before... 
		#...save_state
		self.assertIsInstance(self.dojo.persons[18], Staff)
		self.assertIsInstance(self.dojo.persons[34], Fellow)
		self.assertIsInstance(self.dojo.rooms[0], Office)
		self.assertIsInstance(self.dojo.rooms[1], LivingSpace)
		#Assert that rooms Fefe and Cece still have zero occupancy
		self.assertFalse(self.dojo.rooms[12].occupants)
		self.assertFalse(self.dojo.rooms[13].occupants)
