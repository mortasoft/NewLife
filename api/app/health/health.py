import sys,os
from health.db import *
from dataclasses import dataclass
import utils as app_utils

BASE_NAME = "health"

@dataclass
class Weight(Base):
    __tablename__ = BASE_NAME + "_" +  'weight'
    
    id: str
    date: str
    weight: float
    imc: float
    bodyFat: float
    subcutaneousFat: float
    viseralFat: float
    muscleMass: float
        
    id = Column("id", String(36), primary_key=True, default=generate_uuid)
    date = Column("date", Date())
    weight = Column("weight", Numeric(5,2))
    imc = Column("imc", Numeric(5,2))
    bodyFat = Column("body_fat", Numeric(5,2))
    subcutaneousFat = Column("subcutaneous_fat", Numeric(5,2))
    viseralFat = Column("viseral_fat", Numeric(5,2))
    muscleMass = Column("muscle_mass", Numeric(5,2))
    
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

   
class Health():
    def __init__(self,db) -> None:
        try:
            self.session = db.session
            app_utils.print_with_format(f"The database session was assigned successfully to the {BASE_NAME} class.")
        except Exception as e:
            app_utils.print_with_format_error(f"Error creating session in {BASE_NAME} class {e}")    
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
            self.session.add(new)
            self.session.commit()
            app_utils.print_with_format(f"Weight log {new} created successfully")
        except Exception as e:
            app_utils.print_with_format_error(f"Error creating activity log {new}")
            self.session.rollback()
            raise
        finally:
            self.session.close()       
        
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