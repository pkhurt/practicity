from django import template

register = template.Library()


@register.filter
def date_of_execution_formatted(execution_object):
    """
    This templatefilter makes the method Execution.date_of_execution_formatted() available on templates
    :param execution_object: Execution object
    :type execution_object: Execution
    :return: Date of the execution
    :rtype: dateFormat
    """
    return execution_object.date_of_execution_formatted()


@register.filter
def duration_executed(execution_object):
    """

    :param execution_object:
    :return:
    """
    return execution_object.duration_executed()


@register.filter
def day_of_the_year_executed(execution_object):
    """

    :param execution_object:
    :return:
    """
    return execution_object.day_of_the_year_executed()