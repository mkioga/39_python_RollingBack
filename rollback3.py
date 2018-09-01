
# ==============================================
# Adding database code to Account Class
# ==============================================

# ===============
# rollback3.py
# ===============

# Here we will start storing Account details in a database.
# First we will import sqlite3
# Then we will add commands to create "Accounts" and "Transactions" tables in the database.


import sqlite3

# Connect to database using sqlite3 and name the table accounts.sqlite3
# Then send SQL commands to create the "accounts" and "transactions" table
# In this case, the accounts table stores name of account and account balance
# The transactions table stores the time of transactions, the account that the transaction relates to and the amount
# We will store deposits as positives and withdrawals as negatives.

# The PRIMARY KEY for the transactions table is a "composite key" i.e. combination of time of transaction and account it refers to
# This is because you can have many transactions on different accounts at the same time, so we need to specify time and account
# to uniquely identify a particular transaction in our database.

# NOTE that you can have additional keys in addition to the PRIMARY KEY.
# If you want to create additional keys, you don't remove PRIMARY from primary key, but you use the word UNIQUE

# NOTE that storing "balance" in the "accounts" table is breaking rules of normalization
# Balance can be calculated by summing all the amounts in "transactions" table.
# over time, there will be many transactions and calculating balance every time will be expensive.
# So we add the "balance" in the "accounts" table for performance reasons.

# NOTE we are storing "time" as a "TIMESTAMP" property.
# And we know that sqlite3 only has 5 storage types for its columns i.e. NULL, INTEGER, REAL, TEXT, and BLOB.
# https://www.sqlite.org/datatype3.html
# so where are we getting "TIMESTAMP" from ?
# The above 5 types are STORAGE CLASSES rather than DATATYPES
# And apart from INTEGER primary key field, you can store any kind of value in any type of column.
# integer primary key values are handled differently and can only hold integer values
# The system is flexible and python sqlite3 library includes support for DATETIME values and performs conversions
# automatically to and from DATETIME values.
# But we need to tell it to do that and we will see how to do that later
# Note that we should always store time in UTC

# NOTE: in third line below, table "history" was initially named "transactions" until we changed it later
# down this code below. when we changed table name using "DB Browser"

db = sqlite3.connect("accounts.sqlite")  # make sure to give accounts a sqlite file extension
db.execute("CREATE TABLE IF NOT EXISTS accounts (name TEXT PRIMARY KEY NOT NULL, balance INTEGER NOT NULL)")
db.execute("CREATE TABLE IF NOT EXISTS history (time TIMESTAMP NOT NULL, "   # if you break line to continue in next line, it creates " 
           "account TEXT NOT NULL, amount INTEGER NOT NULL, PRIMARY KEY (time, account))")


class Account(object):

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
            cursor.connection.commit  # to immediately save it.
            print("Account created for {}. ".format(self.name), end='')
        # show_balance remains on this indentation to show balance whether it existed in (if) or just being created by (else)
        self.show_balance()  # We will define this method below. but it is called here to show balance

    # We define the deposit method.
    def deposit(self, amount: int) -> float:  # CHANGE - amount is in int, but we will still return a float
        if amount > 0.0:
            self._balance += amount
            print("{:.2f} deposited".format(amount / 100))  # CHANGE - print using .2f to indicate 2 decimal place. Amount will be divided by 100
        return self._balance / 100  # CHANGE - divide by 100

    # We define the withdrawal method and make sure we don't withdraw more than the balance
    # Also withdrawal amount must be 0 to count

    def withdraw(self, amount: int) -> float:  # CHANGE - amount is int but will still return a float
        if 0 < amount <= self._balance:
            self._balance -= amount
            print("{:.2f} withdrawn".format(amount / 100))  # CHANGE - print format 2 decimal places and amount is divided by 100
            return amount / 100 # CHANGE - divide by 100
        else:
            print("Withdrawn amount must be more than 0 and less or equal to the Account balance")
            return 0.0  # return 0 because withdrawal has not been allowed. so 0 withdrawn

    # Now we define the show_balance method that was called by __init__ method above
    def show_balance(self):
        print("Balance on account {} is {:.2f}".format(self.name, self._balance / 100))  # CHANGE - print 2 decimal places and balance divided by 100


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

# When you run the code for the first time, you see # Accounts get created

# Account created for John. Balance on # Account John is # 0.00
# 1# 0.10 deposited
# 0.10 deposited
# 0.10 deposited
# 0.30 withdrawn
# Withdrawn amount must be more than 0 and less or equal to the # Account balance
# Balance on # Account John is 1# 0.00
# Account created for Terry. Balance on # Account Terry is # 0.00
# Account created for Graham. Balance on # Account Graham is 9# 0.00
# Account created for Eric. Balance on # Account Eric is 7# 0.00

# When you run code for the second time, the # Accounts already exist, so they will be # Retrieved

# Retrieved record for John. Balance on # Account John is # 0.00
# 1# 0.10 deposited
# 0.10 deposited
# 0.10 deposited
# 0.30 withdrawn
# Withdrawn amount must be more than 0 and less or equal to the # Account balance
# Balance on # Account John is 1# 0.00
# Retrieved record for Terry. Balance on # Account Terry is # 0.00
# Retrieved record for Graham. Balance on # Account Graham is 9# 0.00
# Retrieved record for Eric. Balance on # Account Eric is 7# 0.00


# =====================================
# GUI Database Editing
# =====================================

# We are going to learn about ways to view our database tables without leaving intellij.

# Intellij ultimate edition and Pycharm include a plugin called "Database Tools and SQL".

# This plugin is not available in Intellij community edition, so we will install another plugin called "Database Navigator".


# ==============================================================================
# Intellij Community Edition Database Plugin: Installing "Database Navigator"
# ==============================================================================

# We will watch video to install Database Navigatior

# Close projects to go to main Intellij Idea small screen
# At the bottom right, click Configure > Plugins
# you will see a list of plugins that are already installed. Most were installed with intellij and you cannot uninstall them
# but you can disable them by unchecking them if you like to save some memory.

# Then click > Browse Repositories.
# This will show you all the available plugins so you can install others.
# Then we type "Database Navigator" in the search box and click on it and then install it.
# After it downloads, it gives you option to restart Intellij Idea
# Intellij will restart and the plugin will be enabled and we can use it.

# Start here when updating PYTHON CODE BACKUP

# After restarting intellij, we open the 39_Rollback project again.
# Since the database Navigator is now installed, we need to add it to the display
# Click View > Tool Window > DB Browser
# It opens on the left side and we need to move to right. Settings icon > Move to > right

# Now we will create "New Connection" by clicking the + sign under DB Browser
# Then choose SQlite (note it supports others like Oracle, MySQL, PostgreSQL etc)


# Modify name to "Account" which is descriptive of our database
# Then we need to point it to our SQLite database under Database files
# Note that this needs the full path.
# Click space next to "Database files" then click the ... to open browse window
# then navigate to the folder where your account is and select "accounts.sqlite"
# C:\Users\moe\Documents\Python\IdeaProjects\39_RollingBack\accounts.sqlite

# Then click "Test connection" button and it will verify if connection was successful
# then click Ok
# Now the "Account" Database shows under our DB Browser viewer. Expand it to see the tables "accounts" and "transactions"

# NOTE that we have a "main" under Schemas
# "main" is there because many clients databases allow multiple schemas in the database
# SQLite database can only have a single schema, but because the plugin has been designed for many databases (oracle, SQL etc)
# it gives us an option for main. We can ignore it in SQLite because we will not be using it.

# you will find that any query names the plugin generates, it will prefix them with table name "main.something"

# Now we have access to our database in a GUI
# if we expand transactions > columns and click on time, it will show information about time which includes
# Datatype: timestamp
# Attribute: PK (which means its part of Primary Key)

# We can also doubleclick the tables e.g. accounts table. It will bring a new window where you can add filter with "where"
# select * from main.accounts where
#     name =

# Also note that accounts is prefixed with main.accounts. you can ignore main.
# in our case, we don't want to filter, so we click "No Filter" and it opens "accounts" tab that gives us a list of name and balances
# NOTE that if you specify a filter, DB Browser remembers that filter when you click the table again.
# On the toolbar for "accounts" tab generated, there is a + and - option to insert new row (or record) and delete it
# We add record "Michael" with balance of "500". Note there is a green + next to Michael, meaning its not commited yet.
# Then there is a button to "commit" or to "rollback" the new addition
# If you add new record Terry with balance 0, a similar record exist and it will give you and error and red *
# we can click "rollback" to rollback those changes

# We can also tab to Terry and Make it TerryJ and then commit changes
# We may need to click refresh button to refresh added values in the database.


# since we added new entries in the database, we may need to update code above to account for the new records

# This is "DB Browser plugin" functionality in a nutshell.

# ====================================================
# How to rename tables and columns using "DB Browser"
# ====================================================

# In this case we want to rename table named "transactions" to "history"
# To do the renaming, we have to execute a SQL command
# Click the icon in "DB Browser" named "Open SQL Console" > Account
# This opens a window where we can enter this SQL command

# ALTER TABLE transactions RENAME TO history;
# COMMIT;

# put cursor on at the end of first line and click the "execute" button
# Then put cursor at the end of second line and click "execute" button

# To verify that "transactions" is changed to "history", right click "Tables" > Reload
# you will see that it is changed to "history"





















