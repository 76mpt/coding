def bmi_report(weight_kg: float, height_cm: float) -> str:
    """回傳 "BMI 22.9 正常" 這種格式的字串。"""
    bmi = round(weight_kg / (height_cm * height_cm / 100 / 100), 1)
    if bmi < 18.5:
        return f"BMI {bmi} 過輕"
    elif bmi < 24:
        return f"BMI {bmi} 正常"
    elif bmi < 27:
        return f"BMI {bmi} 過重"
    else:
        return f"BMI {bmi} 肥胖"
