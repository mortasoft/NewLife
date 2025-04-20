from datetime import date
from typing import List, Optional, Dict, Any
from sqlalchemy import ForeignKey, String, Integer, Date, Boolean, Float, Index, event
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates, Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import SQLAlchemyError
import logging
from enum import Enum
from dataclasses import dataclass
from contextlib import contextmanager
import utils as app_utils

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base configuration
Base = declarative_base()
BASE_NAME = "goals"

class GoalStatus(Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    
@dataclass
class ModelConfig:
    NAME_MAX_LENGTH: int = 100
    DESCRIPTION_MAX_LENGTH: int = 500
    VALID_CURRENCIES: tuple = ("USD", "EUR", "CRC")

class GoalModel(Base):
    __tablename__ = f"{BASE_NAME}_goal"
    __table_args__ = (
        Index('idx_goal_date', 'date'),
        Index('idx_goal_status', 'status'),
    )
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: app_utils.generate_uuid())
    name: Mapped[str] = mapped_column(String(ModelConfig.NAME_MAX_LENGTH), nullable=False)
    description: Mapped[str] = mapped_column(String(ModelConfig.DESCRIPTION_MAX_LENGTH), nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), 
        default=GoalStatus.PENDING.value,
        nullable=False
    )
    
    objectives: Mapped[List["ObjectiveModel"]] = relationship(
        back_populates="goal",
        cascade="all, delete-orphan",
        lazy="select"
    )
    
    @validates('date')
    def validate_date(self, key: str, value: Date) -> Date:
        if value < date.today():
            raise ValueError("Goal date cannot be in the past")
        return value
    
    @validates('status')
    def validate_status(self, key: str, value: str) -> str:
        if value not in [status.value for status in GoalStatus]:
            raise ValueError(f"Invalid status. Must be one of: {', '.join(status.value for status in GoalStatus)}")
        return value
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            "date": self.date,
            'status': self.status,
            'objectives': [obj.to_dict() for obj in self.objectives]
        }
    
    def __repr__(self) -> str:
        return f"Goal(id={self.id}, name={self.name}, status={self.status})"


class ObjectiveModel(Base):
    __tablename__ = f"{BASE_NAME}_objective"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: app_utils.generate_uuid())
    name: Mapped[str] = mapped_column(String(ModelConfig.NAME_MAX_LENGTH))
    description: Mapped[str] = mapped_column(String(ModelConfig.DESCRIPTION_MAX_LENGTH))
    
    # Type-specific fields
    start_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    end_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_boolean: Mapped[bool] = mapped_column(Boolean, default=False)
    start_value: Mapped[Optional[float]] = mapped_column(Float(10, 2), nullable=True)
    end_value: Mapped[Optional[float]] = mapped_column(Float(10, 2), nullable=True)
    currency_unit: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    
    goal_id: Mapped[str] = mapped_column(String(36), ForeignKey(f"{BASE_NAME}_goal.id"), nullable=False)
    goal: Mapped["GoalModel"] = relationship("GoalModel", back_populates="objectives")
    
    @validates('currency_unit')
    def validate_currency(self, key: str, value: Optional[str]) -> Optional[str]:
        if value and value not in ModelConfig.VALID_CURRENCIES:
            raise ValueError(f"Invalid currency. Must be one of: {', '.join(ModelConfig.VALID_CURRENCIES)}")
        return value
    
    def validate_objective_type(self) -> None:
        type_count = sum([
            bool(self.start_number is not None or self.end_number is not None),
            bool(self.is_boolean),
            bool(self.start_value is not None or self.end_value is not None)
        ])
        if type_count != 1:
            raise ValueError("Exactly one type of objective must be specified")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_number': self.start_number,
            'end_number': self.end_number,
            'is_boolean': self.is_boolean,
            'start_value': float(self.start_value) if self.start_value else None,
            'end_value': float(self.end_value) if self.end_value else None,
            'currency_unit': self.currency_unit,
            'goal_id': self.goal_id
        }
    
    def __repr__(self) -> str:
        return f"[Objective Name={self.name}, Description={self.description}, Start Number={self.start_number}, End Number={self.end_number}, Is Boolean={self.is_boolean}, Start Value={self.start_value}, End Value={self.end_value}, Currency Unit={self.currency_unit}]"

   
class GoalManager:
    def __init__(self, engine) -> None:
        self.engine = engine
        
    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = Session(self.engine)
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database error: {str(e)}")
            raise
        finally:
            session.close()
    
    def create_tables(self) -> None:
        """Create all database tables."""
        try:
            Base.metadata.create_all(self.engine)
            logger.info("Database tables created successfully")
        except SQLAlchemyError as e:
            logger.error(f"Error creating database tables: {str(e)}")
            raise
    
    def add_goal(self, name: str, description: str, date: Date, status: str) -> Dict[str, Any]:
        """Add a new goal to the database."""
        try:
            with self.session_scope() as session:
                new_goal = GoalModel(
                    name=name,
                    description=description,
                    date=date,
                    status=status
                )
                session.add(new_goal)
                session.flush()
                result = new_goal.to_dict()
                
            return {
                'data': result,
                'message': app_utils.generate_message("Goal", 'create'),
                'result': 'ok',
                'status_code': 201
            }
        except Exception as e:
            logger.error(f"Error adding goal: {str(e)}")
            return {
                'data': None,
                'message': f"Error adding goal: {str(e)}",
                'result': 'error',
                'status_code': 400
            }
    
    def get_goals(self) -> Dict[str, Any]:
        """Retrieve all goals from the database."""
        try:
            with self.session_scope() as session:
                goals = session.query(GoalModel).all()
                result = [goal.to_dict() for goal in goals]
                
            return {
                'data': result,
                'message': app_utils.generate_message(None, 'get'),
                'result': 'ok',
                'status_code': 200
            }
        except Exception as e:
            logger.error(f"Error retrieving goals: {str(e)}")
            return {
                'data': None,
                'message': str(e),
                'result': 'error',
                'status_code': 500
            }
    
    def get_goal(self, goal_id: str) -> Dict[str, Any]:
        """Retrieve a specific goal by ID."""
        try:
            with self.session_scope() as session:
                goal = session.query(GoalModel).filter(GoalModel.id == goal_id).first()
                if not goal:
                    return {
                        'data': None,
                        'message': app_utils.generate_message(None, 'id_not_found'),
                        'result': 'error',
                        'status_code': 404
                    }
                
                result = goal.to_dict()
                
            return {
                'data': result,
                'message': app_utils.generate_message(None, 'get'),
                'result': 'ok',
                'status_code': 200
            }
        except Exception as e:
            logger.error(f"Error retrieving goal {goal_id}: {str(e)}")
            return {
                'data': None,
                'message': str(e),
                'result': 'error',
                'status_code': 500
            }
    
    def add_objective(
        self,
        name: str,
        description: str,
        goal_id: str,
        start_number: Optional[int] = None,
        end_number: Optional[int] = None,
        is_boolean: bool = False,
        start_value: Optional[float] = None,
        end_value: Optional[float] = None,
        currency_unit: Optional[str] = None
    ) -> Dict[str, Any]:
        """Add a new objective to a goal."""
        try:
            with self.session_scope() as session:
                # Verify goal exists
                goal = session.query(GoalModel).filter(GoalModel.id == goal_id).first()
                if not goal:
                    raise ValueError(f"Goal with id {goal_id} not found")
                
                new_objective = ObjectiveModel(
                    name=name,
                    description=description,
                    goal_id=goal_id,
                    start_number=start_number,
                    end_number=end_number,
                    is_boolean=is_boolean,
                    start_value=start_value,
                    end_value=end_value,
                    currency_unit=currency_unit
                )
                
                # Validate objective type
                #new_objective.validate_objective_type()
                
                session.add(new_objective)
                session.flush()
                result = new_objective.to_dict()
                
            return {
                'data': result,
                'message': app_utils.generate_message("Objective", 'create'),
                'result': 'ok',
                'status_code': 200
            }
        except Exception as e:
            logger.error(f"Error adding objective: {str(e)}")
            return {
                'data': None,
                'message': str(e),
                'result': 'error',
                'status_code': 400
            }

# Event listeners for logging
@event.listens_for(GoalModel, 'after_insert')
def log_goal_creation(mapper, connection, target):
    logger.info(f"New goal created: {target.name}")

@event.listens_for(ObjectiveModel, 'after_insert')
def log_objective_creation(mapper, connection, target):
    logger.info(f"New objective created: {target.name} for goal {target.goal_id}")