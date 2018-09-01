

# # ======================================================
# # rollback4.py
# # ======================================================


# # ======================================================
# # Update deposit and withdrawal methods
# # ======================================================
#
# # In previous video, we saw a way to change data in our database table using DB Browser
# # Now we will change our accounts class to update the balance columns and then store the transactions details in "history" table
#
# # If you run this code, it shows that "Balance on account John is 10.00"
# # But when you look in the database using "DB Browser" you will find the balance for John is 0.0
# # Doubleclick "accounts" to see that.
#
# # So we need to update both Deposit and Withdrawal methods
# # (1) Create an entry in the "history" table each time a deposit or withdrawal is made
# # (2) Update the account balance in the "accounts" table as well.
# # If any one of these two updates succeeds and the other one fails, then our database will be in an inconsistent state.
# # So we need to make sure that all updates succeed or rollback all the updates if any does not succeed.
#
# # We will add code to update the two database tables. CHANGE_1 on the "deposit" and "withdrawal" methods
# # And then look at how to cause an error so we can rollback the transaction if necessary
#
# # When you run the code with changes under CHANGE_1, the balance account for John is different from what is shown in database
# # This is because we have updated the "deposit" method but not updated "withdrawal" method yet.
# # When you doubleclick "history" table in DB Browser, we see the transactions with only deposits
# # NOTE you may need to ignore filter because timestamp seems not to be working
#
# # We can add static method "current_time" to get time. CHANGE_2
#
# # Now we will update the "withdrawal" method: CHANGE_3
#
#
#
# import sqlite3
# import datetime
# import pytz
#
# db = sqlite3.connect("accounts.sqlite")  # make sure to give accounts a sqlite file extension
# db.execute("CREATE TABLE IF NOT EXISTS accounts (name TEXT PRIMARY KEY NOT NULL, balance INTEGER NOT NULL)")
# db.execute("CREATE TABLE IF NOT EXISTS history (time DATETIME NOT NULL, "   # if you break line to continue in next line, it creates "
#            "account TEXT NOT NULL, amount INTEGER NOT NULL, PRIMARY KEY (time, account))")
#
#
# class Account(object):
#
#     @staticmethod   # CHANGE_2
#     def _current_time():  # CHANGE_2
#         return pytz.utc.localize(datetime.datetime.utcnow())  # CHANGE_2
#
#
#     def __init__(self, name: str, opening_balance: int = 0):  # use int and initialize it to 0
#         # We change init method so it retrieves account details from the database or save them if the account does not exist
#         # We are using the "name" above that is passed to __init__ to put it below under (name,) which is then used to replace
#         # the ? next to (name = ?), and so the name in (name = ?) is assigned the value (name,) which was passed into __init__ above
#
#         cursor = db.execute("SELECT name, balance FROM accounts WHERE (name = ?)", (name,))
#         # cursor then fetches one record and returns a tuple of the values from all the database columns
#         # othewise it returns NONE if no records are found
#         row = cursor.fetchone()  # fetch one record
#
#         if row:  # if row returned is not None (can also write it here "if row is not None")
#             self.name, self._balance = row  # We unpack the tuple returned into name and balance
#             print("Retrieved record for {}. ".format(self.name), end='')
#         else:  # if you are not able to retrieve a record from the database
#             self.name = name  # we save name passed to __init__
#             self._balance = opening_balance  # and add opening balance which is initialized as 0
#             # This is code to save into database
#             cursor.execute("INSERT INTO accounts VALUES(?, ?)", (name, opening_balance))
#             cursor.connection.commit  # to immediately save it.
#             print("Account created for {}. ".format(self.name), end='')
#         # show_balance remains on this indentation to show balance whether it existed in (if) or just being created by (else)
#         self.show_balance()  # We will define this method below. but it is called here to show balance
#
#     # We define the deposit method.
#     def deposit(self, amount: int) -> float:  # CHANGE - amount is in int, but we will still return a float
#         if amount > 0.0:
#             # self._balance += amount  # CHANGE_1: We will remove this line and add the following 6 lines
#             new_balance = self._balance + amount  # CHANGE_1: Calculate balance and assign it to variable new_balance
#             # deposit_time = pytz.utc.localize(datetime.datetime.utcnow())   # CHANGE_1: Calculate time of transaction and assign it to deposit_time (need to import datetime & pytz)
#             deposit_time = Account._current_time()  # CHANGE_2: Make deposit_time to use the static method current_time defined above
#             db.execute("UPDATE accounts SET balance = ? WHERE (name = ?)", (new_balance, self.name))  # CHANGE_1: we update "accounts" table
#             db.execute("INSERT INTO history VALUES(?, ?, ?)", (deposit_time, self.name, amount))   # CHANGE_1: insert our transaction into our "history" table
#             db.commit()  # CHANGE_1: Then we commit
#             self._balance = new_balance  # CHANGE_1: Now we update our self._balance attribute because transaction is completed.
#             print("{:.2f} deposited".format(amount / 100))  # CHANGE - print using .2f to indicate 2 decimal place. Amount will be divided by 100
#         return self._balance / 100  # CHANGE - divide by 100
#
#     # We define the withdrawal method and make sure we don't withdraw more than the balance
#     # Also withdrawal amount must be 0 to count
#
#     def withdraw(self, amount: int) -> float:  # CHANGE - amount is int but will still return a float
#         if 0 < amount <= self._balance:
#             # self._balance -= amount  # CHANGE_3: we delete this line/or comment it out
#
#             new_balance = self._balance - amount  # CHANGE_3
#             withdrawal_time = Account._current_time()  # CHANGE_3
#             db.execute("UPDATE accounts SET balance = ? WHERE (name = ?)", (new_balance, self.name))  # CHANGE_1: we update "accounts" table
#             db.execute("INSERT INTO history VALUES(?, ?, ?)", (withdrawal_time, self.name, -amount))   # CHANGE_1: insert our transaction into our "history"  Note - before amount
#             db.commit()  # CHANGE_1: Then we commit
#             self._balance = new_balance  # CHANGE_1: Now we update our self._balance attribute because transaction is completed.
#
#             # NOTE: Before running code, set John's balance to 0 and then commit it, both in DB Browser
#             # We also delete "history" transactions and commit, both in DB Browser (NOTE: this produces error in my case. see problem below)
#
#             print("{:.2f} withdrawn".format(amount / 100))  # CHANGE - print format 2 decimal places and amount is divided by 100
#             return amount / 100 # CHANGE - divide by 100
#         else:
#             print("Withdrawn amount must be more than 0 and less or equal to the Account balance")
#             return 0.0  # return 0 because withdrawal has not been allowed. so 0 withdrawn
#
#     # Now we define the show_balance method that was called by __init__ method above
#     def show_balance(self):
#         print("Balance on account {} is {:.2f}".format(self.name, self._balance / 100))  # CHANGE - print 2 decimal places and balance divided by 100
#
#
# # We create account for John
# # Now we will write some code to call above functions and test them
# # If you run this code, you will get good Balance of 10.00 and not 9.999999 with rounding errors
#
# if __name__ == '__main__':
#     john = Account("John")  # Give it account name. Default balance is 0.0
#     john.deposit(1010)  # Now we remove the decimals in these parameters i.e. multiply all by 100 to remove decimal
#     john.deposit(10)
#     john.deposit(10)
#     john.withdraw(30)
#     john.withdraw(0)
#     john.show_balance()
#
#     # We create a few more accounts.
#
#     terry = Account("TerryJ")
#     graham = Account("Graham", 9000)
#     eric = Account("Eric", 7000)
#
#     # We add this new code to account for the modifications we made in the database using DB Browser
#
#     michael = Account("Michael")
#     terryG = Account("TerryG")
#
#     # Then we close the database
#
#     db.close()


# problem. Need to check why timestamp does not work in history. I was notable to find the reason why, but will continue
# NOTE: this problem went away in below code where CHANGE_1 and CHANGE_3 were consolidated. Maybe CHANGE_3 had an error above




# ===========================================================
# Consolidating CHANGE_1 and CHANGE_3 above into a function
# ============================================================

# NOTE: for some reason, timestamp works on this one. Maybe there was an issue with withdrawal method above.

# We replace CHANGE_1 (deposit) and CHANGE_3 (withdrawal) with function _save_update.
# This removes the duplication


import sqlite3
import datetime
import pytz

db = sqlite3.connect("accounts.sqlite")  # make sure to give accounts a sqlite file extension
db.execute("CREATE TABLE IF NOT EXISTS accounts (name TEXT PRIMARY KEY NOT NULL, balance INTEGER NOT NULL)")
db.execute("CREATE TABLE IF NOT EXISTS history (time DATETIME NOT NULL, "   # if you break line to continue in next line, it creates " 
           "account TEXT NOT NULL, amount INTEGER NOT NULL, PRIMARY KEY (time, account))")


class Account(object):

    @staticmethod   # CHANGE_2
    def _current_time():  # CHANGE_2
        return pytz.utc.localize(datetime.datetime.utcnow())  # CHANGE_2


    def __init__(self, name: str, opening_balance: int = 0):  # use int and initialize it to 0
        # We change init method so it retrieves account details from the database or save them if the account does not exist
        # We are using the "name" above that is passed to __init__ to put it below under (name,) which is then used to replace
        # the ? next to (name = ?), and so the name in (name = ?) is assigned the value (name,) which was passed into __init__ above

        cursor = db.execute("SELECT name, balance FROM accounts WHERE (name = ?)", (name,))
        # cursor then fetches one record and returns a tuple of the values from all the database columns
        # othewise it returns NONE if no records are found
        row = cursor.fetchone()  # fetch one record

        if row:  # if row returned is not None (can also write it here "if row is not None")
            self.name, self._balance = row  # We unpack the tuple returned into name and balance
            print("Retrieved record for {}. ".format(self.name), end='')
        else:  # if you are not able to retrieve a record from the database
            self.name = name  # we save name passed to __init__
            self._balance = opening_balance  # and add opening balance which is initialized as 0
            # This is code to save into database
            cursor.execute("INSERT INTO accounts VALUES(?, ?)", (name, opening_balance))
            cursor.connection.commit()  # to immediately save it.
            print("Account created for {}. ".format(self.name), end='')
        # show_balance remains on this indentation to show balance whether it existed in (if) or just being created by (else)
        self.show_balance()  # We will define this method below. but it is called here to show balance

    # We define the deposit method.
    def deposit(self, amount: int) -> float:  # CHANGE - amount is in int, but we will still return a float
        if amount > 0.0:

            # # CHANGE_1: We comment this out and replace it with function _save_update
            # new_balance = self._balance + amount  # CHANGE_1: Calculate balance and assign it to variable new_balance
            # # deposit_time = pytz.utc.localize(datetime.datetime.utcnow())   # CHANGE_1: Calculate time of transaction and assign it to deposit_time (need to import datetime & pytz)
            # deposit_time = Account._current_time()  # CHANGE_2: Make deposit_time to use the static method current_time defined above
            # db.execute("UPDATE accounts SET balance = ? WHERE (name = ?)", (new_balance, self.name))  # CHANGE_1: we update "accounts" table
            # db.execute("INSERT INTO history VALUES(?, ?, ?)", (deposit_time, self.name, amount))   # CHANGE_1: insert our transaction into our "history" table
            # db.commit()  # CHANGE_1: Then we commit
            # self._balance = new_balance  # CHANGE_1: Now we update our self._balance attribute because transaction is completed.

            # We call function _save_update and pass it a positive amount (for deposit)
            self._save_update(amount)

            print("{:.2f} deposited".format(amount / 100))  # CHANGE - print using .2f to indicate 2 decimal place. Amount will be divided by 100
        return self._balance / 100  # CHANGE - divide by 100

    # We define the withdrawal method and make sure we don't withdraw more than the balance
    # Also withdrawal amount must be 0 to count

    def withdraw(self, amount: int) -> float:  # CHANGE - amount is int but will still return a float
        if 0 < amount <= self._balance:

            # # CHANGE_3: We comment it out and replace it by calling function _save_update
            # new_balance = self._balance - amount  # CHANGE_3
            # withdrawal_time = Account._current_time()  # CHANGE_3
            # db.execute("UPDATE accounts SET balance = ? WHERE (name = ?)", (new_balance, self.name))  # CHANGE_1: we update "accounts" table
            # db.execute("INSERT INTO history VALUES(?, ?, ?)", (withdrawal_time, self.name, -amount))   # CHANGE_1: insert our transaction into our "history"  Note - before amount
            # db.commit()  # CHANGE_1: Then we commit
            # self._balance = new_balance  # CHANGE_1: Now we update our self._balance attribute because transaction is completed.

            # We call function _save_update and pass it a negative amount (for withdrawal)
            self._save_update(-amount)

            # NOTE: Before running code, set John's balance to 0 and then commit it, both in DB Browser
            # We also delete "history" transactions and commit, both in DB Browser

            print("{:.2f} withdrawn".format(amount / 100))  # CHANGE - print format 2 decimal places and amount is divided by 100
            return amount / 100 # CHANGE - divide by 100
        else:
            print("Withdrawn amount must be more than 0 and less or equal to the Account balance")
            return 0.0  # return 0 because withdrawal has not been allowed. so 0 withdrawn

    # Now we define the show_balance method that was called by __init__ method above
    def show_balance(self):
        print("Balance on account {} is {:.2f}".format(self.name, self._balance / 100))  # CHANGE - print 2 decimal places and balance divided by 100

    # _SAVE_UPDATE FUNCTION (consolidates CHANGE_1 and CHANGE_3)
    # We create function _save_update below to replace CHANGE_1 and CHANGE_3above
    # We just copy and paste CHANGE_1 here (CHANGE_1 has a positive amount). We will just pass negative amount when using it for withdrawal

    def _save_update(self, amount):  # we will pass it an amount
        new_balance = self._balance + amount  # Calculate balance and assign it to variable new_balance
        # deposit_time = pytz.utc.localize(datetime.datetime.utcnow())   # Calculate time of transaction and assign it to deposit_time (need to import datetime & pytz)
        deposit_time = Account._current_time()  # Make deposit_time to use the static method current_time defined above
        db.execute("UPDATE accounts SET balance = ? WHERE (name = ?)", (new_balance, self.name))  # we update "accounts" table
        db.execute("INSERT INTO history VALUES(?, ?, ?)", (deposit_time, self.name, amount))   # insert our transaction into our "history" table
        db.commit()  # Then we commit
        self._balance = new_balance  # Now we update our self._balance attribute because transaction is completed.




# We create account for John
# Now we will write some code to call above functions and test them
# If you run this code, you will get good Balance of 10.00 and not 9.999999 with rounding errors

if __name__ == '__main__':
    john = Account("John")  # Give it account name. Default balance is 0.0
    john.deposit(1010)  # Now we remove the decimals in these parameters i.e. multiply all by 100 to remove decimal
    john.deposit(10)
    john.deposit(10)
    john.withdraw(30)
    john.withdraw(0)
    john.show_balance()

    # We create a few more accounts.

    terry = Account("TerryJ")
    graham = Account("Graham", 9000)
    eric = Account("Eric", 7000)

    # We add this new code to account for the modifications we made in the database using DB Browser

    michael = Account("Michael")
    terryG = Account("TerryG")

    # Then we close the database

    db.close()


# =================================================

# Now we go to next video to see how to retrieve history data

# Displaying date/time in different timezones

