from datetime import datetime

class Room:
    def __init__(self,room_number,room_type,price):
        self.room_number=room_number
        self.room_type=room_type
        self.price=price
        self.bookings=[] # List to track bookings

    def is_available(self,check_in,check_out):
        """Check if the room is available for the given date range."""
        for booking in self.bookings:
            if not (check_out<=booking.check_in or check_in>=booking.check_out):
                return False # Overlapping booking found
        return True
    
    def book_room(self,booking):
        self.bookings.append(booking)

class Guest:
    def __init__(self,guest_id,name,contact_info):
        self.guest_id=guest_id
        self.name=name
        self.contact_info=contact_info
        self.bookings=[] # A guest can have multiple bookings
    
    def add_booking(self,booking):
        self.bookings.append(booking)


class Booking:
    def __init__(self,guest,room,check_in,check_out):
        self.guest=guest
        self.room=room
        self.check_in=check_in
        self.check_out=check_out
        self.status="Reserved"
    
    def check_in_guest(self):
        self.status="Checked_in"
    
    def check_out_guest(self):
        self.status="Checked_out"
        

class HotelManagementSystem:
        def __init__(self):
            self.rooms=[]
            self.guests=[]
            self.bookings=[]# List of bookings
        
        def add_room(self,room_number,room_type,price):
            room=Room(room_number,room_type,price)
            self.rooms.append(room)
        
        def register_guest(self,guest_id,name,contact_info):
            guest=Guest(guest_id,name,contact_info)
            self.guests.append(guest)
            return guest
        
        def make_booking(self,guest_id,room_number,check_in_str,check_out_str):
            guest= next((g for g in self.guests if g.guest_id==guest_id),None)
            room = next((r for r in self.rooms if r.room_number==room_number),None)

            if not guest or not room:
                return "Guest or room not found"
        
            check_in=datetime.strptime(check_in_str,"%Y-%m-%d")
            check_out=datetime.strptime(check_out_str,"%Y-%m-%d")

            if room.is_available(check_in,check_out):
                booking=Booking(guest,room,check_in,check_out)
                room.book_room(booking)
                guest.add_booking(booking)
                self.bookings.append(booking)
                return f"Booking Successful for room room: {room_number}"
            else:
                return "Room is not available for the selected dates"
        
        def check_room_availability(self,room_number,check_in_str,check_out_str):

            room=next((r for r in self.rooms if r.room_number==room_number),None)
            if not room:
                return "Room not found"
            

            check_in=datetime.strptime(check_in_str,"%Y-%m-%d")
            check_out=datetime.strptime(check_out_str,"%Y-%m-%d")

            if room.is_available(check_in,check_out):
                return f"Room {room_number} is available"
            else:
                return f"Room {room_number} is not available"
            


hotel_system=HotelManagementSystem()

hotel_system.add_room(101,"single",100)
hotel_system.add_room(102,"double",150)

guest=hotel_system.register_guest(1,"Komal Singh","komal@gmail.com")


print(hotel_system.make_booking(1,101,"2024-10-15", "2024-10-18"))
print(hotel_system.make_booking(1, 101, "2024-10-17", "2024-10-19"))  # Room is not available

print(hotel_system.check_room_availability(102, "2024-10-15", "2024-10-18"))  # Room 102 is available
