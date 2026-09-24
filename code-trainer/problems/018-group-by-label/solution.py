def group_by_label(records: list[dict]) -> dict:
    """把標註依 label 分組，回傳 {label: [box, ...]}。"""
    # TODO: 只掃一遍 records
    pass
    result = {}
    for record in records:
        result.setdefault(record["label"], []).append(record["box"])
    return result
