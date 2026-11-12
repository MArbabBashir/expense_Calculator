from operator import length_hint


class vehicle:
    def __init__(self, name, max_speed, mil_age):
        self.name  = name
        self.max_speed = max_speed
        self.mil_age = mil_age
        print(name, max_speed, mil_age)

car1 = vehicle("Tesla Model S", 250, 18)

class Rectangle:
    def __init__(self, width, length):
        self.width = width
        self.length = length
    def area(self):
        return self.width * self.length
    def perimeter(self):
        return 2*(self.width + self.length)

rect = Rectangle(10,4)
print(f"Area = {rect.area()} and Perimeter = {rect.perimeter()}")


class Student:
    def __init__(self, name:str, marks:list):
        self.name = name
        self.marks = marks
    def average(self):
        return sum(self.marks)/len(self.marks)

std = Student("Alice", [85, 90, 78, 92,88])
print(f"{std.name} Average Grade: {std.average()}")




print("======Product class with stock value calculator======")


class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
    def total_stock_value(self):
        return self.quantity * self.price

p1 = Product("Laptop", 899.99, 5)
print(f"{p1.name} Total Stock Value: {p1.total_stock_value()}")

print("====== Bank Account with Deposit & Overdraw Protection ======")


class BankAccount:
    def __init__(self, balance):
        self.balance =balance
    def deposit(self, amount):
        self.balance += amount
        print(f"Balance after deposit: {self.balance}")
    def withdraw(self,amount):
        if amount > self.balance:
            print(f"Insufficient funds. Current balance: {self.balance}")
        else:
            self.balance -= amount
            print(f"Balance after withdraw: {self.balance}")


acc1 = BankAccount(1000)
acc1.deposit(500)
acc1.withdraw(200)
acc1.withdraw(2000)


print("====== Light Class with On/Off State Toggle ======")

class Light:
    def __init__(self, state=True):
        self.state = state
    def turn_on(self):
        self.state = True
        print("Light is ON")
    def turn_off(self):
        self.state = False
        print("Light is OFF")
    def status(self):
        print(self.state)
        print(f"Current Status: {self.state}")
    def toggle(self):
        self.state = not self.state
        print("Toggling...")
        print(f"Current Status: {self.state}")

energy_Saver = Light()

energy_Saver.turn_on()
energy_Saver.turn_off()

energy_Saver.toggle()


print("====== User Class with Password Validation ======")

class User:
    def __init__(self,name, password):
        self.name = name
        self.password = password
    def check_password(self):

        password = input("Please enter your password: ")
        if self.password == password:
            print("Password Match")
            return True
        else:
            print("Password not match")
            return False
usr1 = User("arbab bashir", "ArbabBashir")
usr1.check_password()

print("====== Exercise 9: Temperature Class with Unit Converters ======")

class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius
    def to_fahrenheit(self):
        return (self.celsius * 9 / 5) + 32.
    def to_kelvin(self):
        return self.celsius  + 273.15

temp1 = Temperature(100)
print(f"Celcius: {temp1.celsius}")
print(f"Fahrenheit: {temp1.to_fahrenheit()}")
print(f"Kelvin: {temp1.to_kelvin()}")


print("====== Exercise 10: Notebook Class with Add & Display Notes ======")

class Notebook:
    def __init__ (self, names:list):
        self.names = names
    def add_note(self,name):

        self.names.append(name)
        # self.names.append(name_2)

    def show_note(self):
        for i,name in enumerate (self.names):
            print(f"{i}: {name}")

note_book = Notebook(["buy groceries"])
note_book.add_note("read a book")
note_book.add_note("learn more and more")

note_book.show_note()


names = [1,2,3,4,5,6,7,8,]

for i,name in enumerate( names) :
    print(f"{i}: {name}")