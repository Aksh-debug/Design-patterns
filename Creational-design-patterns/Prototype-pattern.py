import copy

class Robot:
    def __init__(self,name,color):
        self.name=name
        self.color=color
        self.backpack=[]

    def clone(self):
        return copy.deepcopy(self)
    
    def show(self):
        print(f"${self.name} of ${self.color} color carrying: ${self.backpack}")


ob1=Robot("Warrior","Blue")
ob2=ob1.clone()
ob2.name="Shobhit"
print(ob1.name,ob2.name)