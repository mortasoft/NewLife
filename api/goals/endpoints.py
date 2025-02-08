from typing import Dict, Any
from http import HTTPStatus
from datetime import date
import utils as app_utils
from apiflask import Schema, HTTPError
from apiflask.fields import (
    Integer as ApiInteger,
    String as ApiString,
    Date as ApiDate,
    Decimal as ApiDecimal
)
from apiflask.validators import (
    Length as ApiLength,
    OneOf as ApiOneOf,
    Range as ApiRange
)
from goals.models import GoalManager

# Constants
CURRENCY_CHOICES = ["USD", "CRC", "EUR"]
MAX_STRING_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 500
MAX_UUID_LENGTH = 36
MAX_NUMBER_VALUE = 1_000_000

class BaseSchema(Schema):
    """Base schema with common fields and methods."""
    @staticmethod
    def generate_example_id() -> str:
        return "a1b2c3d4-e5f6-7890-1234-567890abcdef"

class GoalSchema(BaseSchema):
    """Schema for goal creation requests."""
    name = ApiString(
        required=True,
        validate=ApiLength(max=MAX_STRING_LENGTH),
        example="My 2025 Savings Goal"
    )
    description = ApiString(
        required=True,
        validate=ApiLength(max=MAX_DESCRIPTION_LENGTH),
        example="Save money for a down payment"
    )
    date = ApiDate(
        required=True,
        example=date.today().isoformat()
    )
    
class GoalSchemaOut(GoalSchema):
    """Schema for goal responses, extends GoalSchema with ID."""
    id = ApiString(
        required=False,
        validate=ApiLength(max=MAX_UUID_LENGTH),
        example=BaseSchema.generate_example_id()
    )
    
    
class ObjectiveSchema(BaseSchema):
    """Schema for objective creation and responses."""
    name = ApiString(
        required=True,
        validate=ApiLength(max=MAX_STRING_LENGTH),
        example="Save 100 dollars"
    )
    description = ApiString(
        required=True,
        validate=ApiLength(max=MAX_DESCRIPTION_LENGTH),
        example="Monthly savings target"
    )
    start_number = ApiInteger(
        required=False,
        validate=ApiRange(min=0, max=MAX_NUMBER_VALUE),
        example=0
    )
    end_number = ApiInteger(
        required=False,
        validate=ApiRange(min=0, max=MAX_NUMBER_VALUE),
        example=1000
    )
    is_boolean = ApiInteger(
        required=False,
        validate=ApiOneOf([0, 1]),
        example=0
    )
    start_value = ApiDecimal(
        required=False,
        validate=ApiRange(min=0, max=MAX_NUMBER_VALUE),
        example=0
    )
    end_value = ApiDecimal(
        required=False,
        validate=ApiRange(min=0, max=MAX_NUMBER_VALUE),
        example=100
    )
    currency_unit = ApiString(
        required=False,
        validate=ApiOneOf(CURRENCY_CHOICES),
        example="USD"
    )
    goal_id = ApiString(
        required=True,
        validate=ApiLength(max=MAX_UUID_LENGTH),
        example=BaseSchema.generate_example_id()
    )

class EndpointManager:
    """Manages API endpoints and their configuration."""
    
    def __init__(self, app, engine):
        self.app = app
        self.goal_manager = GoalManager(engine)
        self.setup_error_handlers()
        self.setup_endpoints()
        self.initialize_database()

    def initialize_database(self):
        """Initialize database tables."""
        self.goal_manager.create_tables()
        app_utils.print_with_format("[GOAL-ENDPOINT] Creating all tables.")

    def setup_error_handlers(self):
        """Configure error handlers for the application."""
        @self.app.errorhandler(HTTPError)
        def handle_http_error(error: HTTPError) -> tuple[Dict[str, Any], int]:
            messages = []
            if "json" in error.detail:
                messages.extend(
                    f"{field}: {message}"
                    for field, field_messages in error.detail["json"].items()
                    for message in field_messages
                )
            else:
                messages.append(str(error.message))
            
            return {
                "result": "error",
                "message": messages
            }, error.status_code

    def setup_endpoints(self):
        """Configure all API endpoints."""
        self._setup_goal_endpoints()
        self._setup_objective_endpoints()
        self._setup_utility_endpoints()

    def _setup_goal_endpoints(self):
        """Configure goal-related endpoints."""
        
        @self.app.post('/goal/')
        @self.app.doc(tags=['Goal'], description='Add a new goal.')
        @self.app.input(GoalSchema, location='json')
        @self.app.output(GoalSchemaOut, status_code=HTTPStatus.CREATED)
        def add_goal(json_data):
            app_utils.print_with_format(f"[GOAL-ENDPOINT] Adding goal: {json_data}")
            result = self.goal_manager.add_goal(**json_data)
            return app_utils.create_response(result)

        @self.app.get('/goal/')
        @self.app.doc(tags=['Goal'], description='Get all goals.')
        @self.app.output(GoalSchemaOut(many=True))
        def get_goals():
            try:
                app_utils.print_with_format("[GOAL-ENDPOINT] Getting all goals.")
                result = self.goal_manager.get_goals()
                return app_utils.create_response(result)
            except Exception as e:
                raise HTTPError(
                    message=f"Error getting goals: {str(e)}", 
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR
                )

        @self.app.get('/goal/<string:goal_id>')
        @self.app.doc(tags=['Goal'], description='Get a specific goal.')
        @self.app.output(GoalSchema)
        def get_goal(goal_id):
            try:
                app_utils.print_with_format(f"[GOAL-ENDPOINT] Getting goal: {goal_id}")
                result = self.goal_manager.get_goal(goal_id)
                return app_utils.create_response(result)
            except Exception as e:
                raise HTTPError(
                    message=f"Error getting goal: {str(e)}", 
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR
                )

    def _setup_objective_endpoints(self):
        """Configure objective-related endpoints."""
        
        @self.app.post('/goal/objective/')
        @self.app.doc(tags=['Goal'], description='Add a new objective.')
        @self.app.input(ObjectiveSchema, location='json')
        @self.app.output(ObjectiveSchema, status_code=HTTPStatus.CREATED)
        def add_objective(json_data):
            app_utils.print_with_format(f"[GOAL-ENDPOINT] Adding objective: {json_data}")
            result = self.goal_manager.add_objective(**json_data)
            return app_utils.create_response(result)

    def _setup_utility_endpoints(self):
        """Configure utility endpoints."""
        
        @self.app.get('/hello')
        def say_hello():
            return app_utils.create_response({
                'data': {'message': 'Hello!'},
                'message': 'Success!',
                'status_code': HTTPStatus.OK
            })


def configure_endpoints(app, engine):
    """Entry point for endpoint configuration."""
    EndpointManager(app, engine)