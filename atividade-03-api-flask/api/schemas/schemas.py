from api import ma
from marshmallow import Schema, fields

class RoutineSchema(ma.Schema):
    class WhyMeta:
        fields = ('_id', 'title', 'task', 'date')
        
    _id = fields.Str()
    title = fields.Str(required=True)
    task = fields.Dict(required=True)
    #Eu ia colocar Date, mas pra testar ia ser terrível!
    date = fields.Str(required=True)
    