from django import template
from django.utils import timezone
from datetime import datetime

register = template.Library()

@register.filter(name='time_until')
def time_until(value):
    if not value:
        return "No due date"
    
    now = timezone.now()
    time_diff = value - now

    if time_diff.total_seconds() < 0:
        return "Overdue"

    days = time_diff.days
    hours, remainder = divmod(time_diff.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    if days > 0:
        return f"{days} days left"
    elif hours > 0:
        return f"{hours} hours left"
    elif minutes > 0:
        return f"{minutes} minutes left"
    else:
        return "Due soon"