import calendar
from datetime import date
from itertools import groupby

from django import template
from django.utils.html import conditional_escape as esc

register = template.Library()

def do_menu_calendar(parser, token):
    """
    The template tag's syntax is {% menu_calendar year month meal_list [show_details] %}
    """
    tokens = token.split_contents()
    if len(tokens) < 4:
        raise template.TemplateSyntaxError, "%r tag requires three arguments" % token.contents.split()[0]
    year, month, meal_list = tokens[1:4]
    try:
        show_details = (tokens[4] == 'True')
    except:
        show_details = True
    return MenuCalendarNode(year, month, meal_list, show_details=show_details)


class MenuCalendarNode(template.Node):
    """
    Process a particular node in the template. Fail silently.
    """
    def __init__(self, year, month, meal_list, show_details=True):
        try:
            self.year = template.Variable(year)
            self.month = template.Variable(month)
            self.meal_list = template.Variable(meal_list)
            self.show_details = show_details
        except ValueError:
            raise template.TemplateSyntaxError

    def render(self, context):
        try:
            my_meal_list = self.meal_list.resolve(context)
            my_year = self.year.resolve(context)
            my_month = self.month.resolve(context)
            cal = MenuCalendar(my_meal_list, self.show_details)
            return cal.formatmonth(int(my_year), int(my_month))
        except ValueError:
            return ''
        except template.VariableDoesNotExist:
            return ''

class MenuCalendar(calendar.HTMLCalendar):
    """
    Overload Python's calendar.HTMLCalendar to add the appropriate meals to
    each day's table cell.
    """

    def __init__(self, meals, show_details):
        super(MenuCalendar, self).__init__()
        self.meals = self.group_by_day(meals)
        self.show_details = show_details

    def formatweekday(self, day):
        if day in (5, 6):
            # ignore weekends
            return ''
        return super(MenuCalendar, self).formatweekday(day)

    def formatday(self, day, day_of_week):
        if day_of_week in (5, 6):
            # ignore weekends
            return ''
        if not day:
            return self.day_cell('noday', '&nbsp;')

        cssclass = self.cssclasses[day_of_week]
        if date.today() == date(self.year, self.month, day):
            cssclass += ' today'
        if day in self.meals:
            cssclass += ' filled'
            body = []
            if self.show_details:
                body = self.day_details_body(self.meals[day])
                return self.day_cell(cssclass, '<span class="day-number">%d</span> %s' % (day, ''.join(body)))
            else:
                return self.day_cell(cssclass, '<span class="day-number"><a href="%s">%d</a></span>' % (self.meals[day][0].get_absolute_url(), day))
        else:
            return self.day_cell(cssclass, '<span class="day-number no-meals">%d</span>' % (day))

    def day_details_body(self, objects):
        body = []
        body.append('<ul class="dishes">')
        for meal in objects:
            for dish in meal.dishes.all():
                body.append('<li>')
                body.append('<a href="%s">' % dish.get_absolute_url())
                body.append(esc(dish.name))
                body.append('</a>')
                body.append('</li>')
        body.append('</ul>')
        return body

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(MenuCalendar, self).formatmonth(year, month)

    def group_by_day(self, meals):
        field = lambda m: m.date.day
        return dict(
            [(day, list(items)) for day, items in groupby(meals, field)]
        )

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)

# Register the template tag so it is available to templates
register.tag("menu_calendar", do_menu_calendar)
