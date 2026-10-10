import logging
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import text

from database import get_db
from models import Citizen, CreateCitizen

app = FastAPI()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger(__name__)

@app.get("/")
def home():
    return {
        "message": "Developer.Punitha goes abraod for work .She lives and settle there "
    }


@app.get("/citizens")
def get_citizens(
    from_country: str | None = None,
    passport_status: str | None = None,
    limit: int = 2,
    offset: int = 0,
    db: Session = Depends(get_db)
    ):
    # query = """ SELECT * FROM citizens WHERE (:from_country IS NULL OR from_country = :from_country) AND (:passport_status IS NULL OR passport_status = :passport_status) LIMIT :limit OFFSET :offset """
    # result = db.execute( text(query), { "from_country": from_country, "passport_status": passport_status, "limit": limit, "offset": offset } ).mappings().all()
    # return [dict(row) for row in result] if result else {"message": "No citizen list found"}

    # SQLAlchmey Query
    query = db.query(Citizen)

    if from_country:
        query = query.filter(Citizen.from_country == from_country)

    if passport_status:
        query = query.filter(Citizen.passport_status == passport_status)

    result = query.limit(limit).offset(offset).all()

    if not result:
        return {"message":"No Citizen Found"}
    else:
        return result

    
# get api fetch by id - Path Params
@app.get("/citizen/{id}")
def get_citizen_id(
    id: int ,
    db: Session = Depends(get_db),
    status_code = status.HTTP_200_OK
    ):
    # Write normal SQL Query
    # result = db.execute(text("SELECT * FROM citizens WHERE citizen_id = :id"),{"id": id}).fetchone()
    # Below code for output from raw sql query
    # dict(result._mapping) if result else {"message": "Citizen not found"}
    try:
        SqlAchemelyResult = db.query(Citizen).get(id)
        print("SqlAchemelyResult",SqlAchemelyResult.citizen_id);
        db.commit()
        logging.info("Requested Citizen details fetched successfully")
        return {
            "success": True,
            "information": "Punithaa goes to aboard for work. Lives and settle there",
            "data": {
                "passport_number": SqlAchemelyResult.passport_number,
                    "citizen_name": SqlAchemelyResult.citizen_name,
                    "from_country": SqlAchemelyResult.from_country,
                    "living_country": SqlAchemelyResult.living_country,
                    "living_country_code": SqlAchemelyResult.living_country_code,
                    "citizenship_category": SqlAchemelyResult.citizenship_category,
                    "passport_status": SqlAchemelyResult.passport_status,
                    "type_of_visa": SqlAchemelyResult.type_of_visa,
                    "visa_expire_date": SqlAchemelyResult.visa_expire_date,
                    "purpose_stay": SqlAchemelyResult.purpose_stay
            }
        }
    except IntegrityError as exe:
        db.rollback()
        logging.error("Error in Database constrint")
        raise HTTPException(
            status_code= status.HTTP_409_CONFLICT,
            detail=f"Error in Database constraint : {exe}"
        ) from exe
    except SQLAlchemyError as exe:
        db.rollback()
        logging.error("Database operation failed")
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database operation failed : {exe}"
        ) from exe
    except Exception as exe:
        db.rollback()
        logging.error("Unexpected error as occured")
        raise HTTPException(
            status_code= status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error as occured : {exe}"
        ) from exe



# GET API - With Query Params
@app.get("/citizens")

@app.post("/citizen/add")
def addCitizen(
    CitizenData : CreateCitizen, 
    db: Session = Depends(get_db)
    ):

    # Query
    query = text("""
    INSERT INTO citizens (
    passport_number,
    citizen_name,
    from_country,
    living_country,
    living_country_code,
    citizenship_category,
    passport_status,
    type_of_visa,
    visa_expire_date,
    purpose_stay
    )
    VALUES (
    :passport_number,
    :citizen_name,
    :from_country,
    :living_country,
    :living_country_code,
    :citizenship_category,
    :passport_status,
    :type_of_visa,
    :visa_expire_date,
    :purpose_stay
    )
    """)

    RequestBody = {
    "passport_number": CitizenData.passport_number,
    "citizen_name": CitizenData.citizen_name,
    "from_country": CitizenData.from_country,
    "living_country": CitizenData.living_country,
    "living_country_code": CitizenData.living_country_code,
    "citizenship_category": CitizenData.citizenship_category,
    "passport_status": CitizenData.passport_status,
    "type_of_visa": CitizenData.type_of_visa,
    "visa_expire_date": CitizenData.visa_expire_date,
    "purpose_stay": CitizenData.purpose_stay
    }

    # Try execpt Block
    try:
        # result = db.execute(query,RequestBody)

        # SQLAlchemy
        citizen = Citizen(**CitizenData.model_dump())
        db.add(citizen)

        # if(citizen.rowcount) != 1:
        #     raise RuntimeError("Citizen insert did not affect one row")

        db.commit()
        db.refresh(citizen)
        logging.info("Citizen created successfully")

        return {
            "success": True,
            "message": "Citizen created successfully"
        }
    except IntegrityError as exc:
        db.rollback()
        # 409 - Database constraint
        logger.exception("Citizen creation failed due to a database constraint")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Citizen creation failed due to a database constraint: {exc}"
        ) from exc

    except SQLAlchemyError as exc:
        db.rollback()
        # 500 - Database operation Failed
        logger.exception("Database operation failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database operation failed: {exc}"
        ) from exc
    except Exception as exc:
        db.rollback()
        # 500 - An unexpected server error occurred.
        logger.exception("An unexpected server error occurred")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected server error occurred: {exc}"
        ) from exc

# Put API
@app.put("/citizen/updateData/{citizen_id}")
def update_citizen_data(
    citizen_id: int,
    citizen_data: CreateCitizen,
    db: Session = Depends(get_db),
):
    citizen = db.query(Citizen).filter(Citizen.citizen_id == citizen_id).first()
    if not citizen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Citizen not found"
        )

    for key, value in citizen_data.model_dump().items():
        setattr(citizen, key, value)

    try:
        db.commit()
        db.refresh(citizen)
        logging.info("Citizen updated successfully")
        return {
            "success": True,
            "message": "Citizen updated successfully",
            "data": citizen
        }
    except IntegrityError as exc:
        db.rollback()
        logger.exception("Citizen update failed due to a database constraint: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Citizen update failed due to a database constraint: {exc}"
        ) from exc
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("Database operation failed during citizen update")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database operation failed during citizen update: {exc}"
        ) from exc
    except Exception as exc:
        db.rollback()
        logger.exception("Unexpected error occurred while updating citizen")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error occurred while updating citizen: {exc}"
        ) from exc

# PATCH API


# DELETE API
# DELETE FROM Customers WHERE CustomerName='Alfreds Futterkiste';
@app.delete("/citizen/deleteData/{citizen_id}")
def remove_citizen(
    citizen_id: int,
    db: Session = Depends(get_db)
):
    # Raw SQL
    query = db.execute(text(
        "DELETE FROM citizens WHERE citizen_id = :citizen_id"
    ),{"citizen_id": citizen_id}
    )

    # SQL Alchemy
    record = db.query(Citizen).get(citizen_id)
    db.delete(record)
    return {
        "message":"Data Deleted SuccessFully",
        "citizen_id": citizen_id
        }