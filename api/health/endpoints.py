from flask import jsonify, make_response
import utils as app_utils

from apiflask import Schema, HTTPError
from apiflask.fields import Integer as apiInteger, String as apiString, Date as apiDate, Decimal as apiDecimal
from apiflask.validators import Length as apiLength, OneOf as apiOneOf, Range as apiRange
from health.health import HealthManager
from sqlalchemy.exc import NoForeignKeysError

class AddWeight(Schema):
    date = apiDate(required=True) 
    weight = apiDecimal(required=True, validate=apiRange(min=0, max=300))
    imc = apiDecimal(required=True, validate=apiRange(min=0, max=100))
    body_fat = apiDecimal(required=True, validate=apiRange(min=0, max=100))
    subcutaneous_fat = apiDecimal(required=True, validate=apiRange(min=0, max=100))
    visceral_fat = apiDecimal(required=True, validate=apiRange(min=0, max=100))
    muscle_mass = apiDecimal(required=True, validate=apiRange(min=0, max=100))
    
    
class AddNutrition(Schema):
    food_type = apiString(required=True, validate=apiLength(max=40))
    name = apiString(required=True, validate=apiLength(max=100))
    portion = apiString(required=True, validate=apiLength(max=36))
    example = apiString(required=True, validate=apiLength(max=100))
    recipe = apiString(required=True, validate=apiLength(max=500))
    price = apiDecimal(required=True, validate=apiRange(min=0, max=50000))
    

class AddMenu(Schema):
    day_of_week = apiString(required=True, validate=apiOneOf(['1', '2', '3', '4', '5', '6', '7']))
    menu_week_id = apiString(required=True, validate=apiLength(max=50))
    breakfast_id = apiString(required=True, validate=apiLength(max=36))
    breakfast_snack_id = apiString(required=True, validate=apiLength(max=36))
    lunch_id = apiString(required=True, validate=apiLength(max=36))
    afternoon_snack_id = apiString(required=True, validate=apiLength(max=36))
    dinner_id = apiString(required=True, validate=apiLength(max=36))
    night_snack_id = apiString(required=True, validate=apiLength(max=36))
    

class Get_Menu_Week(Schema):
    menu_week_id = apiString(required=True, validate=apiLength(max=50))

 
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

        return {
            "result": "error",
            "message": messages
        }, error.status_code
    
    try:
        
        database = database
        health = HealthManager(database)

        @app.post('/health/add-weight/')
        @app.doc(tags=['Health'],description='Add a weight log to the database.')
        @app.input(AddWeight, location='json')
        @app.output(Result, status_code=201)
        def add_weight(json_data):
            try:
                # Extract data from json_data, providing default values for optional fields
                date = json_data['date']
                weight = json_data['weight']
                imc = json_data['imc']
                body_fat = json_data.get('body_fat') 
                subcutaneous_fat = json_data.get('subcutaneous_fat')
                visceral_fat = json_data.get('visceral_fat')
                muscle_mass = json_data.get('muscle_mass')

                response = health.add_weight(date, weight, imc, body_fat, subcutaneous_fat, visceral_fat, muscle_mass)
                return make_response(jsonify({'result': response.result, 'message': response.message}), response.status_code)
                
            except Exception as e:
                app_utils.print_with_format(f"[add-weight] {e} {e.__class__.__name__}", type="error")
                return make_response(jsonify({'result': 'error', 'message': str(e)}), 500)
            
        @app.get('/health/get-weights/')
        @app.doc(tags=['Health'],description='Get all the weight logs from the database.')
        @app.output(Result, status_code=200)
        def get_health():
            result = health.get_weights()
            return jsonify(result)
        
        
        @app.post('/health/add-nutrition/')
        @app.doc(tags=['Health'],description='Add a nutrition log to the database')
        @app.input(AddNutrition, location='json')
        @app.output(Result, status_code=201)
        def add_nutrition(json_data):
            try:
                health.add_nutrition(json_data['food_type'], json_data['name'], json_data['portion'], json_data['example'], json_data['recipe'], json_data['price'])
                return jsonify({'result': 'success', 'message': 'Nutrition log added successfully'})
            except NoForeignKeysError as e:
                app_utils.print_with_format(f"[add-nutrition] {e} {e.__class__.__name__}",type="error")
                return jsonify({'result': 'error', 'message': f'Error adding nutrition log. Check the foreign keys. {e}'})
            except Exception as e:
                app_utils.print_with_format(f"[add-nutrition] {e} {e.__class__.__name__}", type="error")
                return jsonify({'result': 'error', 'message': str(e)})
            
        @app.get('/health/get-nutrition/')
        @app.doc(tags=['Health'],description='Get all nutrition logs from the database.')
        @app.output(Result, status_code=200)
        def get_nutrition():
            result = health.get_nutrition()
            return jsonify(result)
        
        @app.post('/health/add-menu/')
        @app.doc(tags=['Health'],description='Add a menu log to the database')
        @app.input(AddMenu, location='json')
        @app.output(Result, status_code=201)
        def add_menu(json_data):
            try:
                health.add_menu(json_data['day_of_week'], json_data['menu_week_id'], json_data['breakfast_id'], json_data['breakfast_snack_id'], json_data['lunch_id'], json_data['afternoon_snack_id'], json_data['dinner_id'], json_data['night_snack_id'])
                return jsonify({'result': 'success', 'message': 'Menu log added successfully'})
            except Exception as e:
                app_utils.print_with_format(f"[add-menu] {e} {e.__class__.__name__}", type="error")
                return jsonify({'result': 'error', 'message': str(e)})
            
        @app.get('/health/get-menu/<int:menu_week_id>')
        @app.doc(tags=['Health'],description='Get the menu from the selected week menu')
        @app.input(Get_Menu_Week, location='json')
        @app.output(Result, status_code=200)
        def get_menu(menu_week_id):
            try:
                result = health.get_menu_week(menu_week_id)
                return jsonify(result)
            except Exception as e:
                app_utils.print_with_format(e, type="error")
                return jsonify({'result': 'error', 'message': str(e)})
    
    except Exception as e:
        app_utils.print_with_format(e, type="error")
        return jsonify({'result': 'error', 'message': str(e)})
        

