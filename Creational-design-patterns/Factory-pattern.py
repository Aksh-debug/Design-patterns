from abc import ABC,abstractmethod

class Toy(ABC):
    @abstractmethod
    def play(self)->None:
        pass

class TeddyBear(Toy):
    def play(self):
        print("Playing with teddy bear")

class Robot(Toy):
    def play(self):
        print("Playing with Robot..")

class ToyMachine:
    _mapping={
        "teddyBear":TeddyBear,
        "robot":Robot
    }
    def makeToy(self,toyName):
        toyClass=self._mapping.get(toyName);
        if toyClass:
            return toyClass()
        print("I do not know how to make this toy!!")
        return None


machine=ToyMachine();
toy1=machine.makeToy('teddyBear')
toy2=machine.makeToy('robot')
toy3=machine.makeToy('cartton')
toy1.play()
toy2.play()
toy3.play()

        