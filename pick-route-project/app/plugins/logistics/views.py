from plugins import api
from flask import request, jsonify
from flask_restful import Resource

class LogisticRouteAPI(Resource):
    
    def get(self):
        return jsonify({'name' : 'test'})

    def post(self):
    	pass

api.add_resource(LogisticRouteAPI, '/logistics/')