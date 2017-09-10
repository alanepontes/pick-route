import json
from decimal import Decimal
from abc import ABCMeta
from plugins import db

class MetaModel():
    __metaclass__ = ABCMeta

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    

class LogisticRoute(db.Model, MetaModel):
    
    __metaclass__ = type('LogisticRouteMeta', (type(db.Model), type(MetaModel)), {})
    __tablename__ = 'logistic_route'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    routes = db.relationship("Route",  back_populates="logistic_route")

    @staticmethod
    def as_graph(identifier):
        logistics_routes = LogisticRoute.query.filter(or_(LogisticRoute.name==identifier, LogisticRoute.id==identifier)).all()


    @staticmethod
    def create_from_text(text):
        db.session.begin(subtransactions=True)
        try:
            name, *paths = text.split('\n')     
            logistic_route = LogisticRoute(name)
            logistic_route.save()
            for path in paths:
                source, target, distance = path.split(' ')
                logistic_route.add_route(source, target, distance)
            
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
    @property
    def serialize(self):
        return {
            'id'     : self.id,
            'name'   : self.name,
            'routes' : [route.serialize for route in self.routes]
        }

    def add_route(self, source, target, distance):
        route = Route(source, target, distance, self)
        route.save()

    def __init__(self, name):
        self.name = name


class Route(db.Model, MetaModel):
    __metaclass__ = type('RouteMeta', (type(db.Model), type(MetaModel)), {})
    __tablename__ = 'route'
    
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(80))
    target = db.Column(db.String(80))
    distance = db.Column(db.Numeric(precision=8, scale=2, asdecimal=True))
    logistic_route_id = db.Column(db.Integer, db.ForeignKey('logistic_route.id'))
    logistic_route = db.relationship("LogisticRoute", back_populates="routes")
    __table_args__ = (db.UniqueConstraint('source', 'target', name='_source_target'),)

    def __init__(self, source, target, distance, logistic_route):
        self.source = source
        self.target = target
        self.distance = distance
        self.logistic_route = logistic_route

    @property
    def serialize(self):
        return {
            'id'       : self.id,
            'source'   : self.source,
            'target'   : self.target,
            'distance' : float(self.distance)
        }

