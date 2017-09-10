from flask import request, jsonify
from flask_restful import reqparse, Resource
from sqlalchemy import or_
from plugins import api
from plugins.logistics.models import LogisticRoute

class LogisticRouteAPI(Resource):
    
    def get(self, identifier=None):
        if identifier:
            logistics_routes = LogisticRoute.query.filter(or_(LogisticRoute.name==identifier, LogisticRoute.id==identifier)).all()
        else:    
            logistics_routes = LogisticRoute.query.all()

        return jsonify([i.serialize for i in logistics_routes]), 200

    def post(self):
        LogisticRoute.create_from_text(str(request.data,'utf-8'))
        return jsonify({'result' : 'sucess'}), 201

    def put(self, identifier):
        return jsonify({'name' : 'test'})

    def delete(self, identifier):
        logistics_routes = LogisticRoute.query.filter(or_(LogisticRoute.name==identifier, LogisticRoute.id==identifier)).all()
        return jsonify({'name' : 'test'})


api.add_resource(LogisticRouteAPI, '/logistics-routes', endpoint="logistics-routes")
api.add_resource(LogisticRouteAPI, '/logistics-routes/<identifier>', endpoint="logistic-route")

