from typing import Dict, Any
from http import HTTPStatus
import utils as app_utils
from apiflask import Schema, HTTPError
from apiflask.fields import (
    String as ApiString,
    Decimal as ApiDecimal,
)
from apiflask.validators import (
    Length as ApiLength,
)
from IA.models import GeminiManager

MAX_STRING_LENGTH = 500

class BaseSchema(Schema):
    """Base schema with common fields and methods."""
    @staticmethod
    def generate_example_id() -> str:
        return "a1b2c3d4-e5f6-7890-1234-567890abcdef"
    

class GeminiSchema(BaseSchema):
    """Schema for Gemini API requests."""
    prompt = ApiString(
        required=True,
        validate=ApiLength(max=MAX_STRING_LENGTH),
        example="What is IA?"
    )
    sys_instruction = ApiString(
        required=False,
        default="You are a cat. Your name is Saki. At the end of each response, you should say 'meow'.",
        example="You are a cat. Your name is Saki. At the end of each response, you should say 'meow'."
    )
    

class GeminiResponse(BaseSchema):
    """Schema for Gemini API responses."""
    response = ApiString()
    generation_time = ApiDecimal(
        required=False)
    

class EndpointManager:
    """Manages API endpoints and their configuration."""
    
    def __init__(self, app, engine):
        self.app = app
        self.gemini_manager = GeminiManager(engine)
        self.setup_error_handlers()
        self.setup_endpoints()

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
        self._setup_endpoints()


    def _setup_endpoints(self):
        """Configure goal-related endpoints."""
        
        @self.app.post('/gemini/')
        @self.app.doc(tags=['Gemini'], description='Ask to Gemini')
        @self.app.input(GeminiSchema, location='json')
        @self.app.output(GeminiResponse, status_code=HTTPStatus.CREATED)
        def request_gemini(json_data):
            app_utils.print_with_format(f"[Gemini] Request Gemini: {json_data}")
            result = self.gemini_manager.request(**json_data)
            return app_utils.create_response(result)


def configure_endpoints(app, engine):
    """Entry point for endpoint configuration."""
    EndpointManager(app, engine)