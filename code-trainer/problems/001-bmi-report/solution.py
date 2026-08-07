def bmi_report(weight_kg: float, height_cm: float) -> str:
    """回傳 "BMI 22.9 正常" 這種格式的字串。"""
    # TODO: 1) 公分換公尺 2) 算 BMI 並四捨五入到小數第一位
    #       3) 依範圍決定分類 4) 用 f-string 組出結果
    bmi = weight_kg/((height_cm / 100) ** 2)
    if bmi < 18.5:
        bmi_case = "過輕"
    elif bmi < 24:
        bmi_case = "正常"
    elif bmi < 27:
        bmi_case = "過重"
    else:
        bmi_case = "肥胖"
    
    return f"BMI {bmi:.1f} {bmi_case}"
    pass
