from django import template

register = template.Library()

PERSIAN_DIGITS = {
    "0": "۰",
    "1": "۱",
    "2": "۲",
    "3": "۳",
    "4": "۴",
    "5": "۵",
    "6": "۶",
    "7": "۷",
    "8": "۸",
    "9": "۹",
}

@register.filter
def persian_numbers(value):
    if not isinstance(value, str):
        value = str(value)
    return ''.join(PERSIAN_DIGITS.get(ch, ch) for ch in value)
