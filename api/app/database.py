from utils import print_with_format, print_with_format_error
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sys

class Database():
    
    Base = declarative_base()
    
    def __init__(self, DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME) -> None:
        """
        Initializes the database connection.

        Raises:
            Exception: If there is an error connecting to the database.
        """       
        try:
            
            self.DB_USER = DB_USER
            self.DB_PASS = DB_PASS
            self.DB_HOST = DB_HOST
            self.DB_PORT = DB_PORT
            self.DB_NAME = DB_NAME
            self.conn_string = f"mysql+pymysql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            self.engine = create_engine(self.conn_string, echo=False, pool_pre_ping=True, pool_recycle=3600, pool_size=10, max_overflow=20, future=True)
            
            # Create the database if it does not exist.
            if not database_exists(self.engine.url):
                create_database(self.engine.url)
            else:
                # Connect to the database.
                self.connection = self.engine.connect()
                self.Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine, future=True)        
                print_with_format(f"[Utils.DB] Connected to the database")
            
            # Create all Tables if doesn't exist
            self.create_all_tables()
            self.state = True
            
        except Exception as e:
            print_with_format_error(f"[Utils.DB] Error connecting to the database {e}. Exiting...")
            self.state = False
               
    def create_all_tables(self):
        """
        Creates all the tables in the database.
        """
        self.Base.metadata.create_all(self.engine)
        print_with_format(f"[Utils.DB] All tables created successfully.")
    
    def __str__(self) -> str:
        return f"DB({self.DB_USER}, {self.DB_PASS}, {self.DB_HOST}, {self.DB_PORT}, {self.DB_NAME})"