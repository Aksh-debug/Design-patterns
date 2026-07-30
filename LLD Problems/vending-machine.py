# Vending machine steps:

# 1. Product Selection
# 2. Payment Validation
# 3. Signal Processing
# 4. Dispensing the Item
# 5. Delivery and confirmation


# these steps are basically different states that a vending machine will be at a particular instance -> state pattern ?
# all these steps will be a different class

from abc import ABC,abstractmethod

class Product:
    def __init__(self,name,price,quantity):
        self.name=name
        self.price=price
        self.quantity=quantity
    def __repr__(self):
        return f"{self.name} (₹{self.price}, qty={self.quantity})"

    
# this base class State basically contains all the methods that will be used by different states
class State(ABC):
    """
    Base State. Every concrete state overrides only the
    method(s) relevant to it. The rest fall back to this
    default "not allowed" behavior.
    """
    def select_product(self,machine,code):
        print("cannot select a product right now")
    def insert_money(self,machine,amount):
        print("cannot insert money right now")
    def process_signal(self,machine):
        print('cannot process dispensing signal right now')
    def dispense(self,machine):
        print('cannot dispense right now')
    def deliver(self,machine):
        print('cannot deliver right now')

class VendingMachine:
    def __init__(self):
        self.inventory={
            "A1": Product("Coke", 25, 5),
            "A2": Product("Chips", 20, 3),
            "A3": Product("Water", 15, 0)
        }
        self.state=ProductSelectionState()
        self.balance=0
        self.selectedCode=None

    def select(self,code):
        self.state.select_product(self,code)
    def insert(self,amount):
        self.state.insert_money(self,amount)
    def process(self):
        self.state.process_signal(self)
    def dispense(self):
        self.state.dispense(self)
    def deliver(self):
        self.state.deliver(self)
    def setState(self,nextState):
        self.state=nextState
    def reset_machine(self):
        self.balance=0
        self.selectedCode=None

class ProductSelectionState(State):
    def select_product(self,machine,code):
        product=machine.inventory.get(code)
        if(product is None):
            print("Invalid product code")
            return 
        if(product.quantity<=0):
            print("Out of stock")
            return 
        machine.selectedCode=code
        print(product.name,'is selected')
        machine.setState(PaymentValidationState())

class PaymentValidationState(ABC):
    def insert_money(self,machine,amount):
        product=machine.inventory.get(machine.selectedCode)
        machine.balance+=amount
        if(machine.balance<product.price):
            print('insufficient funds')
            return 
        print('payment processed')
        machine.setState(ProcessSignalState())

class ProcessSignalState(ABC):
    def process_signal(self,machine):
        print('sending signal')
        print('signal sent')
        machine.setState(DispenseState())

class DispenseState(ABC):
    def dispense(self,machine):
        product=machine.inventory[machine.selectedCode]
        product.quantity-=1
        print('dispensing product...')
        machine.setState(DeliverState())

class DeliverState(ABC):
    def deliver(self,machine):
        print('product is delivered')
        machine.reset_machine()
        machine.setState(ProductSelectionState())


vm=VendingMachine()
vm.select('A2')
vm.insert(20)
vm.process()
vm.dispense()
vm.deliver()
