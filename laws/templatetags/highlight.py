from django import template
import re

register = template.Library()

@register.filter
def highlight(text, search):
    if not search:
        return text

    # Үгийн эхлэл таарсан үед highlight хийх
    pattern = re.compile(rf'\b({re.escape(search)})', re.IGNORECASE)

    return pattern.sub(
        r'<mark>\1</mark>',
        text
    )