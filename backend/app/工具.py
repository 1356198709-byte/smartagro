# 工具.py — 中俄双语翻译工具（主要代码）

def tr(obj, lang: str, field_map: dict):
    """若 lang=ru 且有 _ru 字段值，则替换主字段值"""
    if lang != "ru":
        return
    for zh_field, ru_field in field_map.items():
        ru_val = getattr(obj, ru_field, None)
        if ru_val:
            setattr(obj, zh_field, ru_val)


def tr_dict(d: dict, lang: str, field_map: dict):
    """字典版本"""
    if lang != "ru":
        return
    for zh_key, ru_key in field_map.items():
        if d.get(ru_key):
            d[zh_key] = d[ru_key]
