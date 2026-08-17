def bmi_report(weight_kg: float, height_cm: float) -> str:
    """回傳 "BMI 22.9 正常" 這種格式的字串。"""
    height_cm = height_cm/100
    bmi = round(weight_kg / (height_cm ** 2), 1)
    if bmi < 18.5:
        cate = "過輕"
    elif bmi < 24:
        cate = "正常"
    elif bmi < 27:
        cate = "過重"
    else:
        cate = "肥胖"
    return (f"BMI {bmi} {cate}")
