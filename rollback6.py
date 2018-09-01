

# =============================================
# Displaying time in different timezones
# =============================================

# ==============
# rollback6.py
# ==============

# In rollback6.py, we will change _current_time function to just pull time without timezone
# then we will go back to checkdb.py and see how to get time with timezones from there


import sqlite3
import datetime
import pytz

db = sqlite3.connect("accounts.sqlite")
db.execute("CREATE TABLE IF NOT EXISTS accounts (name TEXT PRIMARY KEY NOT NULL, balance INTEGER NOT NULL)")
db.execute("CREATE TABLE IF NOT EXISTS history (time TIMESTAMP NOT NULL,"
           " account TEXT NOT NULL, amount INTEGER NOT NULL, PRIMARY KEY (time, account))")


class Account(object):

    # We change _current_time module back to not using "astimezone()"
    @staticmethod
    def _current_time():
        return pytz.utc.localize(datetime.datetime.utcnow())

        # We comment this out and use above again
        # local_time = pytz.utc.localize(datetime.datetime.utcnow())
        # return local_time.astimezone()  # We return local_time "astimezone"

    def __init__(self, name: str, opening_balance: int = 0):
        cursor = db.execute("SELECT name, balance FROM accounts WHERE (name = ?)", (name,))
        row = cursor.fetchone()

        if row:
            self.name, self._balance = row
            print("Retrieved record for {}. ".format(self.name), end='')
        else:
            self.name = name
            self._balance = opening_balance
            cursor.execute("INSERT INTO accounts VALUES(?, ?)", (name, opening_balance))
            cursor.connection.commit()
            print("Account created for {}. ".format(self.name), end='')
        self.show_balance()

    def _save_update(self, amount):
        new_balance = self._balance + amount
        deposit_time = Account._current_time()
        db.execute("UPDATE accounts SET balance = ? WHERE (name = ?)", (new_balance, self.name))
        db.execute("INSERT INTO history VALUES(?, ?, ?)", (deposit_time, self.name, amount))
        db.commit()
        self._balance = new_balance

    def deposit(self, amount: int) -> float:
        if amount > 0.0:
            # new_balance = self._balance + amount
            # deposit_time = Account._current_time()
            # db.execute("UPDATE accounts SET balance = ? WHERE (name = ?)", (new_balance, self.name))
            # db.execute("INSERT INTO history VALUES(?, ?, ?)", (deposit_time, self.name, amount))
            # db.commit()
            # self._balance = new_balance
            self._save_update(amount)
            print("{:.2f} deposited".format(amount / 100))
        return self._balance / 100

    def withdraw(self, amount: int) -> float:
        if 0 < amount <= self._balance:
            # new_balance = self._balance - amount
            # withdrawal_time = Account._current_time()
            # db.execute("UPDATE accounts SET balance = ? WHERE (name = ?)", (new_balance, self.name))
            # db.execute("INSERT INTO history VALUES(?, ?, ?)", (withdrawal_time, self.name, -amount))
            # db.commit()
            # self._balance = new_balance
            self._save_update(-amount)
            print("{:.2f} withdrawn".format(amount / 100))
            return amount / 100
        else:
            print("The amount must be greater than zero and no more than your account balance")
            return 0.0

    def show_balance(self):
        print("Balance on account {} is {:.2f}".format(self.name, self._balance / 100))

if __name__ == '__main__':
    john = Account("John")
    john.deposit(1010)
    john.deposit(10)
    john.deposit(10)
    john.withdraw(30)
    john.withdraw(0)
    john.show_balance()

    terry = Account("TerryJ")
    graham = Account("Graham", 9000)
    eric = Account("Eric", 7000)
    michael = Account("Michael")
    terryG = Account("TerryG")

    db.close()



# ================================================
# Create view on rollback6.py
# ================================================

# We create a view by adding the code below (copied from changedb.py)
# The view will be called "localhistory" and we will create it here and then view it on checkdb.py using for loop

# NOTE: Before running this, clear the existing databases by deleting them.
# AFter deleting existing databases, run this code. It will create new databases.
# Then go to checkdb.py and run the section titled "Creating a VIEW for this query"

import sqlite3
import datetime
import pytz

# we will also modify "db = sqlite3.connect("accounts.sqlite")" to add "detect_types=sqlite3.PARSE_DECLTYPES"

db = sqlite3.connect("accounts.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)
db.execute("CREATE TABLE IF NOT EXISTS accounts (name TEXT PRIMARY KEY NOT NULL, balance INTEGER NOT NULL)")
db.execute("CREATE TABLE IF NOT EXISTS history (time TIMESTAMP NOT NULL,"
           " account TEXT NOT NULL, amount INTEGER NOT NULL, PRIMARY KEY (time, account))")

# Add this code to create a view.
# We will modify it by adding "CREATE VIEW IF NOT EXISTS localhistory AS" to the original statement to create the view and then select from it

db.execute("CREATE VIEW IF NOT EXISTS localhistory AS"
           " SELECT strftime('%Y-%m-%d %H:%M:%f', history.time, 'localtime') AS localtime,"
            "history.account, history.amount FROM history ORDER BY history.time")  # We remove the original colon :

class Account(object):

    # We change _current_time module back to not using "astimezone()"
    @staticmethod
    def _current_time():
        return pytz.utc.localize(datetime.datetime.utcnow())

        # We comment this out and use above again
        # local_time = pytz.utc.localize(datetime.datetime.utcnow())
        # return local_time.astimezone()  # We return local_time "astimezone"

    def __init__(self, name: str, opening_balance: int = 0):
        cursor = db.execute("SELECT name, balance FROM accounts WHERE (name = ?)", (name,))
        row = cursor.fetchone()

        if row:
            self.name, self._balance = row
            print("Retrieved record for {}. ".format(self.name), end='')
        else:
            self.name = name
            self._balance = opening_balance
            cursor.execute("INSERT INTO accounts VALUES(?, ?)", (name, opening_balance))
            cursor.connection.commit()
            print("Account created for {}. ".format(self.name), end='')
        self.show_balance()

    def _save_update(self, amount):
        new_balance = self._balance + amount
        deposit_time = Account._current_time()
        db.execute("UPDATE accounts SET balance = ? WHERE (name = ?)", (new_balance, self.name))
        db.execute("INSERT INTO history VALUES(?, ?, ?)", (deposit_time, self.name, amount))
        db.commit()
        self._balance = new_balance

    def deposit(self, amount: int) -> float:
        if amount > 0.0:
            # new_balance = self._balance + amount
            # deposit_time = Account._current_time()
            # db.execute("UPDATE accounts SET balance = ? WHERE (name = ?)", (new_balance, self.name))
            # db.execute("INSERT INTO history VALUES(?, ?, ?)", (deposit_time, self.name, amount))
            # db.commit()
            # self._balance = new_balance
            self._save_update(amount)
            print("{:.2f} deposited".format(amount / 100))
        return self._balance / 100

    def withdraw(self, amount: int) -> float:
        if 0 < amount <= self._balance:
            # new_balance = self._balance - amount
            # withdrawal_time = Account._current_time()
            # db.execute("UPDATE accounts SET balance = ? WHERE (name = ?)", (new_balance, self.name))
            # db.execute("INSERT INTO history VALUES(?, ?, ?)", (withdrawal_time, self.name, -amount))
            # db.commit()
            # self._balance = new_balance
            self._save_update(-amount)
            print("{:.2f} withdrawn".format(amount / 100))
            return amount / 100
        else:
            print("The amount must be greater than zero and no more than your account balance")
            return 0.0

    def show_balance(self):
        print("Balance on account {} is {:.2f}".format(self.name, self._balance / 100))

if __name__ == '__main__':
    john = Account("John")
    john.deposit(1010)
    john.deposit(10)
    john.deposit(10)
    john.withdraw(30)
    john.withdraw(0)
    john.show_balance()

    terry = Account("TerryJ")
    graham = Account("Graham", 9000)
    eric = Account("Eric", 7000)
    michael = Account("Michael")
    terryG = Account("TerryG")

    db.close()






# ================================================
# Timezones - Challenge
# ================================================

# We have seen that we store time in database in UTC and then retrieve them with methods shown above in local time
# Sometimes we need to retrieve the original date/time (not UTC) that was entered,
# and this challenge is to show you how to do that without using another external library

# ============
# Challenge:
# ============

# Store time information in the database so that the original time can be reconstructed.
# You must continue to store time in UTC because its the only reliable way to store time so they are correct relative to each timezone

# Modify the rollback6.py program so it includes an extra column in the database
# This extra column should be used to store either timezone info, or the original time offset from UTC, or tzinfo (you get to choose)
# Then modify checkdb.py to retrieve original time and display it along with UTC time
# Remember to close any open tables and delete the database in the project pane before running your modified program for the first time

# Hints:
# Don't store timezone name in the database. This will not work.
# you may want to review video in section 10 on "pickle" , although you can solve it another way.


# There are three approaches to solve this problem:

# Solution 1:
# The simplest is to store the local time as a string like we did a few videos ago.
# We store local time in addition to UTC.
# We have the code to do this above, so you can refer to it.


# Solution 2:
# Store the time offset in another column
# You can use an aware time utc offset method to get the offset and either store that as a datetime value or call the total_seconds method
# to get a float value of the number of seconds, then add the offset back to get the original time.


# Solution 3:
# This is the approach we will use.
# We will store the original time's tzinfo (timezone information)
# An aware time value contains timezone information in its tzinfo object. That is what makes it aware and not naive
# We will pickle a class instance. This converts the instance into a byte stream that can be stored in a database column.
# we will use the "pickle" modules "dump" function to convert the tzinfo into a bytestream and load to convert it back again after reading it from the database

# Our pickle column is a bytestream and we will need to use an integer column for it.
# first we import pickle
# changes are marked with CHANGE:

# NOTE: Before you run this, delete the existing databases.
# you can do this by rightclicking "accounts.sqlite" on left pane, then select delete, then refactor

import sqlite3
import datetime
import pytz
import pickle

# we will also modify "db = sqlite3.connect("accounts.sqlite")" to add "detect_types=sqlite3.PARSE_DECLTYPES"

db = sqlite3.connect("accounts.sqlite", detect_types=sqlite3.PARSE_DECLTYPES)
db.execute("CREATE TABLE IF NOT EXISTS accounts (name TEXT PRIMARY KEY NOT NULL, balance INTEGER NOT NULL)")

# CHANGE: We add a new "zone" column to "history" table
db.execute("CREATE TABLE IF NOT EXISTS history (time TIMESTAMP NOT NULL,"
           " account TEXT NOT NULL, amount INTEGER NOT NULL, "
           " zone INTEGER NOT NULL, PRIMARY KEY (time, account))")

# Add this code to create a view.
# We will modify it by adding "CREATE VIEW IF NOT EXISTS localhistory AS" to the original statement to create the view and then select from it

db.execute("CREATE VIEW IF NOT EXISTS localhistory AS"
           " SELECT strftime('%Y-%m-%d %H:%M:%f', history.time, 'localtime') AS localtime,"
           "history.account, history.amount FROM history ORDER BY history.time")  # We remove the original colon :

class Account(object):

    # We change _current_time module back to not using "astimezone()"

    # CHANGE: Now we need a tzinfo object for our local timezone.
    # we can get that by converting UTC to local time so we need to modify _current_time method

    @staticmethod
    def _current_time():
        # return pytz.utc.localize(datetime.datetime.utcnow())  # CHANGE: comment this out
        # We comment this out and use above again
        # local_time = pytz.utc.localize(datetime.datetime.utcnow())
        # return local_time.astimezone()  # We return local_time "astimezone"

        # CHANGE: we use this code
        utc_time = pytz.utc.localize(datetime.datetime.utcnow())
        local_time = utc_time.astimezone()
        zone = local_time.tzinfo
        return utc_time, zone  # returns utc_time and zone as a tuple

    def __init__(self, name: str, opening_balance: int = 0):
        cursor = db.execute("SELECT name, balance FROM accounts WHERE (name = ?)", (name,))
        row = cursor.fetchone()

        if row:
            self.name, self._balance = row
            print("Retrieved record for {}. ".format(self.name), end='')
        else:
            self.name = name
            self._balance = opening_balance
            cursor.execute("INSERT INTO accounts VALUES(?, ?)", (name, opening_balance))
            cursor.connection.commit()
            print("Account created for {}. ".format(self.name), end='')
        self.show_balance()


    # CHANGE: Now we need to unpack the two values from _current_time method and then pickle the zone
    def _save_update(self, amount):
        new_balance = self._balance + amount
        deposit_time, zone = Account._current_time() # CHANGE: we unpack returned tuple
        pickled_zone = pickle.dumps(zone)       # CHANGE: we pickle the zone

        db.execute("UPDATE accounts SET balance = ? WHERE (name = ?)", (new_balance, self.name))

        # CHANGE: we add new ? for pickled_zone
        db.execute("INSERT INTO history VALUES(?, ?, ?, ?)", (deposit_time, self.name, amount, pickled_zone))
        db.commit()
        self._balance = new_balance

    def deposit(self, amount: int) -> float:
        if amount > 0.0:
            # new_balance = self._balance + amount
            # deposit_time = Account._current_time()
            # db.execute("UPDATE accounts SET balance = ? WHERE (name = ?)", (new_balance, self.name))
            # db.execute("INSERT INTO history VALUES(?, ?, ?)", (deposit_time, self.name, amount))
            # db.commit()
            # self._balance = new_balance
            self._save_update(amount)
            print("{:.2f} deposited".format(amount / 100))
        return self._balance / 100

    def withdraw(self, amount: int) -> float:
        if 0 < amount <= self._balance:
            # new_balance = self._balance - amount
            # withdrawal_time = Account._current_time()
            # db.execute("UPDATE accounts SET balance = ? WHERE (name = ?)", (new_balance, self.name))
            # db.execute("INSERT INTO history VALUES(?, ?, ?)", (withdrawal_time, self.name, -amount))
            # db.commit()
            # self._balance = new_balance
            self._save_update(-amount)
            print("{:.2f} withdrawn".format(amount / 100))
            return amount / 100
        else:
            print("The amount must be greater than zero and no more than your account balance")
            return 0.0

    def show_balance(self):
        print("Balance on account {} is {:.2f}".format(self.name, self._balance / 100))

if __name__ == '__main__':
    john = Account("John")
    john.deposit(1010)
    john.deposit(10)
    john.deposit(10)
    john.withdraw(30)
    john.withdraw(0)
    john.show_balance()

    terry = Account("TerryJ")
    graham = Account("Graham", 9000)
    eric = Account("Eric", 7000)
    michael = Account("Michael")
    terryG = Account("TerryG")

    db.close()

# After running above code, check the history table in DB Browser, we have the new column "zone"
# Now we go to checkdb.py on section to run solution 3 of challenge

# ============================================================================
# NOTE: All backed up to here. Start backup on rollback7.py and checkdb2.py
# ============================================================================

