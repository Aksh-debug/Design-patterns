# Vending machine steps:

# 1. Product Selection
# 2. Payment Validation
# 3. Signal Processing
# 4. Dispensing the Item
# 5. Delivery and confirmation


# these steps are basically different states that a vending machine will be at a particular instance -> state pattern ?
# all these steps will be a different class

# Vending Machine

# Requirements
# The vending machine should support multiple products with different prices and quantities.
# The machine should accept coins and notes of different denominations.
# The machine should dispense the selected product and return change if necessary.
# The machine should keep track of the available products and their quantities.
# The machine should handle multiple transactions concurrently and ensure data consistency.
# The machine should provide an interface for restocking products and collecting money.
# The machine should handle exceptional scenarios, such as insufficient funds or out-of-stock products.


# entities: Vending_Machine, Products, Coins, Inventory

from abc import ABC,abstractmethod
from enum import Enum
import threading

class Denomination(Enum):
    COIN_1=1
    COIN_2=2
    COIN_5=5
    COIN_10=10
    NOTE_50=50
    NOTE_100=100

class Product:
    def __init__(self,name,price,quantity):
        self.name=name
        self.price=price
        self.quantity=quantity
    def __repr__(self):
        return f"{self.name}"

class State(ABC):
    def select_product(self,machine,code):
        print("Cannot select a product")
    def insert_money(self,machine,denomination):
        print("Cannot insert amount")
    def process_signal(self,machine):
        print("Cannot process signal")
    def dispense(self,machine):
        print("cannot dispense right now")
    def deliver(self,machine):
        print("Cannot deliver right now")

class VendingMachine:
    def __init__(self):
        self._inventory={
            "A1":Product("Coke",25,5),
            "A2":Product("Chips",20,3),
            "A3":Product("Water",15,0)
        }
        self.state:State=ProductSelectionState()
        self.selectedCode=None
        self.balance=0
        self._lock=threading.RLock()
        self.txn_lock=threading.Lock()
    def set_state(self,state):
        with self._lock:
            self.state=state
    def select(self,product):
        self.txn_lock.acquire()
        try:
            with self._lock:
                self.state.select_product(self,product)
        except Exception:
            self.txn_lock.release()
            raise
    def insert(self,amount:Denomination):
        with self._lock:
            self.state.insert_money(self,amount)
    def process(self):
        with self._lock:
            self.state.process_signal(self)
    def dispense(self):
        with self._lock:
            self.state.dispense(self) 
    def deliver(self):
        with self._lock:
            self.state.deliver(self)
        self.txn_lock.release()
    def reset_machine(self):
        with self._lock:
            self.balance=0
            self.selectedCode=None

class ProductSelectionState(State):
    def select_product(self, machine:VendingMachine, code:str):
        product=machine._inventory.get(code)
        if(product is None):
            raise ValueError("Invalid product code")
        if(product.quantity<=0):
            raise Exception("Out of stock")
        machine.selectedCode=code
        machine.set_state(PaymentValidationState())
        print("Product Selected")

class PaymentValidationState(State):
    def insert_money(self, machine:VendingMachine, amount:Denomination):
        product=machine._inventory.get(machine.selectedCode)
        change=0
        machine.balance+=amount.value
        if(product.price>machine.balance):
            print("Insufficient funds")
            return
        if(machine.balance>product.price):
            change=machine.balance-product.price
        if(change>0):
            print(f"Change: ${change} is returned")
        print("Payment Validated")
        machine.set_state(ProcessSignalState())

class ProcessSignalState(State):
    def process_signal(self, machine):
        print("sending signal")
        print("signal sent")
        machine.set_state(DispenseState())

class DispenseState(State):
    def dispense(self, machine:VendingMachine):
        product=machine._inventory.get(machine.selectedCode)
        product.quantity-=1
        print("Dispensing product")
        machine.set_state(DeliverState())

class DeliverState(State):
    def deliver(self, machine):
        print("Product is delivered!!")
        machine.reset_machine()
        machine.set_state(ProductSelectionState())
    
            
if __name__ == "__main__":
    vm = VendingMachine()
    vm.select("A1")
    vm.insert(Denomination.COIN_10)
    vm.insert(Denomination.COIN_10)
    vm.insert(Denomination.COIN_10)   # balance hits 30, price 25 -> change $5
    vm.process()
    vm.dispense()
    vm.deliver()
        
