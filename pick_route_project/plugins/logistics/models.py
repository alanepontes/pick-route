import json
from decimal import Decimal
from abc import ABCMeta
from tools.graph import Graph
from plugins import db

class MetaModel():
    __metaclass__ = ABCMeta

    def save(self):
        try:
            db.create_all()
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        try:
            db.create_all()
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
    routes = db.relationship("Route", cascade="all, delete-orphan")

    def as_graph(self):
        graph = Graph()
        for route in self.routes:
            graph.add_vertex(route.source, {route.target : route.distance})
        return graph

    def get_shortest_route_and_cost(self, source, target, autonomy, price_per_litre):
        graph = self.as_graph()
        shortest_route, total_distance = graph.shortest_path(source, target)
        return shortest_route, (float(total_distance)/autonomy)*price_per_litre

    @staticmethod
    def create_from_text(text):
        db.session.begin(subtransactions=True)
        try:

            name, *paths = text.split('\n')     
            
            for logistic_route in LogisticRoute.query.filter_by(name=name).all():
                logistic_route.delete()
            
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
    distance = db.Column(db.Float(precision=8, scale=2, asdecimal=True))
    logistic_route_id = db.Column(db.Integer, db.ForeignKey('logistic_route.id'))
    logistic_route = db.relationship("LogisticRoute", back_populates="routes")

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

