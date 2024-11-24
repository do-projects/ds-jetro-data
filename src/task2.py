import datetime

class BankSystem:
    #dictionary of transactions to store
    
    def __init__(self):
        self.checking_account = 0
        self.savings_account = 0
        self.transactions = {} 
        self.transaction_counter = 1

    def records(self, details):
        
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")   #timestamp to consider the current date and time
        transaction_id = f"{self.transaction_counter}.{timestamp}"
        self.transaction_counter += 1
        self.transactions.update({transaction_id:details})

    #functions: deposit, withdraw, transfer between accounts
    def deposit(self, amount, acc_type):
        if acc_type=="checking":   #depositing into checking account
            self.checking_account += amount
            self.records(f"Deposit of ${amount} has been credited to your checking account, Available balance is ${self.checking_account}")
        else:
            acc_type=="savings"   #depositing into savings account
            self.savings_account += amount
            self.records(f"Deposit of ${amount} has been credited to your savings account, Available balance is ${self.savings_account}")

    def withdraw(self, amount, acc_type):
        if acc_type=="checking":   #withdrawal from checking account
            if 0<amount<self.checking_account:
                self.checking_account -= amount
                self.records(f"Withdrawal of ${amount} has been debitted from your checking account, Available balance is ${self.checking_account}")
            else:
                raise ValueError("Insufficient funds in your checking account")
        elif acc_type=="savings":   #withdrawal from savings account
            if 0<amount<self.savings_account:
                self.savings_account -= amount
                self.records(f"Withdrawal of ${amount} has been debitted from your savings account, Available balance is ${self.savings_account}")
            else:
                raise ValueError("Insufficient funds in your savings account")
        else:
            raise ValueError("Invalid, use 'checking' or 'savings' account type")

    def transfer(self, amount, from_acc, to_acc):   #transfer between accounts
        if from_acc == "checking" and to_acc == "savings":   #transfer from  checking to savings
            if 0<amount<self.checking_account:
                self.checking_account -= amount
                self.savings_account += amount
                self.records(f"${amount} transferred from your checking account to savings account")
            else:
                raise ValueError("Insufficient funds in your checking account")
        elif from_acc == "savings" and to_acc == "checking":   #transfer from savings to checking
            if 0<amount<self.savings_account:
                self.savings_account -= amount
                self.checking_account += amount
                self.records(f"${amount} transferred from your savings account to checking account")
            else:
                raise ValueError("Insufficient funds in your savings account")
        else:
            raise ValueError("Invalid, use 'checking or 'savings' account type")

    def show_records(self):
        for time, details in self.transactions.items():
            print(f"{time}: {details}")