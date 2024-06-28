from flask import jsonify
import utils as app_utils

from apiflask import Schema
from apiflask.fields import Integer as apiInteger, String as apiString, Date as apiDate
from apiflask.validators import Length as apiLength, OneOf as apiOneOf, Range as apiRange
from hobbies.hobbies import HobbieManager
from datetime import date, timedelta
from random import randint

class AddActivity(Schema):
    date = apiDate(required=True) 
    title = apiString(required=True, validate=apiLength(0, 50), metadata={'description': 'The title of the activity'}) 
    rating = apiInteger(required=True, validate=apiRange(min=1, max=10)) 
    category = apiString(required=True, validate=apiOneOf(['Cine', 'Pelicula', 'Serie', 'Juego', 'Libro', 'Anime', 'Otro'])) 

class Result(Schema):
    result = apiString()
    message = apiString()

def random_date():
    return date(2024, randint(1, 12), randint(1, 28)).strftime('%Y-%m-%d')

def configure_endpoints(app, database):
    
    try:
        
        hobbies = HobbieManager(database=database)

        @app.post('/hobbies/add-activity/')
        @app.doc(tags=['Hobbies'],description='Add an activity log to the database.')
        @app.input(AddActivity, location='json', example={'date': random_date(), 'title': 'The title of the activity', 'rating': 10, 'category': 'Cine'})
        @app.output(Result, status_code=201)
        def add_activity(json_data):
            try:
                hobbies.add_activity(json_data['date'], json_data['title'], json_data['rating'], json_data['category'])
                return jsonify({'result': 'success', 'message': 'Activity added successfully'})
            except Exception as e:
                return jsonify({'result': 'error', 'message': str(e)})
            
        @app.get('/hobbies/get-activity-log/')
        @app.doc(tags=['Hobbies'],description='Get all the activity logs from the database.')
        @app.output(Result, status_code=200)
        def get_hobbies():
            result = hobbies.get_hobbies()
            return jsonify(result)
    
    except Exception as e:
        app_utils.print_with_format_error(e)

