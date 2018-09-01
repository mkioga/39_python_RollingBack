
# ===========
# checkdb.py
# ===========

# We will try to get some input from the "history" table in "accounts" database

import sqlite3

db = sqlite3.connect("accounts.sqlite")

for row in db.execute("SELECT * FROM history"):
    print(row)

db.close()

# When we run above code, we get this results. This is a tuple consisting of two strings (time, name) and an int (deposits)

# ('2018-07-04 14:14:31.203132+00:00', 'John', 1010)
# ('2018-07-04 14:14:31.353149+00:00', 'John', 10)
# ('2018-07-04 14:14:31.509387+00:00', 'John', 10)

# ==========================================================================
# We can confirm that the timestamp is in string format by using this code


import sqlite3

db = sqlite3.connect("accounts.sqlite")

for row in db.execute("SELECT * FROM history"):
    local_time = row[0]
    print("Time = {}: Format = {}".format(local_time, type(local_time)))

db.close()


# When  we run above code we get this result showing timestamp is in string format

# Time = 2018-07-04 14:14:31.203132+00:00: Format = <class 'str'>
# Time = 2018-07-04 14:14:31.353149+00:00: Format = <class 'str'>
# Time = 2018-07-04 14:14:31.509387+00:00: Format = <class 'str'>

# NOTE that we can convert these string types into DATETIME values by importing the DATETIME module
# and using the strptime method of the DATETIME module.
# you can find this in documentation if you want to use it.

# There is a gotcha on this which we will mention later, but as long as we use python documentation
# and Not the SQLITE datetime documentation, we will be fine

# ====================================================================
#
# We have used the python sqlite3 timestamp column type for out times and this relies on the fact that
# the sqlite3 library can examine custom datatypes per column and respond to types that it knows about

# it is possible to define and register your own data types but the "date" and "timestamp" type have already been registered for us.
# So we just need to tell sqlite3 to respond to them.
# we do that by passing PARSE_DECLTYPES when we create the connection


import sqlite3

db = sqlite3.connect("accounts.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)

for row in db.execute("SELECT * FROM history"):
    local_time = row[0]
    print("Time = {}: Format = {}".format(local_time, type(local_time)))

db.close()


# When you run above code, the PARSE_DECLTYPES is supposed to convert the string into "datetime" but in my case
# am still getting class string

# Time = 2018-07-04 14:14:31.203132+00:00: Format = <class 'str'>
# Time = 2018-07-04 14:14:31.353149+00:00: Format = <class 'str'>
# Time = 2018-07-04 14:14:31.509387+00:00: Format = <class 'str'>

# For more information on Adapters and converters, check this link on section 12.6.2.2.2
# https://docs.python.org/3/library/sqlite3.html
# https://docs.python.org/3/library/sqlite3.html#using-adapters-to-store-additional-python-types-in-sqlite-databases


# ===========================================================

# This PARSE_DECLTYPES does not handle timezone aware dates
# you can see results above look like ==> Time = 2018-07-04 14:14:31.203132+00:00:
# The end has +00.00 which shows not timezone variation (either plus or minus)

# we can confirm this by modifying "rollback5.py" to include timezone and then we will see this code will not show timezone
# Now to go "rollback5.py"



import sqlite3

db = sqlite3.connect("accounts.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)

for row in db.execute("SELECT * FROM history"):
    local_time = row[0]
    print("Time = {}: Format = {}".format(local_time, type(local_time)))

db.close()



# After making the timezone changes in rollback5.py, we come and run this and get this result
# We are getting the format "datetime" and we also have no timezone as expected.

# Time = 2018-07-04 10:00:49.391110: Format = <class 'datetime.datetime'>
# Time = 2018-07-04 10:00:49.481968: Format = <class 'datetime.datetime'>
# Time = 2018-07-04 10:00:49.570322: Format = <class 'datetime.datetime'>

# ================================================
# How to retrieve timezones
# ================================================

# There is no reliable standard python libraries to parse with datetime values
# However there are additional libraries to help you retrieve timezones.

# we can search for "python dateutil latest version" and get this link
# https://pypi.org/project/python-dateutil/

# ===============================================
# METHOD_1: To display localtime
# ===============================================

# Note that we first go back to rollback6.py and make changes to _current_time so it does not use "astimezone"


import sqlite3
import pytz

db = sqlite3.connect("accounts.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)

for row in db.execute("SELECT * FROM history"):
    utc_time = row[0]  # Retrieves UTC time
    local_time = pytz.utc.localize(utc_time).astimezone()  # Converts UTC time to localtime
    print("UTC Time = {}: Local Time = {}".format(utc_time, local_time))  # Display both UTC time and Local time

db.close()


# When we run this code, we now get UTC time and Local time in this format
# its now 3.23 PM UTC time (15:23) and 10.23 AM Central time (my local time)

# UTC Time = 2018-07-04 15:23:32.362647: Local Time = 2018-07-04 10:23:32.362647-05:00
# UTC Time = 2018-07-04 15:23:32.451843: Local Time = 2018-07-04 10:23:32.451843-05:00
# UTC Time = 2018-07-04 15:23:32.529392: Local Time = 2018-07-04 10:23:32.529392-05:00


# ===================================================================
# METHOD_2: To display localtime using "sqlite3 strftime function":
# ===================================================================

# We will look at an alternative way to show time in UTC timezone.
# The other way of doing this is to use "sqlite datetime functions" and perform a conversion before getting data from server
# NOTE we don't need to import pytz
# NOTE: if you get a message that "sqlite dialect is not configured" when you hover over the select statement, you can correct this by:
# File > Settings > Search for sql > Select SQL dialect > choose checkdb.py and select sqlite next to it.
# In my version of intellij, I don't see this problem and there is no SQL dialect. So we ignore it.

# Here the SELECT query uses the strftime function to convert the time field into a string.
# "%Y-%m-%d %H:%M:%f" is the parameter that gives the format that datetime will be produced. year, month, day, hour, minute, fractional second (SS:SSS)

# SQLite datetime functions are documented here
# https://www.sqlite.org/lang_datefunc.html

# "history.time" provides a time value from the time column of the history table.
# "localtime" is the modifier to cause the UTC time to be converted to local time

# NOTE that instead of using "strftime" we can use "datetime", but make sure to refer to above link to get correct parameters for datetime function

import sqlite3

db = sqlite3.connect("accounts.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)

for row in db.execute("SELECT strftime('%Y-%m-%d %H:%M:%f', history.time, 'localtime') AS localtime,"
                      "history.account, history.amount FROM history ORDER BY history.time"):
    print(row)

db.close()

# When we run above code, we get results as follows.
# you can see the dates are now in local time
# ADVANTAGE of this method is that it will work with whatever client is being used to access the database.
# So we could create a view in that select statement and users will be able to view data in their local time


# ('2018-07-04 10:23:32.362', 'John', 1010)
# ('2018-07-04 10:23:32.451', 'John', 10)
# ('2018-07-04 10:23:32.529', 'John', 10)
# ('2018-07-04 10:23:32.630', 'John', -30

# ===============================================
# Creating a VIEW for this query
# ==============================================

# We will create a view in rollback6.py by copying code below and adding it to rollback6.py

# db.execute("SELECT strftime('%Y-%m-%d %H:%M:%f', history.time, 'localtime') AS localtime,"
#            "history.account, history.amount FROM history ORDER BY history.time"):


# After modifying rollback6.py and running it to create a view, we can query the view here using this code.

# import sqlite3
#
# db = sqlite3.connect("accounts.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)
#
# for row in db.execute("SELECT * FROM localhistory"):
#     print(row)
#
# db.close()

# When we run this code, we get these results which are similar to the ones we got from previous code.
# It is showing results in local time

# ('2018-07-05 15:08:15.802', 'John', 1010)
# ('2018-07-05 15:08:15.937', 'John', 10)
# ('2018-07-05 15:08:16.101', 'John', 10)
# ('2018-07-05 15:08:16.233', 'John', -30)



# =====================================================
# Checkdb to run solution 3 of Challenge
# ======================================================


import sqlite3
import pytz
import pickle


db = sqlite3.connect("accounts.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)

for row in db.execute("SELECT * FROM history"):  # we select from history table
    utc_time = row[0]
    pickled_zone = row[3]
    zone = pickle.loads(pickled_zone)  # we pickle the data using pickle modules "loads" function
    local_time = pytz.utc.localize(utc_time).astimezone(zone)  # astimezone converts UTC to its original timezone
    print("UTC_TIME = {}, LOCAL_TIME = {}, LOCAL_TIME_TZINFO = {}".format(utc_time, local_time, local_time.tzinfo))

db.close()

# When we run this, we get this results

# UTC_TIME = 2018-07-06 13:42:51.050407, LOCAL_TIME = 2018-07-06 08:42:51.050407-05:00, LOCAL_TIME_TZINFO = Central Daylight Time
# UTC_TIME = 2018-07-06 13:42:51.181332, LOCAL_TIME = 2018-07-06 08:42:51.181332-05:00, LOCAL_TIME_TZINFO = Central Daylight Time
# UTC_TIME = 2018-07-06 13:42:51.482452, LOCAL_TIME = 2018-07-06 08:42:51.482452-05:00, LOCAL_TIME_TZINFO = Central Daylight Time
# UTC_TIME = 2018-07-06 13:42:51.637715, LOCAL_TIME = 2018-07-06 08:42:51.637715-05:00, LOCAL_TIME_TZINFO = Central Daylight Time

