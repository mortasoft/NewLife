import os
import sys
from pathlib import Path
from flask import redirect
from apiflask import APIFlask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine
import utils as app_utils

class LifeApp_API:
    def __init__(self):
        # Add parent directory to path using pathlib
        parent_dir = Path(__file__).parent.parent
        sys.path.append(str(parent_dir))
        
        # Load configuration
        self.config = app_utils.load_env_vars()
        
        # Initialize Flask app
        self.app = self._create_app()
        
        # Setup database
        self.db = self._setup_database()
        
        # Configure routes and endpoints
        self._configure_routes()
    
    def _create_app(self) -> APIFlask:
        """Create and configure the Flask application instance."""
        app = APIFlask(
            __name__,
            title=f"{self.config.API_TITLE} | {self.config.ENVIRONMENT_TYPE}",
            version=self.config.VERSION
        )
        
        # Database configuration
        app.config.update(
            SQLALCHEMY_DATABASE_URI=self.config.SQLALCHEMY_DATABASE_URI,
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            BASE_RESPONSE_SCHEMA=app_utils.BaseResponse,
            BASE_RESPONSE_DATA_KEY='data'
        )
        
        return app
    
    def _setup_database(self) -> SQLAlchemy:
        """Setup database connection and migrations."""
        db = SQLAlchemy(self.app)
        Migrate(self.app, db)
        self.engine = create_engine(
            self.config.SQLALCHEMY_DATABASE_URI,
            pool_pre_ping=True  # Enable connection health checks
        )
        return db
    
    def _configure_routes(self):
        """Configure application routes and endpoints."""
        @self.app.route("/")
        @self.app.doc(hide=True)
        def home():
            return redirect("/docs", code=302)
        
        # Import endpoints here to avoid circular imports
        import goals.endpoints as goals_endpoints
        goals_endpoints.configure_endpoints(self.app, self.engine)
    
    def run(self):
        """Run the Flask application."""
        try:
            self.app.run(
                debug=self.config.API_DEBUG,
                host=self.config.API_HOST,
                port=self.config.API_PORT
            )
            app_utils.print_with_format(
                f"API running on {self.config.API_HOST}:{self.config.API_PORT}",
                type="info"
            )
        except Exception as e:
            app_utils.print_with_format(
                f"Failed to start API: {str(e)}", 
                type="error"
            )
            sys.exit(1)

if __name__ == '__main__':
    flask_app = LifeApp_API()
    flask_app.run()