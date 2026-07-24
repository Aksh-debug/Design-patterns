from abc import ABC, abstractmethod
from enum import Enum
import uuid
from datetime import datetime


#vehicle

class VehicleType(Enum):
    CAR="CAR"
    MOTORCYCLE="MOTORCYCLE"
    BUS="BUS"

class Vehicle(ABC):
    def __init__(self,license_plate:str):
        self.license_plate=license_plate
    @property
    @abstractmethod
    def vehicle_type(self):
        pass

class Motorcycle(Vehicle):
    @property
    def vehicle_type(self):
        return VehicleType.MOTORCYCLE

class Car(Vehicle):
    @property
    def vehicle_type(self):
        return VehicleType.CAR
    
class Bus(Vehicle):
    @property
    def vehicle_type(self):
        return VehicleType.BUS

class Vehicle_factory:
    _mappings={
        VehicleType.CAR: Car,
        VehicleType.MOTORCYCLE:Motorcycle,
        VehicleType.BUS:Bus
    }    
    @staticmethod
    def create_vehicle(self,vehicle_type:VehicleType,license_plate:str)->Vehicle:
        vehicle_class=self._mappings.get(vehicle_type)
        if(not vehicle_class):
            raise ValueError("Unsupported vehicle type")
        return vehicle_class(license_plate)

#slot

class SlotSize(Enum):
    SMALL=1
    MEDIUM=2
    LARGE=3

VEHICLE_MIN_SLOT={
    VehicleType.MOTORCYCLE:SlotSize.SMALL,
    VehicleType.CAR:SlotSize.MEDIUM,
    VehicleType.BUS:SlotSize.LARGE
}

class ParkingSlot:
    def __init__(self,slot_id:str,size:SlotSize):
        self.slot_id=slot_id
        self.size=size
        self.vehicle=None
    @property
    def is_free(self):
        return self.vehicle is None
    def park(self,vehicle):
        self.vehicle=vehicle
    def unpark(self):
        self.vehicle=None

#floor

class ParkingFloor:
    def __init__(self,floor_number:int,slots:list[ParkingSlot]):
        self.floor_number=floor_number
        self.slots=slots
    def find_available_slot(self,vehicle_type:VehicleType):
        required_size=VEHICLE_MIN_SLOT[vehicle_type]
        candidates=[
            s for s in self.slots
            if s.is_free and s.size.value>=required_size.value
        ]
        return min(candidates,key=lambda s:s.size.value)


# pricing strategy -> using strategy pattern

class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fee(self,entry_time,exit_time):
        pass

class HourlyFixedRate(PricingStrategy):
    def __init__(self,rate_per_hour):
        self.rate_per_hour=rate_per_hour
    def calculate_fee(self, entry_time, exit_time):
        return f"Fee ₹ ${self.rate_per_hour} per hour"

class SlabPricingRate(PricingStrategy):
    def calculate_fee(self, entry_time, exit_time):
        return f"Fee ₹ 100 for first 2 hours and then it gets pricier"

# ticket

class Ticket:
    def __init__(self,vehicle:Vehicle,slot:ParkingSlot,pricingStrategy:PricingStrategy):
        self.ticketId=str(uuid.uuid4())
        self.vehicle=vehicle
        self.slot=slot
        self.pricingStrategy=pricingStrategy
        self.entryTime=datetime.now()
        self.exitTime=None
    def close(self):
        self.exitTime=datetime.now()
        return self.pricingStrategy.calculate_fee(self.entryTime,self.exitTime)

# Parking lot

class ParkingLot:
    def __init__(self,floors:list[ParkingFloor],pricingStrategy:PricingStrategy):
        self.floors=floors
        self.pricingStrategy=pricingStrategy
        self.active_tickets:dict[str,Ticket]={}
    def park_vehicle(self,vehicle_type,license_plate):
        vehicle=Vehicle_factory.create_vehicle(vehicle_type,license_plate)
        for floor in self.floors:
            slot=floor.find_available_slot(vehicle_type)
            if(slot):
                slot.park(vehicle)
                ticket=Ticket(vehicle,slot,self.pricingStrategy)
                self.active_tickets[license_plate]=ticket
                return ticket
        raise Exception("Parking slot full for this vehicle!!!")
    def unpark_vehicle(self,license_plate):
        ticket=self.active_tickets.pop(license_plate)
        if(not ticket):
            raise Exception("No active ticket found for this vehicle")
        fee=ticket.close()
        ticket.slot.unpark()
        return fee


# demo run

# if __name__ == "__main__":
#     slots_f1 = [
#         ParkingSlot("F1-S1", SlotSize.SMALL),
#         ParkingSlot("F1-M1", SlotSize.MEDIUM),
#         ParkingSlot("F1-L1", SlotSize.LARGE),
#     ]
#     floor1 = ParkingFloor(1, slots_f1)
#     lot = ParkingLot([floor1], HourlyFlatPricing(rate_per_hour=20))

#     ticket = lot.park_vehicle(VehicleType.CAR, "UP80-XY-1234")
#     print(f"Parked in slot {ticket.slot.slot_id}")

#     fee = lot.unpark_vehicle("UP80-XY-1234")
#     print(f"Fee charged: ₹{fee}")
