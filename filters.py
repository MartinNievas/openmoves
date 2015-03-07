#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from datetime import timedelta
from flask import url_for, request
import math
import time


def format_date_time(time):
    return time.strftime("%Y-%m-%d %H:%M:%S")


def format_date_time_millis(date):
    return date.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def format_distance(distance, unit=True):
    if distance > 1000:
        return "%0.2f%s" % (distance / 1000.0, " km" if unit else "")
    elif distance < 1000:
        return "%0.3f%s" % (distance / 1000.0, " km" if unit else "")


def format_speed(speed, unit=True):
    return "%0.1f%s" % (speed * 3.6, " km/h" if unit else "")


def format_altitude(altitude, unit=True):
    return "%d%s" % (altitude, " m" if unit else "")


def format_temparature(temperature, unit=True):
    return "%0.1f%s" % (temperature - 273.15, " °C" if unit else "")


def format_hr(hr, unit=True):
    return "%d%s" % (hr * 60, " bpm" if unit else "")


def format_energyconsumption(energyconsumption, unit=True):
    return "%0.1f%s" % (energyconsumption / 6.978 / 10.0, " kcal/min" if unit else "")


def duration(value):
    if type(value).__name__ in ('str', 'unicode'):
        value = timedelta(seconds=float(value))
    elif isinstance(value, (float, int)):
        value = timedelta(seconds=float(value))

    hours, remainder = divmod(value.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return '%02d:%02d:%05.2f' % (hours, minutes, seconds)


def swim_pace(value):
    assert isinstance(value, timedelta)
    hours, remainder = divmod(100 * value.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    assert hours == 0
    return '%02d:%05.2f min / 100 m' % (minutes, seconds)


def radian_to_degree(value):
    return 180.0 / math.pi * value


def unix_epoch(date):
    return 1000 * time.mktime(date.timetuple())


# inspired by http://flask.pocoo.org/snippets/44/
def url_for_sortable(sort, sort_order):
    args = request.view_args.copy()
    args.update(request.args)
    args['sort'] = sort
    args['sort_order'] = sort_order
    return url_for(request.endpoint, **args)


def register_globals(app):
    app.jinja_env.globals['url_for_sortable'] = url_for_sortable


def register_filters(app):
    app.jinja_env.filters['date_time'] = format_date_time
    app.jinja_env.filters['date_time_millis'] = format_date_time_millis
    app.jinja_env.filters['duration'] = duration
    app.jinja_env.filters['degree'] = radian_to_degree
    app.jinja_env.filters['epoch'] = unix_epoch
    app.jinja_env.filters['swim_pace'] = swim_pace
