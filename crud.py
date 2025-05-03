from sqlalchemy.orm import Session
from . import models, schemas, auth
from fastapi import HTTPException, status
from sqlalchemy import func

▎*User
CRUD
operations *


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Create an empty profile for the user
    db_profile = models.UserProfile(user_id=db_user.id)
    db.add(db_profile)
    db.commit()

    return db_user

▎*Profile
CRUD
operations *


def get_user_profile(db: Session, user_id: int):
    return db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()


def update_user_profile(db: Session, user_id: int, profile: schemas.UserProfileUpdate):
    db_profile = get_user_profile(db, user_id)
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    profile_data = profile.dict(exclude_unset=True)
    for key, value in profile_data.items():
        setattr(db_profile, key, value)

    db.commit()
    db.refresh(db_profile)
    return db_profile

▎*BMI
Records
CRUD
operations *


def create_bmi_record(db: Session, bmi_record: schemas.BMIRecordCreate, user_id: int):
    # Calculate BMI
    bmi_value = bmi_record.weight_kg / (bmi_record.height_m ** 2)

    # Get the appropriate BMI category
    category = get_bmi_category(db, bmi_value)

    db_bmi_record = models.BMIRecord(
        user_id=user_id,
        weight_kg=bmi_record.weight_kg,
        height_m=bmi_record.height_m,
        bmi_value=bmi_value,
        category_id=category.id if category else None
    )
    db.add(db_bmi_record)
    db.commit()
    db.refresh(db_bmi_record)
    return db_bmi_record


def get_bmi_records(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.BMIRecord).filter(
        models.BMIRecord.user_id == user_id
    ).order_by(models.BMIRecord.created_at.desc()).offset(skip).limit(limit).all()


def get_bmi_record(db: Session, record_id: int, user_id: int):
    return db.query(models.BMIRecord).filter(
        models.BMIRecord.id == record_id,
        models.BMIRecord.user_id == user_id
    ).first()


def delete_bmi_record(db: Session, record_id: int, user_id: int):
    db_record = get_bmi_record(db, record_id, user_id)
    if not db_record:
        raise HTTPException(status_code=404, detail="BMI record not found")

    db.delete(db_record)
    db.commit()
    return {"message": "Record deleted successfully"}

▎*BMI
Category
operations *


def get_bmi_category(db: Session, bmi_value: float):
    return db.query(models.BMICategory).filter(
        models.BMICategory.min_value <= bmi_value,
        models.BMICategory.max_value > bmi_value
    ).first()


def get_bmi_categories(db: Session):
    return db.query(models.BMICategory).order_by(models.BMICategory.min_value).all()


def initialize_bmi_categories(db: Session):
    categories = [
        {
            "name": "Underweight (Severe thinness)",
            "min_value": 0,
            "max_value": 16,
            "description": "BMI less than 16",
            "health_risk": "Severe health risk",
            "recommendations": "Consult with healthcare provider for weight gain strategies"
        },
        {
            "name": "Underweight (Moderate thinness)",
            "min_value": 16,
            "max_value": 17,
            "description": "BMI between 16 and 17",
            "health_risk": "Moderate health risk",
            "recommendations": "Gradual, healthy weight gain recommended"
        },
        {
            "name": "Underweight (Mild thinness)",
            "min_value": 17,
            "max_value": 18.5,
            "description": "BMI between 17 and 18.5",
            "health_risk": "Mild health risk",
            "recommendations": "Consider adding more calories to your diet"
        },
        {
            "name": "Normal weight",
            "min_value": 18.5,
            "max_value": 25,
            "description": "BMI between 18.5 and 25",
            "health_risk": "Low risk",
            "recommendations": "Maintain healthy diet and regular exercise"
        },
        {
            "name": "Overweight (Pre-obese)",
            "min_value": 25,
            "max_value": 30,
            "description": "BMI between 25 and 30",
            "health_risk": "Enhanced risk",
            {
                "name": "Overweight (Pre-obese)",
                "min_value": 25,
                "max_value": 30,
                "description": "BMI between 25 and 30",
                "health_risk": "Enhanced risk",
                "recommendations": "Consider increasing physical activity and modifying diet"
            },
        {
            "name": "Obese (Class I)",
            "min_value": 30,
            "max_value": 35,
            "description": "BMI between 30 and 35",
            "health_risk": "Medium risk",
            "recommendations": "Consult healthcare provider; diet and exercise changes recommended"
        },
        {
            "name": "Obese (Class II)",
            "min_value": 35,
            "max_value": 40,
            "description": "BMI between 35 and 40",
            "health_risk": "High risk",
            "recommendations": "Seek medical advice for weight loss program"
        },
        {
            "name": "Obese (Class III)",
            "min_value": 40,
            "max_value": 100,  # Using a high upper bound
            "description": "BMI over 40",
            "health_risk": "Very high risk",
            "recommendations": "Immediate medical attention recommended"
        },
    ]

    # Check if categories already exist
    if db.query(models.BMICategory).count() == 0:
        for
    category in categories:
    db_category = models.BMICategory(**category)
    db.add(db_category)
    db.commit()

    return db.query(models.BMICategory).all()
