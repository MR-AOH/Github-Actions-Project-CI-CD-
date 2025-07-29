import pygame
import time
import threading
import random
from utils import Direction, WHITE, BLACK, RED, GREEN, FPS, DARK_GRAY, WINDOW_WIDTH, WINDOW_HEIGHT
from CarsCreation import Car, EmergencyVehicle
from RoadsCreation import Road
# Initialize Pygame
pygame.init()


pygame.mixer.init()
try:
    pygame.mixer.Sound("siren.wav")  # Load a siren sound if available
except:
    pass


class TrafficSimulation:
    def __init__(self):
        self.roads = [
            Road("West", Direction.WEST),
            Road("East", Direction.EAST),
            Road("North", Direction.NORTH),
            Road("South", Direction.SOUTH)
        ]
        self.current_road_index = 0
        self.running = True
        self.car_counter = 1
        self.last_car_spawn = 0
        self.emergency_mode = False
        self.emergency_road_index = -1
        self.emergency_vehicle = None

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Traffic Intersection Simulation")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

    def change_traffic_lights(self):
        while self.running:
            if self.emergency_mode:
                time.sleep(0.1)  # Check more frequently during emergency
                continue
            
            # Set all lights to red first
            for road in self.roads:
                road.traffic_light.change_color("Red")
            
            time.sleep(1)  # Brief all-red period
            
            # Only proceed if not in emergency mode (double check)
            if not self.emergency_mode:
                # Then turn current road green
                current_road = self.roads[self.current_road_index]
                current_road.traffic_light.change_color("Green")
                
                # Wait for green light duration
                green_start = time.time()
                while time.time() - green_start < 5 and not self.emergency_mode:
                    time.sleep(0.1)
                
                # Back to red and move to next road (only if not in emergency)
                if not self.emergency_mode:
                    current_road.traffic_light.change_color("Red")
                    self.current_road_index = (self.current_road_index + 1) % len(self.roads)
            
            time.sleep(1)

    def spawn_cars(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_car_spawn > 3000:
            direction = random.choice(list(Direction))
            car = Car(f"Car{self.car_counter}", direction)
            road_index = direction.value
            self.roads[road_index].add_car(car)
            self.car_counter += 1
            self.last_car_spawn = current_time

    def spawn_emergency_vehicle(self):
        if self.emergency_mode:
            return
        direction = random.choice(list(Direction))
        self.emergency_vehicle = EmergencyVehicle("Ambulance", direction)
        road_index = direction.value
        self.roads[road_index].add_car(self.emergency_vehicle)

    def check_emergency_exit(self):
        if self.emergency_mode and self.emergency_vehicle:
            # Check if emergency vehicle has left the scene
            if (self.emergency_vehicle.x < -100 or self.emergency_vehicle.x > WINDOW_WIDTH + 100 or 
                self.emergency_vehicle.y < -100 or self.emergency_vehicle.y > WINDOW_HEIGHT + 100):
                
                # Reset emergency mode
                self.emergency_mode = False
                self.emergency_road_index = -1
                self.emergency_vehicle = None
                
                pygame.display.set_caption("Traffic Intersection Simulation")
                
                # Don't interfere with traffic lights here - let the normal thread handle it

    def draw_intersection(self):
        road_width = 60
        pygame.draw.rect(self.screen, DARK_GRAY, (WINDOW_WIDTH // 2 - road_width, 0, road_width * 2, WINDOW_HEIGHT))
        pygame.draw.rect(self.screen, DARK_GRAY, (0, WINDOW_HEIGHT // 2 - road_width, WINDOW_WIDTH, road_width * 2))
        for y in range(0, WINDOW_HEIGHT, 20):
            pygame.draw.rect(self.screen, WHITE, (WINDOW_WIDTH // 2 - 2, y, 4, 10))
        for x in range(0, WINDOW_WIDTH, 20):
            pygame.draw.rect(self.screen, WHITE, (x, WINDOW_HEIGHT // 2 - 2, 10, 4))

    def draw_traffic_lights(self):
        light_size = 20
        positions = [
            (WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2 - 80),
            (WINDOW_WIDTH // 2 + 80, WINDOW_HEIGHT // 2 + 80),
            (WINDOW_WIDTH // 2 + 80, WINDOW_HEIGHT // 2 - 80),
            (WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2 + 80),
        ]
        for i, (road, pos) in enumerate(zip(self.roads, positions)):
            pygame.draw.rect(self.screen, BLACK, (pos[0] - light_size // 2, pos[1] - light_size // 2, light_size, light_size))
            color = GREEN if road.traffic_light.get_color() == "Green" else RED
            pygame.draw.circle(self.screen, color, pos, light_size // 2 - 2)
            text = self.small_font.render(road.name, True, BLACK)
            text_rect = text.get_rect(center=(pos[0], pos[1] - 40))
            self.screen.blit(text, text_rect)

    def draw_info(self):
        if self.emergency_mode:
            info_text = f"🚨 EMERGENCY MODE - {self.roads[self.emergency_road_index].name} Road"
        else:
            current_road = self.roads[self.current_road_index]
            info_text = f"Active: {current_road.name} Road"
        
        text = self.font.render(info_text, True, BLACK)
        self.screen.blit(text, (10, 10))
        
        total_cars = sum(len(road.cars) for road in self.roads)
        car_text = f"Total Cars: {total_cars}"
        text = self.small_font.render(car_text, True, BLACK)
        self.screen.blit(text, (10, 50))
        
        text = self.small_font.render("Press E for emergency", True, BLACK)
        self.screen.blit(text, (10, 80))

    def start_simulation(self):
        light_thread = threading.Thread(target=self.change_traffic_lights)
        light_thread.daemon = True
        light_thread.start()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_SPACE:
                        direction = random.choice(list(Direction))
                        car = Car(f"Car{self.car_counter}", direction)
                        self.roads[direction.value].add_car(car)
                        self.car_counter += 1
                    elif event.key == pygame.K_e:
                        self.spawn_emergency_vehicle()

            self.spawn_cars()
            self.check_emergency_exit()

            for road in self.roads:
                road.update_cars(self)

            self.screen.fill(WHITE)
            self.draw_intersection()
            self.draw_traffic_lights()
            for road in self.roads:
                for car in road.cars:
                    car.draw(self.screen)
            self.draw_info()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

if __name__ == "__main__":
    simulation = TrafficSimulation()
    simulation.start_simulation()