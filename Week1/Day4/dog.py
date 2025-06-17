# Goal: Create a Dog class with methods for barking, running speed, and fighting.

# Instructions:

# Step 1: Create the Dog Class

# Create a class called Dog with name, age, and weight attributes.
# Implement a bark() method that returns “ is barking”.
# Implement a run_speed() method that returns weight / age * 10.
# Implement a fight(other_dog) method that returns a string indicating which dog won the fight, based on run_speed * weight.


# Step 2: Create Dog Instances

# Create three instances of the Dog class with different names, ages, and weights.


# Step 3: Test Dog Methods

# Call the bark(), run_speed(), and fight() methods on the dog instances to test their functionality.

class Dog:
    def __init__(self, name, age, weight):
        # ... code to initialize attributes ...
        self.name = name
        self.age = age
        self.weight = weight

    def bark(self):
        # ... code to return bark message ...
        return "is barking"

    def run_speed(self):
        # ... code to return run speed ...
        return self.weight / self.age * 10

    def fight(self, other_dog):
        # ... code to determine and return winner ...
        if other_dog.run_speed() > self.run_speed() :
            return f"{other_dog.name} won the fight"
        else : 
            return f"{self.name} won the fight"

# Step 2: Create dog instances
#... your code here
dog1 = Dog("rex", 5, 75)
dog2 = Dog("plume", 2, 30)
dog3 = Dog("teeth", 6, 90)

# Step 3: Test dog methods
print(dog1.bark())
print(dog2.run_speed())
print(dog1.fight(dog2))