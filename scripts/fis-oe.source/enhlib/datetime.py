from .stdlib.datetime import date, time, datetime
from .dbf import Date, Time, DateTime

dates = date, Date
times = time, Time
datetimes = datetime, DateTime

moments = dates + times + datetimes
