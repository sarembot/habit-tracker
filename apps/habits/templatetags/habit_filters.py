from django import template

register = template.Library()

@register.filter
def exists(completed_habits, args):
    habit, date = args
    return completed_habits.filter(habit=habit, completed_date=date.date()).exists()