def bmi_report(weight_kg: float, height_cm: float) -> str:
    """回傳 "BMI 22.9 正常" 這種格式的字串。"""
    # TODO: 1) 公分換公尺 2) 算 BMI 並四捨五入到小數第一位
    #       3) 依範圍決定分類 4) 用 f-string 組出結果
    height = height_cm / 100
    cate = ""
    bmi = round(weight_kg / (height ** 2), 1)
    if bmi < 18.5:
        cate = "過輕"
    elif bmi < 24:
        cate = "正常"
    elif bmi < 27:
        cate = "過重"
    else:
        cate = "肥胖"
    return f"BMI {bmi} {cate}"
