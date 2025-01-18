from dataclasses import dataclass
from sqlalchemy import create_engine, ForeignKey, String, Integer, Date, Column, Numeric, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Date, Column, Numeric, DateTime
from database import Database
import utils as app_utils

BASE_NAME = "hobbies"

@dataclass
class ActivityLog(Database.Base):
    __tablename__ = BASE_NAME + "_" +  'activity_log'
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=app_utils.generate_uuid)
    date: Mapped[Date] = mapped_column(Date())
    title: Mapped[str] = mapped_column(String(60))
    rating: Mapped[int] = mapped_column(Integer)
    category: Mapped[str] = mapped_column(String(40))
    
    def __init__(self, date, title, rating, category):
        self.date = date
        self.title = title
        self.rating = rating
        self.category = category
        
    def __repr__(self) -> str:
        return f"[Date={self.date}, Title={self.title}, Rating={self.rating}, Category={self.category}]"

   
class HobbieManager():
    def __init__(self, database) -> None:
        try:
            self.db = database
            self.session = database.Session()
            app_utils.print_with_format(f"[Hobbies] The database session was assigned successfully to the {BASE_NAME} class.")
        except Exception as e:
            app_utils.print_with_format(f"[Hobbies] Error creating session in {BASE_NAME} class {e}", type="error")    
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
            self.session.refresh(new)
            app_utils.print_with_format(f"Activity log {new} created successfully")
            return new
        except Exception as e:
            app_utils.print_with_format(f"Error creating activity log {new} {e}", type="error")
            self.session.rollback()
            return None
        finally:
            self.session.close()       
        
    def get_hobbies(self):
        """
        Gets all the activity logs from the database.
        
        Returns:
            list: List of activity logs.
        """
        try:
            result = self.session.query(ActivityLog).order_by(ActivityLog.date).all()
            formatted_result = []
            for activity in result:
                formatted_date = activity.date.strftime("%Y-%m-%d")
                formatted_activity = {
                    "id": activity.id,
                    "date": formatted_date,
                    "title": activity.title,
                    "rating": activity.rating,
                    "category": activity.category
                }
                formatted_result.append(formatted_activity)
            app_utils.print_with_format(f"Activity logs retrieved successfully")
            return formatted_result
        except Exception as e:
            app_utils.print_with_format(f"Error retrieving activity logs {e}", type="error")
            raise
        finally:
            self.session.close()