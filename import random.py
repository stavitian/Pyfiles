import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from abc import ABC, abstractmethod

class Organism(ABC):
    def __init__(self, x, y, energy):
        self.x = x
        self.y = y
        self.energy = energy
        self.age = 0

    @abstractmethod
    def update(self, world):
        pass

    @abstractmethod
    def reproduce(self):
        pass

class Plant(Organism):
    def __init__(self, x, y):
        super().__init__(x, y, 50)
        self.growth_rate = random.uniform(0.1, 0.3)

    def update(self, world):
        self.energy += self.growth_rate * world.sunlight
        self.age += 1
        if self.energy > 100:
            self.energy = 100

    def reproduce(self):
        if self.energy > 80 and random.random() < 0.1:
            self.energy -= 30
            return Plant(self.x + random.randint(-1, 1), self.y + random.randint(-1, 1))
        return None

class Animal(Organism):
    def __init__(self, x, y, speed, sense_range):
        super().__init__(x, y, 100)
        self.speed = speed
        self.sense_range = sense_range

    def move(self, world):
        dx, dy = random.randint(-self.speed, self.speed), random.randint(-self.speed, self.speed)
        self.x = (self.x + dx) % world.width
        self.y = (self.y + dy) % world.height

    def find_food(self, world):
        for organism in world.organisms:
            if isinstance(organism, self.food_type):
                distance = ((self.x - organism.x)**2 + (self.y - organism.y)**2)**0.5
                if distance < self.sense_range:
                    return organism
        return None

    def eat(self, food):
        self.energy += food.energy
        food.energy = 0

    def update(self, world):
        self.age += 1
        self.energy -= 1
        food = self.find_food(world)
        if food:
            self.eat(food)
        else:
            self.move(world)

    @abstractmethod
    def reproduce(self):
        pass

class Herbivore(Animal):
    food_type = Plant

    def __init__(self, x, y):
        super().__init__(x, y, speed=2, sense_range=5)

    def reproduce(self):
        if self.energy > 150 and random.random() < 0.05:
            self.energy -= 50
            return Herbivore(self.x, self.y)
        return None

class Carnivore(Animal):
    food_type = Herbivore

    def __init__(self, x, y):
        super().__init__(x, y, speed=3, sense_range=7)

    def reproduce(self):
        if self.energy > 200 and random.random() < 0.03:
            self.energy -= 70
            return Carnivore(self.x, self.y)
        return None

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.organisms = []
        self.sunlight = 1.0
        self.time = 0

    def add_organism(self, organism):
        self.organisms.append(organism)

    def remove_dead_organisms(self):
        self.organisms = [org for org in self.organisms if org.energy > 0]

    def update(self):
        self.time += 1
        self.sunlight = 0.5 + 0.5 * np.sin(self.time / 50)  # Day-night cycle

        for organism in self.organisms:
            organism.update(self)

        new_organisms = []
        for organism in self.organisms:
            child = organism.reproduce()
            if child:
                new_organisms.append(child)

        self.organisms.extend(new_organisms)
        self.remove_dead_organisms()

class Simulation:
    def __init__(self, world_width, world_height):
        self.world = World(world_width, world_height)
        self.fig, self.ax = plt.subplots()
        self.sc = self.ax.scatter([], [], c=[])
        self.ax.set_xlim(0, world_width)
        self.ax.set_ylim(0, world_height)

    def initialize(self):
        for _ in range(50):
            self.world.add_organism(Plant(random.randint(0, self.world.width-1), 
                                          random.randint(0, self.world.height-1)))
        for _ in range(20):
            self.world.add_organism(Herbivore(random.randint(0, self.world.width-1), 
                                              random.randint(0, self.world.height-1)))
        for _ in range(5):
            self.world.add_organism(Carnivore(random.randint(0, self.world.width-1), 
                                              random.randint(0, self.world.height-1)))

    def update(self, frame):
        self.world.update()
        x = [org.x for org in self.world.organisms]
        y = [org.y for org in self.world.organisms]
        colors = ['g' if isinstance(org, Plant) else 'b' if isinstance(org, Herbivore) else 'r' for org in self.world.organisms]
        self.sc.set_offsets(np.c_[x, y])
        self.sc.set_color(colors)
        self.ax.set_title(f"Time: {self.world.time}, Sunlight: {self.world.sunlight:.2f}")
        return self.sc,

    def run(self):
        self.initialize()
        anim = FuncAnimation(self.fig, self.update, frames=1000, interval=50, blit=True)
        plt.show()

if __name__ == "__main__":
    simulation = Simulation(100, 100)
    simulation.run()