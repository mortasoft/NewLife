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
from flask import jsonify

class Base(DeclarativeBase):
    pass

BASE_NAME = "goals"

@dataclass
class GoalModel(Base):
    __tablename__ = BASE_NAME + "_" +  'goal'
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=app_utils.generate_uuid)
    name: Mapped[str] = mapped_column(String(100), nullable=False, info={"example": "a1b2c3d4-e5f6-7890-1234-567890abcdef"})
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
            self.engine = engine
            
    def create_tables(self):
        """
        Create tables in the database.
        """
        Base.metadata.create_all(self.engine)
    
    def add_goal(self, name, description, date):
        """
        Adds a goal to the database.
        """
        with Session(self.engine) as session:
            new_goal = GoalModel(name=name, description=description, date=date)
            session.add(new_goal)
            session.flush()
            session.commit()
            return {'data': new_goal, 'message': app_utils.generate_message(new_goal,'create'), 'result': 'ok', 'status_code': 200}
    
    def get_goals(self):
        """
        Get all goals from the database.
        """
        with Session(self.engine) as session:
            goals = session.query(GoalModel).all()
            return {'data': goals, 'message': app_utils.generate_message(None,'get'), 'result': 'ok', 'status_code': 200}
        
    def get_goal(self, goal_id):
        """
        Get a goal by its ID.
        """
        with Session(self.engine) as session:
            goal = session.query(GoalModel).filter(GoalModel.id == goal_id).first()
            if goal:
                return {'data': goal, 'message': app_utils.generate_message(goal,'get'), 'result': 'ok', 'status_code': 200}
            else:
                return {'data': None, 'message': app_utils.generate_message(goal,'get'), 'result': 'error', 'status_code': 404}