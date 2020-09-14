import calendar
import datetime
import random
import string


class YearCustomHTMLCal(calendar.HTMLCalendar):
    cssclasses = [style + " center aligned" for style in
                  calendar.HTMLCalendar.cssclasses]
    cssclass_month_head = "center aligned"
    cssclass_year_head = "center aligned"
    cssclass_year = "ui table"
    
    def __init__(self, events, *args, **kwargs):
        super(YearCustomHTMLCal, self).__init__(*args, **kwargs)
        self.events = events
        self.current_date = datetime.date(1, 1, 1)

    def formatyear(self, theyear, width=3):
        v = []
        a = v.append
        width = max(width, 1)
        a(f'<table border="0" cellpadding="0" cellspacing="0" class="{self.cssclass_year}">')
        a('\n')
        a(f'<thead><tr><th colspan="{width}" class="{self.cssclass_year_head}">{theyear}</th></tr></thead>\n')
        a('<tbody>')
        for i in range(1, 13, width):
            # months in this row
            months = range(i, min(i+width, 13))
            a('<tr>')
            for m in months:
                a('<td>')
                a(self.formatmonth(theyear, m, withyear=False))
                a('</td>')
            a('</tr>')
        a('</tbody>')
        a('</table>')
        return ''.join(v)

    def formatmonthname(self, theyear, themonth, withyear=True):
        if withyear:
            s = f'{calendar.month_name[themonth]} {theyear}'
        else:
            s = '%s' % calendar.month_name[themonth]
        return f'''
        <tr>
            <th colspan="7" class="{self.cssclass_month_head}">
                <a href=".?year={theyear}&month={themonth}">{s}</a>
            </th>
        </tr>
        '''

    def formatmonth(self, year, month, withyear):
        self.current_date = datetime.date(year, month, 1)
        result = super().formatmonth(year, month, withyear)
        return result

    def formatday(self, day, weekday):
        self.current_date = datetime.date(
                                self.current_date.year,
                                self.current_date.month, 
                                day if day != 0 else 1
                            )
                            
        if day == 0:
            return '<td class="%s">&nbsp;</td>' % self.cssclass_noday
        else:
            event = False
            for e in self.events:
                if e.date == self.current_date:
                    event = True
                    break

            return f'''
            <td class="{self.cssclasses[weekday]}">
                <a href=".{create_url_from_date(self.current_date)}">
                    <span style="color: {"red" if event else ""}">{day}</span>
                </a>
            </td>
            '''


class MonthCustomHTMLCal(calendar.HTMLCalendar):
    cssclasses = [style + "center aligned" for style in
                  calendar.HTMLCalendar.cssclasses]
    cssclass_month_head = "center aligned"
    cssclass_month = "ui celled fixed table"
    cssclasses_weekday_head = ["center aligned" for _ in calendar.HTMLCalendar.cssclasses_weekday_head]

    def __init__(self, events, *args, **kwargs):
        super(MonthCustomHTMLCal, self).__init__(*args, **kwargs)
        self.events = events
        self.current_date = datetime.date(1, 1, 1)

    def formatmonthname(self, theyear, themonth, withyear=True):
        if withyear:
            s = f'''
                {calendar.month_name[themonth]}
                <a href=".?year={theyear}">
                     {theyear}
                </a>
            '''
        else:
            s = '%s' % calendar.month_name[themonth]
        prev_month = 12 if themonth == 1 else themonth - 1
        next_month = 1 if themonth == 12 else themonth + 1
        prev_year = theyear - 1 if themonth == 1 else theyear
        next_year = theyear + 1 if themonth == 12 else theyear
        return f'''
        <tr>
            <th class="{self.cssclass_month_head}">
                <a href=".?year={prev_year}&month={prev_month}">{calendar.month_name[prev_month]}</a>
            </th>
            <th colspan="5" class="{self.cssclass_month_head}">
                {s}
            </th>
            <th class="{self.cssclass_month_head}">
                <a href=".?year={next_year}&month={next_month}">{calendar.month_name[next_month]}</a>
            </th>
        </tr>
        '''

    def formatmonth(self, year, month, withyear=True):
        self.current_date = datetime.date(year, month, 1)
        """
               Return a formatted month as a table.
               """
        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="%s">' % (
            self.cssclass_month))
        a('\n')
        a('<thead>\n')
        a(self.formatmonthname(year, month, withyear=withyear))
        a('\n')
        a('</thead>\n')
        a(self.formatweekheader())
        a('\n')
        a('<tbody>\n')
        for week in self.monthdays2calendar(year, month):
            a(self.formatweek(week))
            a('\n')
        a('</tbody>\n')
        a('</table>')
        a('\n')
        return ''.join(v)

    def formatday(self, day, weekday):
        self.current_date = datetime.date(
            self.current_date.year,
            self.current_date.month,
            day if day != 0 else 1
        )

        if day == 0:
            return '<td class="%s">&nbsp;</td>' % self.cssclass_noday
        else:
            event = False
            for e in self.events:
                if e.date == self.current_date:
                    event = True
                    break

            return f'''
            <td class="{self.cssclasses[weekday]}">
                <a href=".{create_url_from_date(self.current_date)}">
                    <span style="color: {"red" if event else ""}">{day}</span>
                </a>
            </td>
            '''


def create_url_from_date(date):
    args = {
        'year': date.year,
        'month': date.month,
        'day': date.day
    }
    return create_url_get_args(args)


def create_url_get_args(args):
    get_attrs = '?'
    for k, v in args.items():
        get_attrs += f'{k}={v}&'
    return get_attrs[:-1]


def random_string_generator(length=10):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def token_generator(instance, new_token=None):
    if new_token:
        token = new_token
    else:
        token = random_string_generator()
    klass = instance.__class__
    qs = klass.objects.filter(token=token)
    if qs.exists():
        new_token = f'{token}{random_string_generator(2)}'
        return token_generator(instance, new_token)
    return token
