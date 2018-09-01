
# =======================================================
# Rolling back transactions
# =======================================================

# We will simulate an error and then make code to rollback transaction

# ===============
# rollback7.py
# ===============

# first delete accounts.sqlite files on the left, then run rollback7.py again to make sure good data is created
# The history table has a composite key (two keys to make unique key) made up of history.time and history.account column
# A way to simulate an error here is to save a transaction with same time and account as one that already exits

# We can do this by modifying _current_time method to return same number each time (CHANGE_1)
# When you run the code with CHANGE_1, we get error message "sqlite3.IntegrityError: UNIQUE constraint failed: history.time, history.account"
# This is because when we try to add a new history row with same time and account, as a row that already exists
# you get sqlite3.IntegrityError: because the primary key will not be unique

# We can use a try clause to rollback transaction if an error is encountered ( CHANGE_2 )
# When you run after CHANGE_2, we don't get an error

# Finally we remove CHANGE_1, (return 1) which was a test code and return the initial return
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
        # return 1   # CHANGE_1. This is for testing



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

        # CHANGE_2: code for rolling back if error is found.
        try:   # CHANGE_2
            db.execute("UPDATE accounts SET balance = ? WHERE (name = ?)", (new_balance, self.name))
            db.execute("INSERT INTO history VALUES(?, ?, ?)", (deposit_time, self.name, amount))
        except sqlite3.Error:
            db.rollback()  # Rollback if you get an error
        else:
            db.commit()  # Commits if no error is found
            self._balance = new_balance  # Then updates the balance


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


