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

        return jsonify([i.serialize for i in logistics_routes])

    def post(self):
        
        try:
            LogisticRoute.create_from_text(str(request.data,'utf-8'))
            return jsonify({'result' : 'sucess'})
        except Exception as e:
            return jsonify({'result' : 'error', 'message' : e})


    def delete(self, identifier):
        try:
            logistic_route = LogisticRoute.query.filter(or_(LogisticRoute.name==identifier, LogisticRoute.id==identifier)).first()
            logistic_route.delete()
            return jsonify({'result' : 'sucess'})
        except Exception as e:
            return jsonify({'result' : 'error', 'message' : e})
       


class ShortestRouteAPI(Resource):
    
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, location='args')
        parser.add_argument('source', required=True, location='args')
        parser.add_argument('target', required=True, location='args')
        parser.add_argument('autonomy', required=True, type=float, location='args')
        parser.add_argument('price_per_litre', required=True, type=float, location='args')
        args = parser.parse_args()
        
        logistics_routes = LogisticRoute.query.filter_by(name=args['name']).first()
        shortest_route_and_cost = logistics_routes.get_shortest_route_and_cost(args['source'], args['target'], args['autonomy'], args['price_per_litre'])
        return jsonify(shortest_route_and_cost)


api.add_resource(LogisticRouteAPI, '/logistics-routes', endpoint="logistics-routes")
api.add_resource(LogisticRouteAPI, '/logistics-routes/<identifier>', endpoint="logistic-route")
api.add_resource(ShortestRouteAPI, '/shortests-routes', endpoint="shortests-routes")
