# The ATM system should support basic operations such as balance inquiry, cash withdrawal, and cash deposit.
# Users should be able to authenticate themselves using a card and a PIN (Personal Identification Number).
# The system should interact with a bank's backend system to validate user accounts and perform transactions.
# The ATM should have a cash dispenser to dispense cash to users.
# The system should handle concurrent access and ensure data consistency.
# The ATM should have a user-friendly interface for users to interact with.



import threading
from abc import ABC,abstractmethod

class Bank:
    def __init__(self):
        self._lock=threading.RLock()
        self.accounts={
            "1234":{"PIN":0000,"balance":10000.0}
        }
    def validate_pin(self,account_no,pin):
        with self._lock:
            acc=self.accounts.get(account_no)
            return acc is not None and acc["PIN"]==pin
    def get_balance(self,account_no):
        with self._lock:
            return self.accounts[account_no]["balance"]
    def debit_amount(self,account_no,amount):
        with self._lock:
            acc=self.accounts.get(account_no)
            if(not acc):
                print("Invalid account number")
                return False
            current_balance=acc["balance"]
            if(amount>current_balance):
                print("Insufficient Funds")
                return False
            self.accounts[account_no]["balance"]-=amount
            print(f"Amount: ${amount} has been debited from {account_no}")
            return True
    def credit_amount(self,account_no,amount):
        with self._lock:
            acc=self.accounts[account_no]
            if(not acc):
                print("Invalid account number")
                return 
            self.accounts[account_no]["balance"]+=amount
            print(f"Amount: ${amount} has been credited to {account_no}")

class CashDispenser:
    def __init__(self,cash_available=100000):
        self.cash_available=cash_available
        self._lock=threading.RLock()
    def dispense(self,amount):
        with self._lock:
            if(amount>self.cash_available):
                print('ATM out of cash')
                return 
            self.cash_available-=amount
            print(f"Dispensing ${amount} amount. Please collect your cash.")

# STRATEGY PATTERN : for different transaction strategies

class Transaction(ABC):
    @abstractmethod
    def execute(self,atm,transaction,amount=None):
        pass

class BalanceEnquiry(Transaction):
    def execute(self, atm, account_no, amount=None):
        balance=atm.bank.get_balance(account_no)
        print(f"Your balance: {balance}")

class CashWithdrawl(Transaction):
    def execute(self,atm,account_no,amount=None):
        if atm.bank.debit_amount(account_no,amount):
            atm.dispenser.dispense(amount)

class DepositCash(Transaction):
    def execute(self,atm,account_no,amount=None):
        atm.bank.credit_amount(account_no,amount)

# STATE PATTERN - For different ATM states

class ATMState(ABC):
    @abstractmethod
    def insert_card(self,atm,account_no):
        pass
    @abstractmethod
    def enter_pin(self,atm,pin):
        pass
    @abstractmethod
    def do_transaction(self,atm,transaction:Transaction,amount=None):
        pass

class IdleState(ATMState):
    def insert_card(self, atm, account_no):
        atm.current_account=account_no
        atm.set_state(HasCardState())
        print("Card inserted. Please enter PIN")
    def enter_pin(self,atm,pin):
        print("Please insert card first")
    def do_transaction(self, atm, transaction, amount=None):
        print("Please insert card first")

class HasCardState(ATMState):
    def insert_card(self, atm, account_no):
        print("Card already inserted")
    def enter_pin(self, atm, pin):
        if(atm.bank.validate_pin(atm.current_account,pin)):
            atm.set_state(AuthenticatedState())
            print("PIN Correct. Choose a transaction")
        else:
            print("Wrong PIN")
            atm.set_state(IdleState())
    def do_transaction(self, atm, transaction, amount=None):
        print("Enter PIN first.")

class AuthenticatedState(ATMState):
    def insert_card(self, atm, account_no):
        print("Already authenticated")
    def enter_pin(self, atm, pin):
        print("Already entered PIN")
    def do_transaction(self, atm, transaction, amount=None):
        transaction.execute(atm,atm.current_account,amount)
        atm.set_state(IdleState())
        print("Transaction Completed. Card ejected!!")

class ATM:
    def __init__(self,dispenser:CashDispenser,bank:Bank):
        self.bank=bank
        self.dispenser=dispenser
        self.current_account=None
        self.state=IdleState()
    def set_state(self,state):
        self.state=state
    def insert_card(self,account_no):
        self.state.insert_card(self,account_no)
    def enter_pin(self,pin):
        self.state.enter_pin(self,pin)
    def do_transaction(self,transaction,amount=None):
        self.state.do_transaction(self,transaction,amount)

if __name__=='__main__':
    atm = ATM(CashDispenser(),Bank())
    atm.insert_card("1234")
    atm.enter_pin(0000)
    atm.do_transaction(BalanceEnquiry())
    
    atm.insert_card("1234")
    atm.enter_pin(0000)
    atm.do_transaction(CashWithdrawl(),1500)
    
    
