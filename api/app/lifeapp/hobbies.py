from lifeapp.db import *
from utils import print_with_format
from dataclasses import dataclass

BASE_NAME = "hobbies"

@dataclass
class ActivityLog(Base):
    __tablename__ = BASE_NAME + "_" +  'activity_log'
    
    id: str
    date: str
    title: str
    rating: int
    category: str
        
    id = Column("id", String(36), primary_key=True, default=generate_uuid)
    date = Column("date", Date())
    title = Column("title", String(40)) 
    rating = Column("rating", Integer)
    category = Column("category", String(40))
    
    def __init__(self, date, title, rating, category):
        self.date = date
        self.title = title
        self.rating = rating
        self.category = category
        
    def __repr__(self) -> str:
        return f"[Date={self.date}, Title={self.title}, Rating={self.rating}, Category={self.category}]"

   
class Hobbies():
    def __init__(self) -> None:
        try:
            self.session = DB().session
        except Exception as e:
            raise
    
    def add_activity(self, date, title, rating, category):
        """
        Adds an activity log to the database.
        
        Args:
            date (str): The date of the activity log.
            title (str): The title of the activity log.
            rating (int): The rating of the activity log.
            category (str): The category of the activity log.
        
        """
        new = ActivityLog(date, title, rating, category)
        try:
            self.session.add(new)
            self.session.commit()
            print_with_format(f"Activity log {new} created successfully")
        except Exception as e:
            print_with_format(f"Error creating activity log {new}")
            self.session.rollback()
            raise
        finally:
            self.session.close()       
        
    def get_hobbies(self):
        """
        Gets all the activity logs from the database.
        
        Returns:
            list: List of activity logs.
        """
        try:
            result = self.session.query(ActivityLog).all()
            print_with_format(f"Activity logs retrieved successfully")
            return result
        except Exception as e:
            print_with_format(f"Error retrieving activity logs")
            raise
        finally:
            self.session.close()