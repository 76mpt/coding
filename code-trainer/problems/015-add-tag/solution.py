def add_tag(tag, tags=None):
    """把 tag 加進 tags；沒給 tags 就建一個新的 list。"""
    if tags is None:
        tags = []
    tags.append(tag)
    return tags