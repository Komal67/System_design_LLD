from datetime import datetime

class Movie:
    def __init__(self,movie_id,name,genre,length):
        self.movie_id=movie_id
        self.name=name
        self.genre=genre
        self.length=length

    def get_movie_details(self):
        return f"{self.name} ({self.genre}) - {self.length} minutes"
    

class Seat:
    def __init__(self,seat_number):
        self.seat_number=seat_number
        self.is_booked=False
    
    def book_seat(self):
        if not self.is_booked:
            self.is_booked=True
            return True
        return False
    
    def cancel_seat(self):
        if self.is_booked:
            self.is_booked=False
            return True
        return False

class Screen:
    def __init__(self,screen_number,num_seats):
        self.screen_number=screen_number
        self.seats= [Seat(seat_num) for seat_num in range(1,num_seats+1)]
    
    def get_available_seats(self):
        return [seat for seat in self.seats if not seat.is_booked]
    
    def book_seats(self,seat_numbers):
        booked_seats=[]
        for seat_number in seat_numbers:
            seat=self.seats[seat_number-1]
            if seat.book_seat():
                booked_seats.append(seat)
        return booked_seats
    
    def cancel_seats(self,seat_numbers):
        for seat_number in seat_numbers:
            self.seats[seat_number-1].cancel_seat()
            

class ShowTiming:
    def __init__(self,movie,screen,show_time):
        self.movie=movie
        self.screen=screen
        self.show_time=show_time

    def get_show_details(self):
        return f"{self.movie.get_movie_details()} on Screen {self.screen.screen_number} at {self.show_time.strftime('%Y-%m-%d %H:%M')}"
    
    def available_seats(self):
        return self.screen.get_available_seats()
    
    def book_seats(self,seat_numbers):
        return self.screen.book_seats(seat_numbers)
    
    def cancel_seats(self,seat_numbers):
        return self.screen.cancel_seats(seat_numbers)
    
class Theatre:
    def __init__(self,theatre_id,name,num_screens):
        self.theatre_id=theatre_id
        self.name=name
        self.screens=[Screen(screen_num,50) for screen_num in range(1,num_screens+1)]
        self.show_timings=[]

    def add_show_timing(self,movie,screen_number,show_time):
        screen=self.screens[screen_number-1]
        show_timing=ShowTiming(movie,screen,show_time)
        self.show_timings.append(show_timing)
        return show_timing
    
    def search_movie(self,movie_name):
        shows=[show for show in self.show_timings if show.movie.name.lower()==movie_name.lower()]
        return shows

class Booking:
    def __init__(self,booking_id,patron_name,show,seat_numbers):
        self.booking_id=booking_id
        self.patron_name=patron_name
        self.show=show
        self.seat_numbers=seat_numbers
        self.is_active=True

    def complete_booking(self):
        if self.is_active:
            booked_seats=self.show.book_seats(self.seat_numbers)
            if booked_seats:
                print(f"Booking confirm for {self.patron_name}")
                return True
        return False
    
    def cancel_booking(self):
        if self.is_active:
            self.show.cancel_seats(self.seat_numbers)
            print(f"Booking canceled for {self.patron_name}")




theatre = Theatre("T001","Grand Cinema",3)
movie1=Movie("M001","Inception","Sci-Fi",148)
movie2=Movie("M002","Avengers","Action",180)

theatre.add_show_timing(movie1,1,datetime(2024,9,20,15,0))
theatre.add_show_timing(movie2,2,datetime(2024,9,20,18,0))

shows = theatre.search_movie("Inception")
for show in shows:
    print(show.get_show_details())
    print(f"Available seats: {[seat.seat_number for seat in show.available_seats()]}")


# Create a booking
show = shows[0]  # Assume the user selects the first show
seat_numbers = [1, 2, 3]  # User selects these seat numbers
booking = Booking("B001", "John Doe", show, seat_numbers)
booking.complete_booking()

# Cancel the booking
booking.cancel_booking()