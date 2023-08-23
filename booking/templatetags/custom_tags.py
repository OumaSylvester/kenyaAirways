from django import template
from datetime import datetime


register = template.Library()

@register.filter
def unique_times(schedule, unique_times_set):
    times = schedule.times.all()
    unique_times = [time for time in times if time not in unique_times_set]
    unique_times_set.update(unique_times)
    return unique_times


@register.simple_tag
def today():
    return datetime.today()
