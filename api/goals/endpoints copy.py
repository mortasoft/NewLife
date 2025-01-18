from flask import jsonify, make_response
import utils as app_utils
from apiflask import Schema, HTTPError
from apiflask import APIBlueprint, Schema, input, output
from apiflask.fields import Integer as apiInteger, String as apiString, Date as apiDate, Decimal as apiDecimal
from apiflask.validators import Length as apiLength, OneOf as apiOneOf, Range as apiRange
from goals.goals import GoalManager, GoalSchema
from sqlalchemy.exc import NoForeignKeysError, IntegrityError

# Define the blueprint
goals_bp = APIBlueprint('goals', __name__, url_prefix='/goals')

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


class ObjectiveSchema(Schema):  # Schema for Objective model
    id = apiString()
    name = apiString()
    # ... other fields as needed
 
class Result(Schema):
    result = apiString()
    message = apiString()
    
    

    

def configure_endpoints(app,database):

    # Define your custom error handler
    @app.errorhandler(HTTPError)
    def handle_http_error(error):
        messages = []
        for field, field_messages in error.detail["json"].items():
            for message in field_messages:
                messages.append(f"{field}: {message}")

        return {"result": "error", "message": messages}, error.status_code
    
    try:
        
        goals = GoalManager(database)

        @app.post('/goal/add-goal/')
        @app.doc(tags=['Goal'],description='Add a new goal to the database.')
        @app.input(Add_Goal, location='json')
        @app.output(GoalSchema, status_code=201)
        def add_goal(json_data):
            try:
                response = goals.add_goal(**json_data)
                app_utils.print_with_format(f"[add-goal] {response.result} {response.message}")
                return make_response(jsonify({'result': response.result, 'message': response.message, 'data': response.data}), response.status_code)
            except Exception as e:
                app_utils.print_with_format(f"[add-goal-error] {e} {e.__class__.__name__}", type="error")
                return make_response(jsonify({'result': 'error', 'message': str(e)}), 500)
            
        @app.get('/goal/get-goals/')
        @app.doc(tags=['Goal'],description='Get all goals from the database.')
        #@app.output(Add_Goal(many=True), status_code=200)
        #@app.output(Result, status_code=200)
        def get_goals():
            try:
                result = goals.get_goals()
                print(result)
                return GoalSchema(many=True).dump(result), 200
                #return make_response(jsonify(result), 201)
            except Exception as e:
                app_utils.print_with_format(f"[get-goals] {e} {e.__class__}", type="error")
                raise HTTPError(500, message=str(e))
                #return jsonify({'result': 'error', 'message': str(e)})
        
        
        @app.post('/goal/add-objective/')
        @app.doc(tags=['Goal'],description='Add a new objective to the database.')
        @app.input(AddObjective, location='json')
        @app.output(Result, status_code=201)
        def add_objective(json_data):
            try:
                response = goals.add_objective(json_data['name'], json_data['description'], json_data['goal_id'], json_data['start_number'], json_data['end_number'], json_data['is_boolean'], json_data['start_value'], json_data['end_value'], json_data['currency_unit'])
                return make_response(jsonify({'result': response.result, 'message': response.message}), response.status_code)
            except NoForeignKeysError as e:
                app_utils.print_with_format(f"[add-objective] {e} {e.__class__.__name__}",type="error")
                return jsonify({'result': 'error', 'message': f'Error adding objective. Check the foreign keys. {e}'})
            except Exception as e:
                app_utils.print_with_format(f"[add-objective] {e} {e.__class__.__name__}", type="error")
                return make_response(jsonify({'result': response.result, 'message': response.message}), response.status_code)
            
        @app.get('/goals/get-objectives/')
        @app.doc(tags=['Goal'],description='Get all the objectives from the database.')
        @app.output(Result, status_code=200)
        def get_objectives():
            result = goals.get_objectives()
            return jsonify(result)
        
        @app.get('/goals/get-objectives-by-goal/<string:goal_id>')
        @app.doc(tags=['Goal'],description='Get the objectives of a goal.')
        @app.output(Result, status_code=200)
        def get_objectives_by_goal(goal_id):
            result = goals.get_objectives_by_goal(goal_id)
            return jsonify(result)
            
    except Exception as e:
        app_utils.print_with_format(e, type="error")
        return jsonify({'result': 'error', 'message': str(e)})