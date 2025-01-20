from flask import jsonify, make_response
import utils as app_utils
from apiflask import Schema, APIBlueprint, HTTPError
from apiflask.fields import Integer as apiInteger, String as apiString, Date as apiDate, Decimal as apiDecimal
from apiflask.validators import Length as apiLength, OneOf as apiOneOf, Range as apiRange
from goals.goals import GoalManager, GoalModel
from sqlalchemy import create_engine
import random

class GoalSchema(Schema):
    name = apiString(required=True, validate=apiLength(max=100), example=f"My goal "+ str(random.randint(1, 1000000)))
    description = apiString(required=True, validate=apiLength(max=500), example=f"My goal description")
    date = apiDate(required=True)
    
class GoalSchemaOut(Schema):
    name = apiString(required=True, validate=apiLength(max=100), example=f"My goal "+ str(random.randint(1, 1000000)))
    description = apiString(required=True, validate=apiLength(max=500), example=f"My goal description")
    date = apiDate(required=True)
    id = apiString(required=False, validate=apiLength(max=36), example=f"a1b2c3d4-e5f6-7890-1234-567890abcdef")
    
    
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
    
    GoalModel.metadata.create_all(engine)
    
    # Define your custom error handler
    @app.errorhandler(HTTPError)
    def handle_http_error(error):
        messages = []
        if "json" in error.detail:  # Check if 'json' key exists
            for field, field_messages in error.detail["json"].items():
                for message in field_messages:
                    messages.append(f"{field}: {message}")
        else:  # Handle cases where 'json' is missing
            messages.append(str(error.message))  # Or a more specific message 

        return {"result": "error", "message": messages}, error.status_code
    

    @app.post('/goal/')
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
        
    @app.get('/goal/')
    @app.doc(tags=['Goal'],description='Get all goals from the database.')
    @app.output(GoalSchemaOut(many=True), status_code=200)
    def get_goals():
        try:
            app_utils.print_with_format(f"[GOAL-ENDPOINT] Getting all goals.")
            result = GoalManager(engine).get_goals()
            return {
                'message': result['message'],
                'status_code': result['status_code'],
                'result': result['result'],
                'data': result['data']
            }, result['status_code']
        except Exception as e:
            raise HTTPError(message=f"Error getting goals: {str(e)}", status_code=500)
        
    @app.post('/goal/<string:goal_id>')
    @app.doc(tags=['Goal'],description='Get a goal from the database.')
    @app.output(GoalSchema, status_code=200)
    def get_goal(goal_id):
        try:
            app_utils.print_with_format(f"[GOAL-ENDPOINT] Getting goal: {goal_id}")
            result = GoalManager(engine).get_goal(goal_id)
            return {
                'message': result['message'],
                'status_code': result['status_code'],
                'result': result['result'],
                'data': result['data']
            }, result['status_code']
        except Exception as e:
            raise HTTPError(message=f"Error getting goal: {str(e)}", status_code=500)
        
            
        

        
    @app.get('/hello')
    def say_hello():
        data = {'message': 'Hello!'}
        return {'data': data, 'message': 'Success!', 'code': 200}
            
            
