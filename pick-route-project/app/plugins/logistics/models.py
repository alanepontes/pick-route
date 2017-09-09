#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta
from plugins import db

class MetaModel(db.Model, metaclass=ABCMeta):
	
	def save(self):
		try:
			db.create_all()
			db.session.add(self)
			db.session.commit()
		except Exception as e:
			db.session.rollback()
			print e.args
		

class LogisticRoute(MetaModel):

	__tablename__ = 'logistics_routes'
	
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), unique=True)
	
	def __init__(self, name):
		self.name = name


class Routes(db.Model, MetaModel):

	__tablename__ = 'routes'
	
	id = db.Column(db.Integer, primary_key=True)
	source = db.Column(db.String(80))
	target = db.Column(db.String(80))
	distance = db.Column(db.Numeric, precision=8, scale=2, asdecimal=True)
	logistic_route_id = db.Column(db.Integer, db.ForeignKey('logistic_route.id'))
	logistic_route = db.relationship('LogisticRoute', foreign_keys=logistic_route_id)
	__table_args__ = (db.UniqueConstraint('source', 'target', name='_source_target'),)

	def __init__(self, source, target, distance):
		self.source = source
		self.target = target
		self.distance = distance

