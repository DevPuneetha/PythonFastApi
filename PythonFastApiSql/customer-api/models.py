from sqlalchemy import Column, Integer, String, Date
from database import Base
from pydantic import BaseModel


class Citizen(Base):
    __tablename__ = "citizens"

    citizen_id = Column(Integer, primary_key=True, index=True)
    passport_number = Column(String(50), nullable=False)
    citizen_name = Column(String(100), nullable=False)
    from_country = Column(String(100))
    living_country = Column(String(100))
    living_country_code = Column(String(10))
    citizenship_category = Column(String(50))
    passport_status = Column(String(50))
    type_of_visa = Column(String(50))
    visa_expire_date = Column(Date)
    purpose_stay = Column(String(255))

class CreateCitizen(BaseModel):
    passport_number: str
    citizen_name: str
    from_country: str
    living_country: str
    living_country_code: str
    citizenship_category: str
    passport_status: str
    type_of_visa: str
    visa_expire_date: str
    purpose_stay : str