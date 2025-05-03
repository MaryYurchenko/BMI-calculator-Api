def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """
    Calculate BMI using the formula: weight (kg) / height^2 (m)
    """
    if weight_kg <= 0 or height_m <= 0:
        raise ValueError("Weight and height must be positive values")

    return weight_kg / (height_m ** 2)


def get_bmi_category_info(bmi_value: float) -> dict:
    """
    Determine BMI category and provide recommendations based on the BMI value.
    This function is simplified and would use the database categories in practice.
    """
    if bmi_value < 16:
        return {
            "category": "Underweight (Severe thinness)",
            "description": "BMI less than 16",
            "health_risk": "Severe health risk",
            "recommendations": "Consult with healthcare provider for weight gain strategies"
        }
    elif bmi_value < 17:
        return {
            "category": "Underweight (Moderate thinness)",
            "description": "BMI between 16 and 17",
            "health_risk": "Moderate health risk",
            "recommendations": "Gradual, healthy weight gain recommended"
        }
    # ... and so on with other categories
    elif bmi_value < 18.5:
        return {
            "category": "Underweight (Mild thinness)",
            "description": "BMI between 17 and 18.5",
            "health_risk": "Mild health risk",
            "recommendations": "Consider adding more calories to your diet"
        }
    elif bmi_value < 25:
        return {
            "category": "Normal weight",
            "description": "BMI between 18.5 and 25",
            "health_risk": "Low risk",
            "recommendations": "Maintain healthy diet and regular exercise"
        }
    elif bmi_value < 30:
        return {
            "category": "Overweight (Pre-obese)",
            "description": "BMI between 25 and 30",
            "health_risk": "Enhanced risk",
            "recommendations": "Consider increasing physical activity and modifying diet"
        }
    elif bmi_value < 35:
        return {
            "category": "Obese (Class I)",
            "description": "BMI between 30 and 35",
            "health_risk": "Medium risk",
            "recommendations": "Consult healthcare provider; diet and exercise changes recommended"
        }
    elif bmi_value < 40:
        return {
            "category": "Obese (Class II)",
            "description": "BMI between 35 and 40",
            "health_risk": "High risk",
            "recommendations": "Seek medical advice for weight loss program"
        }
    else:
        return {
            "category": "Obese (Class III)",
            "description": "BMI over 40",
            "health_risk": "Very high risk",
            "recommendations": "Immediate medical attention recommended"
        }
