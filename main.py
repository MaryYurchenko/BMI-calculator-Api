from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from typing import Optional

app = FastAPI(title="BMI Calculator API",
              description="API для расчета индекса массы тела (BMI)",
              version="1.0.0")


class BMIInput(BaseModel):
    height: float = Field(..., gt=0, description="Рост в сантиметрах")
    weight: float = Field(..., gt=0, description="Вес в килограммах")

    @validator('height')
    def height_must_be_reasonable(cls, v):
        if v < 50 or v > 300:
            raise ValueError('Рост должен быть в диапазоне от 50 до 300 см')
        return v

    @validator('weight')
    def weight_must_be_reasonable(cls, v):
        if v < 2 or v > 700:
            raise ValueError('Вес должен быть в диапазоне от 2 до 700 кг')
        return v


class BMIOutput(BaseModel):
    bmi: float
    category: str
    height: float
    weight: float


class UserProfile(BaseModel):
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    bmi_data: BMIOutput


class UserDatabase:
    def __init__(self):
        self.users = {}

    def add_user(self, user_id: str, profile: UserProfile):
        self.users[user_id] = profile

    def get_user(self, user_id: str):
        if user_id not in self.users:
            return None
        return self.users[user_id]


user_db = UserDatabase()


def calculate_bmi(height: float, weight: float) -> float:
    """
    Рассчитывает BMI по формуле: вес (кг) / (рост (м) ^ 2)
    """
    height_m = height / 100  # конвертация из см в метры
    return round(weight / (height_m ** 2), 1)


def get_bmi_category(bmi: float) -> str:
    """
    Определяет категорию BMI
    """
    if bmi < 16:
        return "Выраженный дефицит массы тела"
    elif bmi < 18.5:
        return "Недостаточная масса тела"
    elif bmi < 25:
        return "Нормальная масса тела"
    elif bmi < 30:
        return "Избыточная масса тела"
    elif bmi < 35:
        return "Ожирение I степени"
    elif bmi < 40:
        return "Ожирение II степени"
    else:
        return "Ожирение III степени"


@app.get("/")
async def root():
    return {"message": "Добро пожаловать в API для расчета BMI"}


@app.post("/calculate_bmi", response_model=BMIOutput)
async def calculate_bmi_endpoint(data: BMIInput):
    bmi = calculate_bmi(data.height, data.weight)
    category = get_bmi_category(bmi)

    return BMIOutput(
        bmi=bmi,
        category=category,
        height=data.height,
        weight=data.weight
    )


@app.post("/users/{user_id}")
async def create_user(user_id: str, profile: UserProfile):
    if user_db.get_user(user_id):
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    user_db.add_user(user_id, profile)
    return {"message": f"Пользователь {user_id} создан успешно"}


@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user = user_db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return user
