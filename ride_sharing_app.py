from datetime import datetime
# To calculate distance based on location
from geopy.distance import geodesic

class Driver:
    def __init__(self,driver_id,name,location,car_details):
        self.driver_id=driver_id
        self.name=name
        self.location=location   # Tuple (latitude, longitude)
        self.available=True
        self.car_details=car_details
        self.current_date=None
    
    def update_location(self,new_loaction):
        self.location=new_loaction

    def assign_ride(self,ride):
        self.current_ride=ride
        self.available=False
    
    def complete_ride(self):
        self.current_ride=None
        self.available=True
    

class Rider:
    def __init__(self,rider_id,name,location):
        self.rider_id=rider_id
        self.name=name
        self.location=location
    
    def request_ride(self,pickup_location,dropoff_location):
        """Request a ride by specifying pickup and dropoff locations."""
        return Ride(self, pickup_location, dropoff_location)
    
class Ride:
    def __init__(self,rider,pickup_location,dropoff_location):
        self.rider= rider
        self.pickup_location=pickup_location
        self.dropoff_location=dropoff_location
        self.driver=None
        self.fare=0
        self.status="Pending"  # Ride statuses: Pending, Ongoing, Completed, Canceled
        self.start_time=None
        self.end_time=None
    

    def assign_driver(self,driver):
        self.driver=driver
        self.status="Ongoing"
        self.start_time=datetime.now()

    def complete_ride(self):
        self.status="Completed"
        self.end_time=datetime.now()
        self.fare=self.calculate_fare()


    def calculate_fare(self):        
        """Calculate fare based on distance between pickup and dropoff locations."""
        distance=geodesic(self.pickup_location,self.dropoff_location).kilometers
        base_fare=2.5
        fare_per_km=1.2
        return base_fare + (fare_per_km*distance)
    
    def cancel_ride(self):
        self.status="Canceled"

class RideSharingService:
    def __init__(self):
        self.drivers=[]  # List of registered drivers
        self.rides=[]    # List of active ride requests

    def registered_driver(self,driver):
        """Add a driver to the system."""
        self.drivers.append(driver)

    def find_nearest_driver(self,rider_location):
        """Find the nearest available driver to the rider."""
        nearest_driver=None
        min_distance=float('inf')

        for driver in self.drivers:
            if driver.available:
                distance=geodesic(rider_location,driver.location).kilometers
                if distance<min_distance:
                    nearest_driver=driver
                    min_distance=distance
        
        return nearest_driver
    
    
    def request_ride(self,rider,pickup_location,dropoff_location):
        ride=rider.request_ride(pickup_location,dropoff_location)
        nearest_driver=self.find_nearest_driver(pickup_location)

        if nearest_driver:
            ride.assign_driver(nearest_driver)
            nearest_driver.assign_ride(ride)
            self.rides.append(ride)
            return f"Ride assigned to {nearest_driver.name}."
        else:
            return "No available drivers at the moment"
    
    def cancel_ride(self,ride):
        """Cancel a ride and release the driver."""
        ride.cancel_ride()
        if ride.driver:
            ride.driver.complete_ride()
        self.rides.remove(ride)
    
    def complete_ride(self,ride):
        """Complete a ride and calculate the fare."""
        ride.complete_ride()
        ride.driver.complete_ride()
        self.rides.remove(ride)
        return f"Ride completed. Fare: {ride.fare}"
    
# Initialize the ride-sharing service
service=RideSharingService()

# Register some drivers
driver1=Driver(1,"Alice",(40.7128,-74.0060),"Toyota Prius")
driver2=Driver(2,"Bob",(40.7129,-74.0070),"Honda Civic")


service.registered_driver(driver1)
service.registered_driver(driver2)

# Register a rider
rider=Rider(1,"John",(40.7120,-74.0100))

# Rider requests a ride
ride_info=service.request_ride(rider,(40.7120,-74.0100),(40.7300,-74.0010))
print(ride_info) # Should assign a driver to the ride

# Complete the ride
ride=service.rides[0]    # Get the first active ride
fare_info=service.complete_ride(ride)
print(fare_info)        # Output the ride fare and completion status

