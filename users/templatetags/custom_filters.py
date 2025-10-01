from django import template
from datetime import datetime, timedelta
from django.utils import timezone

register = template.Library()

@register.filter
def humanized_date(value):
    if value:
        today = datetime.now(timezone.get_current_timezone()).date()
        value_local = timezone.localtime(value)
        value_date = value_local.date()

        yesterday = today - timedelta(days=1)

        if value_date == today:
            return f"Today at {value.strftime('%I:%M %p')}"
        elif value_date == yesterday:
            return f"Yesterday at {value_date.strftime('%I:%M %p')}"
        elif value_date.year == today.year:
            return value_date.strftime('%B %d at %I:%M %p')
        else:
            return value_date.strftime('%B %d, %Y at %I:%M %p')
    return ''