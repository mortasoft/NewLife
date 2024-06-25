from flask import jsonify

from apiflask import Schema
from apiflask.fields import Integer as apiInteger, String as apiString, Date as apiDate, Decimal as apiDecimal
from apiflask.validators import Length as apiLength, OneOf as apiOneOf, Range as apiRange

import utils as app_utils

from health.health import Health
from health.db import *
from sqlalchemy import String, Integer, Date, Column, Numeric, DateTime

class AddWeight(Schema):
    date = apiDate(required=True) 
    weight = apiDecimal(required=True, validate=apiRange(min=0, max=300))
    imc = apiDecimal(required=True, validate=apiRange(min=0, max=100))
    bodyFat = apiDecimal(required=True, validate=apiRange(min=0, max=100))
    subcutaneousFat = apiDecimal(required=True, validate=apiRange(min=0, max=100))
    viseralFat = apiDecimal(required=True, validate=apiRange(min=0, max=100))
    muscleMass = apiDecimal(required=True, validate=apiRange(min=0, max=100))
 

class Result(Schema):
    result = String()
    message = String()
    

def configure_endpoints(app):
    
    try:
        
        database = DB()
        health = Health(database)

        @app.post('/health/add-weight/')
        @app.doc(tags=['Health'],description='Add a weight log to the database.')
        @app.input(AddWeight, location='json')
        @app.output(Result, status_code=201)
        def add_weight(json_data):
            try:
                health.add_weight(json_data['date'], json_data['weight'], json_data['imc'], json_data['bodyFat'], json_data['subcutaneousFat'], json_data['viseralFat'], json_data['muscleMass'])
                return jsonify({'result': 'success', 'message': 'Weight added successfully'})
            except Exception as e:
                return jsonify({'result': 'error', 'message': str(e)})
            
        @app.get('/health/get-weights/')
        @app.doc(tags=['Health'],description='Get all the weight logs from the database.')
        @app.output(Result, status_code=200)
        def get_health():
            result = health.get_weights()
            return jsonify(result)
    
    except Exception as e:
        app_utils.print_with_format_error(e)

