import calendar
from django import template
from django.utils.safestring import mark_safe
from cal.utils import YearCustomHTMLCal, MonthCustomHTMLCal

register = template.Library()


@register.filter
def month_name(num):
    return calendar.month_name[num]
    

@register.simple_tag(takes_context=True)
def get_year_calendar(context):
    year = context['year']
    events = context['object_list']
    cal = YearCustomHTMLCal(events=events)
    return mark_safe(cal.formatyear(year))


@register.simple_tag(takes_context=True)
def get_month_calendar(context):
    year = context['year']
    month = context['month']
    events = context['object_list']
    cal = MonthCustomHTMLCal(events=events)
    return mark_safe(cal.formatmonth(year, month))
