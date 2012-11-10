import calendar
from datetime import date
from itertools import groupby

from django import template
from django.utils.html import conditional_escape as esc

register = template.Library()

def do_menu_calendar(parser, token):
    """
    The template tag's syntax is {% menu_calendar year month meal_list [show_details] [show_school_type_labels] %}
    """
    tokens = token.split_contents()
    print tokens

    if len(tokens) < 4:
        raise template.TemplateSyntaxError, "%r tag requires three arguments" % token.contents.split()[0]
    year, month, meal_list = tokens[1:4]
    try:
        show_details = (tokens[4] == 'True')
    except:
        show_details = True
    try:
        show_school_type_labels = (tokens[5] == 'True')
    except:
        show_school_type_labels = False
    print 'show_school_type_labels:', show_school_type_labels
    return MenuCalendarNode(year, month, meal_list, show_details=show_details,
                            show_school_type_labels=show_school_type_labels)


class MenuCalendarNode(template.Node):
    """
    Process a particular node in the template. Fail silently.
    """
    def __init__(self, year, month, meal_list, show_details=True, 
                 show_school_type_labels=False):
        try:
            self.year = template.Variable(year)
            self.month = template.Variable(month)
            self.meal_list = template.Variable(meal_list)
            self.show_details = show_details
            self.show_school_type_labels = show_school_type_labels
        except ValueError:
            raise template.TemplateSyntaxError

    def render(self, context):
        print 'rendering:', self.show_school_type_labels
        try:
            my_meal_list = self.meal_list.resolve(context)
            my_year = self.year.resolve(context)
            my_month = self.month.resolve(context)
            cal = MenuCalendar(my_meal_list, self.show_details,
                               self.show_school_type_labels)
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

    def __init__(self, meals, show_details, show_school_type_labels):
        super(MenuCalendar, self).__init__()
        self.meals = self.group_by_day(meals)
        self.show_details = show_details
        self.show_school_type_labels = show_school_type_labels

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
            body.append('<li class="school-type">')
            if self.show_school_type_labels:
                body.append('<span>%s</span>' % meal.get_school_type_display())
            body.append('<ul>')
            for dish in meal.dishes.all().order_by('name'):
                body.append('<li>')
                body.append('<a href="%s?date=%s">' % (dish.get_absolute_url(), meal.date))
                body.append(esc(dish.name))
                body.append('</a>')
                body.append('</li>')
            body.append('</ul>')
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
