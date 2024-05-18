from sqlalchemy import create_engine, ForeignKey, String, Integer, Date, Column, Numeric, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, asc, desc
import uuid
import hashlib
import os
from utils import print_with_format



def generate_uuid():
    """
    Generates a UUID.

    Returns:
        str: UUID generated.
    """
    return str(uuid.uuid4())


def generate_hash(text):
    """
    Generates a hash from a text.

    Args:
        text (str): Text to hash.

    Returns:
        str: Hash generated.
    """
    return hashlib.sha1(text.encode()).hexdigest()


class Base(DeclarativeBase):
    pass

    
class DB():
    def __init__(self) -> None:
        """
        Initializes the database connection.

        Raises:
            Exception: If there is an error connecting to the database.
        """
        self.DB_USER = os.getenv("DB_USERNAME")
        self.DB_PASS = os.getenv("DB_PASSWORD")
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_PORT = os.getenv("DB_PORT")
        self.DB_NAME = os.getenv("DB_LIFEAPP_NAME")
        conn_string = f"mysql+pymysql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        engine = create_engine(conn_string, echo=False)
        
        try:
            # Create the database if it does not exist.
            if not database_exists(engine.url):
                create_database(engine.url)
            else:
                # Connect to the database.
                engine.connect()
            
            # Create the tables.
            Base.metadata.create_all(bind=engine)
            
            Session = sessionmaker(bind=engine)        
            self.session = Session()
            print_with_format("Connected to the database")
        except Exception as e:
            print_with_format("Error connecting to the database")
            raise
    
    def __str__(self) -> str:
        return f"DB({self.DB_USER}, {self.DB_PASS}, {self.DB_HOST}, {self.DB_PORT}, {self.DB_NAME})"