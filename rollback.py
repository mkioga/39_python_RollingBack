
# ==============
# rollback.py
# ==============

# =================================================
# Transaction inaccuracies due to rounding errors
# =================================================

# We will now look at how to roll back transactions in databases in situations where its
# important that all transactions are successful

# An example is in bank transfers. We don't want to have one account debited without a similar
# amount being credited to the other account.
# We will use an "Account" class to ensure that both transactions occur or neither of them do.

# we will also look at a new way to view contents of our database from intellij


#
# class Account(object):
#
#     def __init__(self, name: str, opening_balance: float = 0.0):  # define with name as string and opening balance as float initialized to 0.0
#         # then we assign parameters
#         self.name = name
#         self._balance = opening_balance
#         print("Account created for {}. ".format(self.name), end='')
#         self.show_balance()  # We will define this method below. but it is called here to show balance
#
#     # We define the deposit method.
#     def deposit(self, amount: float) -> float:  # Deposit is float and annotation type -> is float
#         if amount > 0.0:
#             self._balance += amount
#             print("{} deposited".format(amount))
#         return self._balance
#
#     # We define the withdrawal method and make sure we don't withdraw more than the balance
#     # Also withdrawal amount must be 0 to count
#     def withdraw(self, amount: float) -> float:
#         if 0 < amount <= self._balance:
#             self._balance -= amount
#             print("{} withdrawn".format(amount))
#             return amount  # This is the amount withdrawn.
#         else:
#             print("Withdrawn amount must be more than 0 and less or equal to the Account balance")
#             return 0.0  # return 0 because withdrawal has not been allowed. so 0 withdrawn
#
#     # Now we define the show_balance method that was called by __init__ method above
#     def show_balance(self):
#         print("Balance on account {} is {}".format(self.name, self._balance))
#
#
# # Now we will write some code to call above functions and test them
# # Note that the balance should be 10.00 although it shows 9.9999. This is because we used float instead of integer.
# # Computer numbers are represented in binary and we lose some accuracy every time we are dividing fractions in binary
#
# # One solution is to use the " decimal class " that comes with python.
# # Check rollback2.py to see how decimal class is used.
#
# if __name__ == '__main__':
#     john = Account("John")  # Give it account name. Default balance is 0.0
#     john.deposit(10.10)
#     john.deposit(0.10)
#     john.deposit(0.10)
#     john.withdraw(0.30)
#     john.withdraw(0)
#     john.show_balance()
#


# ==========================================================
# Working with integer values only to avoid rounding errors
# ==========================================================

# The other thing we can do is work entirely with integer values.
# Integers can be stored exactly in binary so there will be no rounding errors if we make all our arithmetic on integers
# We do this for example if we want to add $ 10.30, we multiply by 100 to make it 1030,
# Then we do transactions with 1030, say divide by 2 to get 515, then after transactions are done
# we divide result by 100 to get 5.15 (in dollars and cents).

# we will change our code as noted by CHANGE


class Account(object):

    def __init__(self, name: str, opening_balance: int = 0):  # CHANGE - use int and initialize it to 0
        # then we assign parameters
        self.name = name
        self._balance = opening_balance
        print("Account created for {}. ".format(self.name), end='')
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




# Next - Create rollback3.py to connect to database.




