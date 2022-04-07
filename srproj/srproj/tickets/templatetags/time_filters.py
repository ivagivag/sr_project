from django import template

register = template.Library()


@register.filter()
def hr_timedelta(value):
    """Convert a datetime.timedelta object into Days, Hours and Minutes"""
    secs = value.total_seconds()
    result = ""
    sec_per_day = 60 * 60 * 24
    if secs > sec_per_day:
        days = int(secs // sec_per_day)
        result += f"{days} day"
        if days > 1:
            result += 's'
        secs -= days * sec_per_day
    sec_per_hour = 60 * 60
    if secs > sec_per_hour:
        hrs = int(secs // sec_per_hour)
        result += f" {hrs} hour"
        if hrs > 1:
            result += 's'
        secs -= hrs * sec_per_hour
    sec_per_min = 60
    if secs > sec_per_min:
        mins = int(secs // sec_per_min)
        result += f" {mins} minute"
        if mins > 1:
            result += 's'

    return result
