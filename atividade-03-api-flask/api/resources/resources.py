from flask_restful import Resource
from api import api
from flask import make_response, jsonify, request
from ..schemas import schemas
from ..models import model
from ..services import services
from ..services.services import RoutineService

class RoutineList(Resource):
    def get(self):
        routines = RoutineService.getRoutines()
        routine = schemas.RoutineSchema(many=True)
        return make_response(routine.jsonify(routines), 200)
    
    def post(self):
        routineSchema = schemas.RoutineSchema()
        validate = routineSchema.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            jsonData = request.get_json()
            newRoutine = model.Routine(**jsonData)
            result = RoutineService.postRoutine(newRoutine)
            res = routineSchema.jsonify(result)
            return make_response(res, 201)
        
        
class RoutineOne(Resource):
    def get(self, id):
        routine = RoutineService.getRoutine(id)
        if routine is None:
            return make_response(jsonify("Não foi encontrada nenhuma rotina com esse id!"), 404)
        routineSchema = schemas.RoutineSchema()
        return make_response(routineSchema.jsonify(routine), 200)
    
    def patch(self, id):
        routine = RoutineService.getRoutine(id)
        if routine is None:
            return make_response(jsonify("Não foi encontrada nenhuma rotina com esse id!"), 404)
        routineschema = schemas.RoutineSchema()
        validate = routineschema.validate(request.json)
        if validate:
            return make_response(jsonify(validate), 400)
        else:
            jsonData = request.get_json()
            newRoutine = model.Routine(**jsonData)
            patchRoutine = RoutineService.patchRoutine(newRoutine, id)
            return make_response(routineschema.jsonify(patchRoutine, 200))
        
    def delete(self, id):
        routine = RoutineService.getRoutine(id)
        if routine is None:
            return make_response(jsonify("Não foi encontrada nenhuma rotina com esse id!"), 404)
        RoutineService.deleteRoutine(id)
        return make_response(jsonify("Registro de rotina deletado com sucesso!"))
    
api.add_resource(RoutineOne, '/routine/<id>')
api.add_resource(RoutineList, '/routines')