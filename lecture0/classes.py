class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(2, 8)
print(p.x)
print(p.y)

class Flight():
    # def is a method aka a function
    # creates a flight
    def __init__(self, capacity):
        # set the input equal to flight's capacity
        self.capacity = capacity
        # create an empty list of passengers
        self.passengers = []
    
    def add_passenger(self, name):
        # if there are no open seats return false
        if not self.open_seats():
            return False
        # there are open seats so add name to passenger list
        self.passengers.append(name)
        return True

    # tells us how many seats are left
    def open_seats(self):
        return self.capacity - len(self.passengers)

flight = Flight(3)

people = ["Anna", "Richie", "Hermione", "Ron"]
for person in people:
    if flight.add_passenger(person):
        print(f"Added {person} in flight successfully.")
    else:
        print("There are no available seats")