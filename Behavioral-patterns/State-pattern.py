from abc import abstractmethod,ABC

class TrafficLightState(ABC):
    @abstractmethod
    def show(self):
        pass
    @abstractmethod
    def next_light(self):
        pass

class RedLight(TrafficLightState):
    def show(self):
        print("RED Light, don't move");
    def next_light(self):
        return GreenLight()

class YellowLight(TrafficLightState):
    def show(self):
        print('Yellow Light,please wait!!')
    def next_light(self):
        return RedLight()

class GreenLight(TrafficLightState):
    def show(self):
        print('Green Light GO GO !')
    def next_light(self):
        return YellowLight()


class TrafficLight:
    def __init__(self):
        self.state=RedLight()
    def show(self):
        self.state.show()
    def change(self):
        self.state=self.state.next_light()


light=TrafficLight()
light.show()
light.change()
light.show()
light.change()
light.show()
light.change()
