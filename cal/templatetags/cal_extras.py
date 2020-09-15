import calendar
import datetime
from django import template
from django.utils.safestring import mark_safe
from cal.utils import YearCustomHTMLCal, MonthCustomHTMLCal

from ..models import Event

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
    now = datetime.datetime.now()
    year = context.get('year') or now.year
    month = context.get('month') or now.month
    events = context.get('object_list') or Event.objects.available(context['request'])
    cal = MonthCustomHTMLCal(events=events)
    return mark_safe(cal.formatmonth(year, month))
