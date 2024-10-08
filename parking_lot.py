import uuid
from datetime import datetime


class Vehicle:
    def __init__(self,license_plate,size):
        self.license_plate=license_plate
        self.size=size
        print(f"license plate {self.license_plate}, {self.size}")
    

class ParkingSlot:
    def __init__(self,slot_id,size):
        self.slot_id=slot_id
        self.size=size
        self.is_occupied=False
        print(f"slot_id {self.slot_id},size {self.size} , occupied {self.is_occupied}")
    
    def is_available(self):
        return not self.is_occupied

class ParkingTicket:
    def __init__(self,vehicle,level,slot):
        self.ticket_id=str(uuid.uuid4())
        self.vehicle=vehicle
        self.level=level
        self.slot=slot
        self.entry_time=datetime.now()

        print("tickettt",self.ticket_id,self.vehicle,self.level,self.slot,self.entry_time)


class Level:
    def __init__(self,level_number,num_slots):
        self.level_number=level_number
        self.slots=[]
        self.available_slot_by_size={
            "small":[],
            "medium":[],
            "large":[]
        }

        for i in range(num_slots):
            print(i,num_slots//3,(2*num_slots)//3)
            if i < num_slots//3:
                slot=ParkingSlot(i,"small")
            elif i < (2*num_slots)//3:
                slot=ParkingSlot(i,"medium")
            else:
                slot=ParkingSlot(i,"large")
            self.slots.append(slot)
            self.available_slot_by_size[slot.size].append(slot)
        print(self.available_slot_by_size)
    
    def find_available_slot(self,vehicle):
        if vehicle.size in self.available_slot_by_size:
            available_slots=self.available_slot_by_size[vehicle.size]

            for slot in available_slots:
                if slot.is_available():
                    return slot
                
        return None
    
    def park_vehicle(self,vehicle,slot):
        slot.is_occupied=True
        self.available_slot_by_size[slot.size].remove(slot)
    
    def unpark_vehicle(self,slot):
        self.is_occupied=False
        self.available_slot_by_size[slot.size].append(slot)


class ParkingLot:
    def __init__(self,num_levels,slot_per_level):
        self.levels=[]
        self.vehicles_to_ticket={}
        for i in range(num_levels):
            self.levels.append(Level(i,slot_per_level))



    def park_vehicle(self,vehicle):
        for level in self.levels:
            slot=level.find_available_slot(vehicle)
            if slot:
                ticket=ParkingTicket(vehicle,level,slot)
                self.vehicles_to_ticket[vehicle.license_plate]=ticket
                level.park_vehicle(vehicle,slot)
                return ticket
        return None


    def unpark_vehicle(self,license_plate):
        if license_plate in self.vehicles_to_ticket:
            ticket=self.vehicles_to_ticket.pop(license_plate)
            level=ticket.level
            slot=ticket.slot
            level.unpark_vehicle(slot)
            return ticket
        return None


parking_lot=ParkingLot(3,10) # 3 levels, 10 slots per level

vehicle1=Vehicle("Creta","medium")
vehicle2=Vehicle("Thar","large")

ticket1=parking_lot.park_vehicle(vehicle1)
print(f"vehicle {vehicle1.license_plate} parked at level {ticket1.level.level_number}, slot {ticket1.slot.slot_id}")

ticket2=parking_lot.park_vehicle(vehicle2)
print(f"vehicle {vehicle2.license_plate} parked at level {ticket2.level.level_number}, slot {ticket2.slot.slot_id}")

unparked_ticket=parking_lot.unpark_vehicle(vehicle1.license_plate)
print(f"vehicle {unparked_ticket.vehicle.license_plate} unparked from level {unparked_ticket.level.level_number} ,slot {unparked_ticket.slot.slot_id}")