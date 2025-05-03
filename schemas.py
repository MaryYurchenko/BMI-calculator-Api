from pydantic import BaseModel, validator, Field
from datetime import datetime
from typing import Optional, List


# User schemas
class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


# User Profile schemas
class UserProfileBase(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(UserProfileBase):
    pass


class UserProfile(UserProfileBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


# BMI Record schemas
class BMIRecordBase(BaseModel):
    weight_kg: float = Field(..., gt=0)
    height_m: float = Field(..., gt=0)

    @validator('height_m')
    def height_must_be_reasonable(cls, v):
        if v > 3:
            raise ValueError('Height seems too large. Please enter height in meters.')
        return v


class BMIRecordCreate(BMIRecordBase):
    pass


class BMIRecord(BMIRecordBase):
    id: int
    user_id: int
    bmi_value: float
    created_at: datetime

    class Config:
        orm_mode = True


# BMI Category schemas
class BMICategory(BaseModel):
    id: int
    name: str
    min_value: float
    max_value: float
    description: str
    health_risk: str
    recommendations: str

    class Config:
        orm_mode = True


# BMI calculation response
class BMICalculationResult(BaseModel):
    bmi: float
    category: str
    description: str
    health_risk: str
    recommendations: str


# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
