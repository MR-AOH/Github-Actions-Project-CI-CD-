import pygame
from TrafficLight import TrafficLight
from utils import Direction, WINDOW_WIDTH, WINDOW_HEIGHT, WHITE, BLACK, RED, GREEN, YELLOW, BLUE, GRAY, DARK_GRAY, LIGHT_GRAY
from RoadsCreation import Road
from CarsCreation import Car, EmergencyVehicle
from main import TrafficSimulation

def test_traffic_light_color_change():
    light = TrafficLight()
    light.change_color("Green")
    assert light.get_color() == "Green"

def test_car_stops_on_red_light():
    car = Car("TestCar", Direction.NORTH)
    # Position car near the stop zone
    car.y = WINDOW_HEIGHT // 2 + 50
    stopped = not car.update("Red")
    assert stopped is True
    assert car.waiting is True

def test_emergency_vehicle_forced_green_light():
    simulation = TrafficSimulation()
    emergency_vehicle = EmergencyVehicle("Ambulances", Direction.NORTH)
    road = Road("North Road", Direction.NORTH)
    road.add_car(emergency_vehicle)
    simulation.roads = [road]
    simulation.emergency_mode = True
    simulation.emergency_road_index = Direction.NORTH.value
    road.update_cars(simulation)
    assert road.traffic_light.get_color() == "Green"
