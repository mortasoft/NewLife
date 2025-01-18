from flask import jsonify, make_response
import utils as app_utils
from apiflask import Schema, APIBlueprint, HTTPError
from apiflask.fields import Integer as apiInteger, String as apiString, Date as apiDate, Decimal as apiDecimal
from apiflask.validators import Length as apiLength, OneOf as apiOneOf, Range as apiRange
from goals.goals import GoalManager, GoalModel
from sqlalchemy import create_engine

class GoalSchema(Schema):
    name = apiString(required=True, validate=apiLength(max=100))
    description = apiString(required=True, validate=apiLength(max=500))
    date = apiDate(required=True)
        
    
class ObjectiveSchema(Schema):
    name = apiString(required=True, validate=apiLength(max=100))
    description = apiString(required=True, validate=apiLength(max=500))
    start_number = apiInteger(required=False)
    end_number = apiInteger(required=False)
    is_boolean = apiInteger(required=False)
    start_value = apiDecimal(required=False)
    end_value = apiDecimal(required=False)
    currency_unit = apiString(required=False, validate=apiLength(max=10))
    goal_id = apiString(required=True, validate=apiLength(max=36))  


def configure_endpoints(app,engine):

    # Define your custom error handler
    @app.errorhandler(HTTPError)
    def handle_http_error(error):
        messages = []
        for field, field_messages in error.detail["json"].items():
            for message in field_messages:
                messages.append(f"{field}: {message}")

        return {"result": "error", "message": messages}, error.status_code
    

    @app.post('/goal/add-goal/')
    @app.doc(tags=['Goal'],description='Add a new goal to the database.')
    @app.input(GoalSchema, location='json')
    @app.output(GoalSchema, status_code=201)
    def add_goal(json_data):
        app_utils.print_with_format(f"[GOAL-ENDPOINT] Adding goal: {json_data}")
        result = GoalManager(engine).add_goal(**json_data)
                
        return {
            'message': result['message'],
            'status_code': result['status_code'],
            'result': result['result'],
            'data': result['data']
        }, result['status_code']

        
    @app.get('/hello')
    def say_hello():
        data = {'message': 'Hello!'}
        return {'data': data, 'message': 'Success!', 'code': 200}
            
            
