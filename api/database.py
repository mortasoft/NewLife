from utils import print_with_format
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy_utils import database_exists, create_database
import sys

class Database():
    """
    Database class for managing database connections and sessions.
    """
    Base = declarative_base()
    
    def __init__(self, DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME) -> None:
        """
        Initializes the database connection.

        Raises:
            Exception: If there is an error connecting to the database.
        """       
        try:
            
            self.conn_string = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
            self.engine = create_engine(self.conn_string, echo=False, pool_pre_ping=True, pool_recycle=3600, pool_size=10, max_overflow=20, future=True)
            
            # Create the database if it does not exist.
            if not database_exists(self.engine.url):
                create_database(self.engine.url)
            
            self.Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine, future=True)        
            print_with_format(f"[Database] Connected to the database")
            
            # Create all Tables if doesn't exist
            self.create_all_tables()
            self.state = True
            
        except Exception as e:
            print_with_format(f"[Utils.DB] Error connecting to the database {e}. Exiting...", type="error")
            self.state = False
            sys.exit()
    
    
    def get_session(self):
        with self.Session() as session:
            try:
                yield session
                session.commit()
            except Exception as e:
                session.rollback()
                raise
             
               
    def create_all_tables(self):
        """
        Creates all the tables in the database.
        """
        self.Base.metadata.create_all(self.engine)
        print_with_format(f"[Utils.DB] All tables created successfully.")
    
    
    def __str__(self) -> str:
        return f"DB({self.conn_string})"
    