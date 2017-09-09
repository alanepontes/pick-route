#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_script import Manager, Command

from plugins import app, db

class InitDatabase(Command):
	
	def __init_db(self):
		try:
			db.create_all()
			print('Initialized the database.')
		except Exception as e:
			raise e


	def run(self):
		self.__init_db()

manager = Manager(app)
manager.add_command('init_db', InitDatabase())

if __name__ == '__main__':
	manager.run() 	