from typing import List
from dataclasses import dataclass
from sqlalchemy import create_engine, ForeignKey, String, Integer, Date, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from apiflask import Schema, fields
import utils as app_utils
from database import Database

class Base(DeclarativeBase):
    pass

BASE_NAME = "goals"

@dataclass
class GoalModel(Base):
    __tablename__ = BASE_NAME + "_" +  'goal'
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=app_utils.generate_uuid)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    
    # Objectives related to the goal
    objectives: Mapped[List["ObjectiveModel"]] = relationship(
        back_populates="goal", cascade="all, delete-orphan"
    )
    
    def __init__(self, name, description, date):
        self.name = name
        self.description = description
        self.date = date
    
    def __repr__(self):
        return f"Goal(id={self.id}, name={self.name}, date={self.date})"


@dataclass
class ObjectiveModel(Base):
    __tablename__ = BASE_NAME + "_" +  'objective'
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=app_utils.generate_uuid)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(500))
    
     # For numeric objectives
    start_number: Mapped[int] = mapped_column(Integer, nullable=True)
    end_number: Mapped[int] = mapped_column(Integer, nullable=True)
    
    # For boolean objectives
    is_boolean: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # For Currency objectives
    start_value: Mapped[Float] = mapped_column(Float(10, 2), nullable=True)  # 10 digits, 2 decimal places
    end_value: Mapped[Float] = mapped_column(Float(10, 2), nullable=True)
    currency_unit: Mapped[str] = mapped_column(String(10), nullable=True)  # Example USD, EUR, etc.
    
     # Foreign key linking to Goal
    goal_id: Mapped[str] = mapped_column(String(36), ForeignKey(BASE_NAME + "_goal.id"), nullable=False)
    
    # Relationship back to Goal
    goal: Mapped["GoalModel"] = relationship("GoalModel", back_populates="objectives")
    
    # @validates Decorator for automatic validation 
    @validates('start_value')
    def validate_start_value(self, key, value):
        if value is not None and self.end_value is not None and value > self.end_value:
            raise ValueError("El valor de start_value no puede ser mayor que end_value.")
        return value

    @validates('end_value')
    def validate_end_value(self, key, value):
        if value is not None and self.start_value is not None and value < self.start_value:
            raise ValueError("El valor de end_value no puede ser menor que start_value.")
        return value
    
    def __init__(self, name, description, goal_id, start_number=None, end_number=None, is_boolean=False, start_value=None, end_value=None, currency_unit=None):
        self.name = name
        self.description = description
        self.goal_id = goal_id
        self.start_number = start_number
        self.end_number = end_number
        self.is_boolean = is_boolean
        self.start_value = start_value
        self.end_value = end_value
        self.currency_unit = currency_unit
    
    def __repr__(self) -> str:
        return f"[Objective Name={self.name}, Description={self.description}, Start Number={self.start_number}, End Number={self.end_number}, Is Boolean={self.is_boolean}, Start Value={self.start_value}, End Value={self.end_value}, Currency Unit={self.currency_unit}]"

   
class GoalManager():
    def __init__(self,engine) -> None:
        try:
            self.engine = engine
            app_utils.print_with_format(f"[Goal] The database was assigned successfully to the {BASE_NAME} class.")
        except Exception as e:
            app_utils.print_with_format(f"[Goal] Error creating session in {BASE_NAME} class {e}", type="error")    
            raise
    
    def add_goal(self, name, description, date):
        """
        Adds a goal to the database.
        """
        with Session(self.engine) as session:
            new = GoalModel(name=name, description=description, date=date)
            session.add(new)
            session.flush()
            session.commit()
            message = f"[Goal] {new} created successfully"
            app_utils.print_with_format(message)
            

        
        
        
        with self.db.Session() as session:
                return app_utils.Response('success', message, 201, Go.dump(self, new, many=False))
            except Exception as e:
                self.db.Session().rollback()
                app_utils.print_with_format(f"Error creating goal {e}", type="error")
                return app_utils.Response('error', f"Error creating goal {e}", 500)
        
    def get_goals(self):
        """
        Gets all the goals from the database.
        
        Returns:
            list: List of goals.
        """
        try:
            with self.db.Session() as session:
                stmt = select(Goal).options(joinedload(Goal.objectives))
                result = session.execute(stmt)
                goals = result.scalars().all()
                return goals
        except Exception as e:
            app_utils.print_with_format(f"Error retrieving goals {e}", type="error")
            return app_utils.Response('error', f"Error retrieving goals {e}", 500)
            
        
    def add_objective(self, name, description, goal, start_number=None, end_number=None, 
                      is_boolean=False, start_value=None, end_value=None, currency_unit=None):
        """
        Adds an objective to the database.
        
        Args:
            name (str): The name of the objective.
            description (str): The description of the objective.
            goal_id (str): The id of the goal.
            start_number (int): The start number of the objective.
            end_number (int): The end number of the objective.
            is_boolean (bool): If the objective is boolean.
            start_value (Float): The start value of the objective.
            end_value (Float): The end value of the objective.
            currency_unit (str): The currency unit of the objective.
        """
        try:
            with self.db.Session() as session:
                goal_instance=session.query(Goal).filter(Goal.id == goal).first()
                
                # Create the new objective object
                new_objective = Objective(
                    name=name,
                    description=description,
                    goal_id=goal_instance,
                    start_number=start_number,
                    end_number=end_number,
                    is_boolean=is_boolean,
                    start_value=start_value,
                    end_value=end_value,
                    currency_unit=currency_unit
                )
                
                #session.add(goal_instance)
                session.add(new_objective)
                session.commit()
                message = f"Objective {new_objective} created successfully"
                app_utils.print_with_format(message)
                return app_utils.Response('success', message, 201)
        except IntegrityError as e:
            app_utils.print_with_format(f"The id cannot be null or not exist  {e}", type="error")
            self.db.Session().rollback()
            return app_utils.Response('error', f"Error creating goal {e}", 500)
        except Exception as e:
            app_utils.print_with_format(f"Error creating objective {e}", type="error")
            self.db.Session().rollback()
            return app_utils.Response('error', f"Error creating goal {e}", 500)      
        
    def get_objectives(self):
        """
        Gets all the objectives from the database.
        
        Returns:
            list: List of objectives.
        """
        try:
            result = self.db.Session().query(Objective).all()
            app_utils.print_with_format(f"Objectives retrieved successfully")
            return result
        except Exception as e:
            app_utils.print_with_format(f"Error retrieving objectives {e}", type="error")
            self.db.Session().rollback()
            return app_utils.Response('error', f"Error creating goal {e}", 500)    
        
    def get_objectives_by_goal(self, goal_id):
        """
        Gets all the objectives from the database by goal.
        
        Args:
            goal_id (str): The id of the goal.
        
        Returns:
            list: List of objectives.
        """
        try:
            result = self.db.Session().query(Objective).filter(Objective.goal_id == goal_id).all()
            app_utils.print_with_format(f"Objectives retrieved successfully")
            return result
        except Exception as e:
            app_utils.print_with_format(f"Error retrieving objectives {e}", type="error")
            self.db.Session().rollback()
            return app_utils.Response('error', f"Error creating goal {e}", 500) 