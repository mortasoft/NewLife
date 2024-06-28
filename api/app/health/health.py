from dataclasses import dataclass
from sqlalchemy import create_engine, ForeignKey, String, Integer, Date, Column, Numeric, DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
import utils as app_utils
from database import Database

BASE_NAME = "health"

@dataclass
class Weight(Database.Base):
    __tablename__ = BASE_NAME + "_" +  'weight'
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=app_utils.generate_uuid)
    date: Mapped[Date] = mapped_column(Date())
    weight: Mapped[float] = mapped_column(Numeric(5,2))
    imc: Mapped[float] = mapped_column(Float)
    bodyFat: Mapped[float] = mapped_column(Float)
    subcutaneousFat: Mapped[float] = mapped_column(Float)
    viseralFat: Mapped[float] = mapped_column(Float)
    muscleMass: Mapped[float] = mapped_column(Float)
    
    def __init__(self, date, weight, imc, bodyFat, subcutaneousFat, viseralFat, muscleMass):
        self.date = date
        self.weight = weight
        self.imc = imc
        self.bodyFat = bodyFat
        self.subcutaneousFat = subcutaneousFat
        self.viseralFat = viseralFat
        self.muscleMass = muscleMass
    
    def __repr__(self) -> str:
        return f"[Date={self.date}, Weight={self.weight}, IMC={self.imc}, Body Fat={self.bodyFat}, Subcutaneous Fat={self.subcutaneousFat}, Viseral Fat={self.viseralFat}, Muscle Mass={self.muscleMass}]"


@dataclass
class Nutrition(Database.Base):
    __tablename__ = BASE_NAME + "_" +  'nutrition'
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=app_utils.generate_uuid)
    food_type: Mapped[str] = mapped_column(String(40))
    name: Mapped[str] = mapped_column(String(100))
    portion: Mapped[str] = mapped_column(String(36))
    example: Mapped[str] = mapped_column(String(100))
    recipe: Mapped[str] = mapped_column(String(500))
    price: Mapped[float] = mapped_column(Float)
    
    def __init__(self, food_type, name, portion, example, recipe, price):
        self.food_type = food_type
        self.name = name
        self.portion = portion
        self.example = example
        self.recipe = recipe
        self.price = price
    
    def __repr__(self) -> str:
        return f"[Food Type={self.food_type}, Name={self.name}, Portion={self.portion}, Example={self.example}, Recipe={self.recipe}, Price={self.price}]"


@dataclass
class Menu(Database.Base):
    __tablename__ = BASE_NAME + "_" +  'nutrition_menu'

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=app_utils.generate_uuid)
    day_of_week: Mapped[int] = mapped_column(Integer)
    menu_week_id: Mapped[str] = mapped_column(String(36))
    breakfast_id: Mapped[str] = Column(String(36), ForeignKey(f"{BASE_NAME}_nutrition.id"), nullable=False)
    breakfast_snack_id: Mapped[str] = Column(String(36), ForeignKey(f"{BASE_NAME}_nutrition.id"), nullable=False)
    lunch_id: Mapped[str] = Column(String(36), ForeignKey(f"{BASE_NAME}_nutrition.id"), nullable=False)
    afternoon_snack_id: Mapped[str] = Column(String(36), ForeignKey(f"{BASE_NAME}_nutrition.id"), nullable=False)
    dinner_id: Mapped[str] = Column(String(36), ForeignKey(f"{BASE_NAME}_nutrition.id"), nullable=False)
    night_snack_id: Mapped[str] = Column(String(36), ForeignKey(f"{BASE_NAME}_nutrition.id"), nullable=False)
    
    breakfast = relationship("Nutrition", foreign_keys=[breakfast_id])
    breakfast_snack = relationship("Nutrition", foreign_keys=[breakfast_snack_id])
    lunch = relationship("Nutrition", foreign_keys=[lunch_id])
    afternoon_snack = relationship("Nutrition", foreign_keys=[afternoon_snack_id])
    dinner = relationship("Nutrition", foreign_keys=[dinner_id])
    night_snack = relationship("Nutrition", foreign_keys=[night_snack_id])
    
    def __init__(self, day_of_week, menu_week_id, breakfast_id, breakfast_snack_id, lunch_id, afternoon_snack_id, dinner_id, night_snack_id):
        self.day_of_week = day_of_week
        self.menu_week_id = menu_week_id
        self.breakfast_id = breakfast_id
        self.breakfast_snack_id = breakfast_snack_id
        self.lunch_id = lunch_id
        self.afternoon_snack_id = afternoon_snack_id
        self.dinner_id = dinner_id
        self.night_snack_id = night_snack_id
        
    def __repr__(self) -> str:
        return f"[Day of Week={self.day_of_week}, Menu Week ID={self.menu_week_id}, Breakfast ID={self.breakfast_id}, Breakfast Snack ID={self.breakfast_snack_id}, Lunch ID={self.lunch_id}, Afternoon Snack ID={self.afternoon_snack_id}, Dinner ID={self.dinner_id}, Night Snack ID={self.night_snack_id}]"
        
   
class HealthManager():
    def __init__(self,database) -> None:
        try:
            self.db = database
            self.session = database.Session()
            app_utils.print_with_format(f"[Health] The database session was assigned successfully to the {BASE_NAME} class.")
        except Exception as e:
            app_utils.print_with_format_error(f"[Health] Error creating session in {BASE_NAME} class {e}")    
            raise
    
    def add_weight(self, date, weight, imc, bodyFat, subcutaneousFat, viseralFat, muscleMass): 
        """
        Adds a weight log to the database.
        
        Args:
            date (str): The date of the weight log.
            weight (float): The weight of the weight log.
            imc (float): The imc of the weight log.
            bodyFat (float): The body fat of the weight log.
            subcutaneousFat (float): The subcutaneous fat of the weight log.
            viseralFat (float): The viseral fat of the weight log.
            muscleMass (float): The muscle mass of the weight log.
        """
        new = Weight(date, weight, imc, bodyFat, subcutaneousFat, viseralFat, muscleMass)
        try:
            with self.session as session:
                session.add(new)
                session.commit()
                app_utils.print_with_format(f"Weight log {new} created successfully")
        except Exception as e:
            app_utils.print_with_format_error(f"Error creating activity log {new}")
        
        
    def get_weights(self):
        """
        Gets all the weight logs from the database.
        
        Returns:
            list: List of weight logs.
        """
        try:
            result = self.session.query(Weight).all()
            app_utils.print_with_format(f"Activity logs retrieved successfully")
            return result
        except Exception as e:
            app_utils.print_with_format_error(f"Error retrieving activity logs {e}")
            raise
        finally:
            self.session.close()       
            pass
        
    def add_nutrition(self, food_type, name, portion, example, recipe, price):
        """
        Adds a nutrition log to the database.
        
        Args:
            food_type (str): The type of food.
            name (str): The name of the food.
            portion (str): The portion of the food.
            example (str): An example of the food.
            recipe (str): The recipe of the food.
            price (float): The price of the food.
        """
        new = Nutrition(food_type, name, portion, example, recipe, price)
        try:
            with self.session as session:
                session.add(new)
                session.commit()
                app_utils.print_with_format(f"Nutrition log {new} created successfully")
        except Exception as e:
            app_utils.print_with_format_error(f"Error creating nutrition log {new}")
            self.session.rollback()
            raise
        finally:
            self.session.close()       
            pass
    
    def get_nutrition(self):
        """
        Gets all the nutrition logs from the database.
        
        Returns:
            list: List of nutrition logs.
        """
        try:
            result = self.session.query(Nutrition).all()
            app_utils.print_with_format(f"Nutrition logs retrieved successfully")
            return result
        except Exception as e:
            app_utils.print_with_format_error(f"Error retrieving nutrition logs {e}")
            raise
        finally:
            self.session.close()       
            pass
    
    def add_menu(self,day_of_week, menu_week_id, breakfast_id, breakfast_snack_id, lunch_id, afternoon_snack_id, dinner_id, night_snack_id):
        
        new_menu = Menu(day_of_week, menu_week_id, breakfast_id, breakfast_snack_id, lunch_id, afternoon_snack_id, dinner_id, night_snack_id)
        
        try: 
            with self.session as session:
                session.add(new_menu)
                session.commit()
                app_utils.print_with_format(f"Menu {new_menu} created successfully")
        except Exception as e:
            app_utils.print_with_format_error(f"Error creating menu {new_menu}")
    
    def create_week_menu(self, menu_week_id, menu):
        """
        Creates a week menu.
        
        Args:
            menu_week_id (str): The id of the week menu.
            menu (list): The list of menus.
        """
        for m in menu:
            self.add_menu(m['day_of_week'], menu_week_id, m['breakfast_id'], m['breakfast_snack_id'], m['lunch_id'], m['afternoon_snack_id'], m['dinner_id'], m['night_snack_id'])
    
    
    def get_menu_week(self, menu_week_id):
        """
        Gets the menu from the selected week menu.
        
        Args:
            menu_week_id (str): The id of the week menu.
        
        Returns:
            list: List of menus.
        """
        try:
            result = self.session.query(Menu).filter(Menu.menu_week_id == menu_week_id).all()
            app_utils.print_with_format(f"Menu retrieved successfully")
            return result
        except Exception as e:
            app_utils.print_with_format_error(f"Error retrieving menu {e}")
            raise
        finally:
            self.session.close()       
            pass