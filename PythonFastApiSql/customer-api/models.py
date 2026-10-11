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

class patchCitizen(BaseModel):
    passport_number: str | None = None
    citizen_name: str | None = None
    from_country: str | None = None
    living_country: str | None = None
    living_country_code: str | None = None
    citizenship_category: str | None = None
    passport_status: str | None = None
    type_of_visa: str | None = None
    visa_expire_date: str | None = None
    purpose_stay : str | None = None