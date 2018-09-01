
# =============
# rollback2.py
# =============

# ==================================================
# Using decimal class to get rid of rounding errors
# ==================================================

# The main program still uses float values but the Account class converts them to decimal objects
# So the users are allowed to use float values but then they are converted to decimal for storage.

# if you run this code, you will see the balance is 10.00 and not 9.99999999
# So there are no rounding errors.



from decimal import *
 
 
class Account(object):
    _qb = Decimal('0.00')  # class constant, accessible without creating an instance.
 
    def __init__(self, name: str, opening_balance: float = 0.0):
        self.name = name
        self._balance = Decimal(opening_balance).quantize(Account._qb)  # Converts floats to decimal objects
        print("Account created for {}. ".format(self.name), end='')
        self.show_balance()
 
    def deposit(self, amount: float) -> Decimal:
        decimal_amount = Decimal(amount).quantize(Account._qb)    # Converts floats to decimal objects
        if decimal_amount > Account._qb:
            self._balance = self._balance + decimal_amount
            print("{} deposited".format(decimal_amount))
        return self._balance
 
    def withdraw(self, amount: float) -> Decimal:
        decimal_amount = Decimal(amount).quantize(Account._qb)    # Converts floats to decimal objects
        if Account._qb < decimal_amount <= self._balance:
            self._balance = self._balance - decimal_amount
            print("{} withdrawn".format(decimal_amount))
            return decimal_amount
        else:
            print("The amount must be greater than zero and no more than your account balance")
            return Account._qb
 
    def show_balance(self):
        print("Balance on account {} is {}".format(self.name, self._balance))
 
 
if __name__ == '__main__':
    tim = Account("Tim")
    tim.deposit(10.1)
    tim.deposit(0.1)
    tim.deposit(0.1)
    tim.withdraw(0.3)
    tim.withdraw(0)
    tim.show_balance()
 
    print("=" * 80)
    x = tim.withdraw(900)
    print(x)