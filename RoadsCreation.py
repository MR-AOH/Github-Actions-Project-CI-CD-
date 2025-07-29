
from enum import Enum
from utils import Direction, WHITE, BLACK, RED, GREEN, YELLOW, BLUE, GRAY, DARK_GRAY, LIGHT_GRAY
from TrafficLight import TrafficLight

import pygame
import time


WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
class Road:
    def __init__(self, name, direction):
        self.name = name
        self.direction = direction
        self.traffic_light = TrafficLight()
        self.cars = []

    def add_car(self, car):
        self.cars.append(car)

    def remove_car(self, car):
        if car in self.cars:
            self.cars.remove(car)

    def update_cars(self, simulation):
        from CarsCreation import EmergencyVehicle
        cars_to_remove = []
        for i, car in enumerate(self.cars):
            front_car = self.cars[i - 1] if i > 0 else None
            light_color = self.traffic_light.get_color()
            
            if isinstance(car, EmergencyVehicle):
                # Check if ambulance is near the intersection
                near = False
                if car.direction == Direction.NORTH and car.y < WINDOW_HEIGHT // 2 + 100:
                    near = True
                elif car.direction == Direction.SOUTH and car.y > WINDOW_HEIGHT // 2 - 100:
                    near = True
                elif car.direction == Direction.EAST and car.x > WINDOW_WIDTH // 2 - 100:
                    near = True
                elif car.direction == Direction.WEST and car.x < WINDOW_WIDTH // 2 + 100:
                    near = True

                if near and not simulation.emergency_mode:
                    # Activate emergency mode and set all lights to red except this one
                    simulation.emergency_mode = True
                    simulation.emergency_road_index = self.direction.value
                    pygame.display.set_caption(f"🚨 Emergency override: Opening signal for {self.name} road")
                    
                    # Set all lights to red first, then this one to green
                    for road in simulation.roads:
                        road.traffic_light.change_color("Red")
                    time.sleep(0.1)  # Brief pause
                    self.traffic_light.change_color("Green")
                    
                    try:
                        pygame.mixer.Sound("siren.wav").play()
                    except:
                        pass
                
                # Emergency vehicles always get green light
                light_color = "Green" if simulation.emergency_mode and simulation.emergency_road_index == self.direction.value else light_color
            
            should_remove = car.update(light_color, front_car)
            if should_remove:
                cars_to_remove.append(car)
        
        for car in cars_to_remove:
            self.remove_car(car)
