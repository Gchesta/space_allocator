import unittest
from os import remove
from os.path import isfile

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from space_allocator.app import dojo, database, Staff, Fellow, LivingSpace, Office, Base, RoomDB, PersonDB


class TestSaveState(unittest.TestCase):

	def setUp(self):
		self.dojo = dojo
		self.database = database
		
	def test_save_state_file_exists_defined_db(self):
		"""test that the db is created with specified name"""
		self.database.save_state("trial.db")
		self.assertTrue(isfile("trial.db"))
		remove("trial.db")

	def test_save_state_succesfully_with_defined_db_2(self):
		"""test that the db is created with specified name"""
		self.dojo.load_people("dummy.txt")
		self.database.save_state("trial.db")
		engine = create_engine("sqlite:///trial.db", echo = False)
		Base.metadata.bind = engine
		DBSession = sessionmaker(bind=engine)
		session = DBSession()
		dbpersons = session.query(PersonDB).all()
		self.assertEqual(len(dbpersons), 35)
		self.assertEqual(dbpersons[17].name, "Skip Cheru")

	def test_save_state_succesfully_with_undefined_db(self):
		self.dojo.load_people("dummy.txt")
		self.database.save_state()
		engine = create_engine("sqlite:///dojo.db", echo = False)
		Base.metadata.bind = engine
		DBSession = sessionmaker(bind=engine)
		session = DBSession()
		dbpersons = session.query(PersonDB).all()
		self.assertEqual(len(dbpersons), 35)
		self.assertEqual(dbpersons[17].name, "Skip Cheru")


class LoadState(unittest.TestCase):

	def setUp(self):
		self.dojo = dojo
		self.database = database
		self.dojo.persons = []
		
	def test_notification_on_lack_of_db(self):
		"""test that the db exists even without defining"""
		fake_db = self.database.load_state("fake.db")
		self.assertEqual(fake_db, "\nThe database you have specified does not exist\n")

	def test_load_state_succesfully(self):
		print(self.dojo.persons)
		no_of_persons1 = len(self.dojo.persons)
		self.assertTrue(no_of_persons1 == 0)
		self.database.load_state("trial.db")
		no_of_persons2 = len(self.dojo.persons)
		self.assertEqual(no_of_persons2 - no_of_persons1, 35)
		self.assertEqual(self.dojo.persons[8].category, "Staff")

		