#!/usr/bin/env python
"""
Utility Functions
"""

import datetime
from tabulate import tabulate

def getWeekDay(curr_time):
    """
    Function to return day of the week
    Python indexes days of the week from 0 to 6 starting Monday
    weekdays as a list
    """
    weekDays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    weekDayIndex = curr_time.weekday()

    day = weekDays[weekDayIndex]

    return day

def getTime24(curr_time):
    """
    Function to return current time in HH:MM format
    """
    timeVal = curr_time.strftime("%H:%M")

    return timeVal

def print_results(results):
    """
    Function to print food truck list to the console.
    """
    trucks = []
    for foodtruck in results:
        trucks.append([foodtruck['applicant'], foodtruck['location']])
    columns = ["NAME", "ADDRESS"]

    table_format = "pipe"
    print ("\n", tabulate(trucks, columns, tablefmt=table_format))

