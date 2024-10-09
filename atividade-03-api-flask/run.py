from api import app, mongo
from api.models.model import Routine
from api.services import services
from api.services.services import RoutineService

if (__name__) == '__main__':
    with app.app_context():
        if 'routines' not in mongo.db.list_collection_names():
            routine = Routine(
                title = '',
                task='',
                date=''
            )
            RoutineService.newRoutine(routine)
    
    app.run(port=4000, debug=True)