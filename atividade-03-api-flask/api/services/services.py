from api import mongo
from bson import ObjectId
from ..models import model

class RoutineService:
    
    @staticmethod
    def getRoutines():
        return list(mongo.db.routines.find())
    
    @staticmethod
    def getRoutine(id):
        return mongo.db.routines.find_one({'_id': ObjectId(id)})
    
    def postRoutine(routine):
        result = mongo.db.routines.insert_one({
            'title': routine.title,
            'task': routine.task,
            'date': routine.date
        })
        return mongo.db.routines.find_one({'_id': ObjectId(result.inserted_id)})
    
    def patchRoutine(self, id):
        patchRoutine = mongo.db.routines.find_one_and_update(
            {'_id': ObjectId(id)},
            {'$set':{
                'title': self.title,
                'task': self.task,
                'date': self.date
            }},
            return_document=True
        )
        return patchRoutine
    
    def deleteRoutine(id):
        mongo.db.routines.delete_one({'_id': ObjectId(id)})
    