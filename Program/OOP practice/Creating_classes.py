name = "John"
age = 18
print(type(name), type(age)) #Will output string and integer respectively. 
'''
Class
-A blueprint, template, or prototype used to build objects. It defines the -structure, data type, and allowable behaviors.
An architectural blueprint for a house.

Object
-A specific instance created from a class. It has actual data and occupies memory space.
-The physical house built from that blueprint.
'''
#methods allow you to manipulate objects like .strip(), .replace()
class dog:
    def bark(self):
        print("Whoof whoof!")
    #this is an example of a method. it is a function
    #we can add attributes/data here 
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

dog1 = dog("Bruce", "Scottish Terrier")

# Create a class
class Person:
	def __init__(self,name, age):
		self.name=name
		self.age = age
	def greet(self):
		print("hello my name is ", self.name)

# Create an object
p1 = Person("John", 36)
p1.greet()
# Call the greet method


class Car: 
      def __init__(self, model, year, colour, for_sale):
        self.model = model
        self.year = year 
        self.colour = colour
        self.forsale = for_sale

car1 = Car("Mustang", "2024", "red", False)
print(car1.model) #Mustang
print(car1.colour) #red

car2 = Car("Corvette", "2022", "blue", True)
print(car2.forsale) #True
print(car2)