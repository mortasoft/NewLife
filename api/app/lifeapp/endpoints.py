from flask import jsonify
from lifeapp.hobbies import Hobbies
from apiflask import Schema
from apiflask.fields import Integer, String, Date
from apiflask.validators import Length, OneOf, Range

class AddActivity(Schema):
    date = Date(required=True) 
    title = String(required=True, validate=Length(0, 50), metadata={'description': 'The title of the activity'}) 
    rating = Integer(required=True, validate=Range(min=1, max=10)) 
    category = String(required=True, validate=OneOf(['Cine', 'Pelicula', 'Serie', 'Juego', 'Libro', 'Anime', 'Otro'])) 

class Result(Schema):
    result = String()
    message = String()
    

def configure_endpoints(app):
    
    hobbies = Hobbies()

    @app.post('/hobbies/add-activity/')
    @app.doc(tags=['LifeApp'])
    @app.input(AddActivity, location='json')
    @app.output(Result, status_code=201)
    def add_activity(json_data):
        try:
            hobbies.add_activity(json_data['date'], json_data['title'], json_data['rating'], json_data['category'])
            return jsonify({'result': 'success', 'message': 'Activity added successfully'})
        except Exception as e:
            return jsonify({'result': 'error', 'message': str(e)})
        
    @app.get('/hobbies/get-activity-log/')
    @app.doc(tags=['LifeApp'])
    @app.output(Result, status_code=200)
    def get_hobbies():
        result = hobbies.get_hobbies()
        return jsonify(result)
        

