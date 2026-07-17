class Burger:
    def __init__(self):
        self.parts=[]
    def show(self):
        print("Your Burger contains:")
        for ingredient in self.parts:
            print(ingredient,end=",")

class Builder:
    def __init__(self):
        self.burger=Burger()
    def add_cheese(self):
        self.burger.parts.append('cheese')
        return self
    def add_bun(self):
        self.burger.parts.append('bun')
        return self
    def add_patty(self):
        self.burger.parts.append('patty')
        return self
    def add_bacon(self):
        self.burger.parts.append('bacon')
        return self
    def build(self):
        return self.burger


my_burger=Builder().add_bun().add_patty().add_cheese().add_bacon().build()
my_burger.show()


