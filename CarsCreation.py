from TrafficLight import TrafficLight
from utils import Direction, WINDOW_WIDTH, WINDOW_HEIGHT, WHITE, BLACK, RED, GREEN, YELLOW, BLUE, GRAY, DARK_GRAY, LIGHT_GRAY
from RoadsCreation import Road
import random
import pygame





class Car:
    def __init__(self, name, direction, color=None):
        self.name = name
        self.direction = direction
        self.color = color or (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.speed = 2
        self.waiting = False

        if direction == Direction.NORTH:
            self.x = WINDOW_WIDTH // 2 - 15
            self.y = WINDOW_HEIGHT - 50
        elif direction == Direction.SOUTH:
            self.x = WINDOW_WIDTH // 2 + 15
            self.y = -50
        elif direction == Direction.EAST:
            self.x = -50
            self.y = WINDOW_HEIGHT // 2 - 15
        elif direction == Direction.WEST:
            self.x = WINDOW_WIDTH + 50
            self.y = WINDOW_HEIGHT // 2 + 15

    def update(self, traffic_light_color, front_car=None):
        intersection_zone = (
            WINDOW_WIDTH // 2 - 60 < self.x < WINDOW_WIDTH // 2 + 60 and
            WINDOW_HEIGHT // 2 - 60 < self.y < WINDOW_HEIGHT // 2 + 60
        )

        should_stop = False
        stop_distance = 70
        if traffic_light_color != "Green":
            if self.direction == Direction.NORTH and self.y > WINDOW_HEIGHT // 2 and self.y < WINDOW_HEIGHT // 2 + stop_distance:
                should_stop = True
            elif self.direction == Direction.SOUTH and self.y < WINDOW_HEIGHT // 2 and self.y > WINDOW_HEIGHT // 2 - stop_distance:
                should_stop = True
            elif self.direction == Direction.EAST and self.x < WINDOW_WIDTH // 2 and self.x > WINDOW_WIDTH // 2 - stop_distance:
                should_stop = True
            elif self.direction == Direction.WEST and self.x > WINDOW_WIDTH // 2 and self.x < WINDOW_WIDTH // 2 + stop_distance:
                should_stop = True

        if front_car:
            buffer_distance = 30
            if self.direction in [Direction.NORTH, Direction.SOUTH]:
                dy = abs(self.y - front_car.y)
                if dy < buffer_distance and (
                    (self.direction == Direction.NORTH and self.y > front_car.y) or
                    (self.direction == Direction.SOUTH and self.y < front_car.y)
                ):
                    self.waiting = True
                    return False
            elif self.direction in [Direction.EAST, Direction.WEST]:
                dx = abs(self.x - front_car.x)
                if dx < buffer_distance and (
                    (self.direction == Direction.EAST and self.x < front_car.x) or
                    (self.direction == Direction.WEST and self.x > front_car.x)
                ):
                    self.waiting = True
                    return False

        if should_stop and not intersection_zone:
            self.waiting = True
            return False

        self.waiting = False

        if self.direction == Direction.NORTH:
            self.y -= self.speed
        elif self.direction == Direction.SOUTH:
            self.y += self.speed
        elif self.direction == Direction.EAST:
            self.x += self.speed
        elif self.direction == Direction.WEST:
            self.x -= self.speed

        if (self.x < -100 or self.x > WINDOW_WIDTH + 100 or 
            self.y < -100 or self.y > WINDOW_HEIGHT + 100):
            return True

        return False

    def draw(self, screen):
        car_width = 25
        car_height = 15
        if self.direction in [Direction.NORTH, Direction.SOUTH]:
            car_width, car_height = car_height, car_width

        car_rect = pygame.Rect(self.x - car_width // 2, self.y - car_height // 2, car_width, car_height)
        pygame.draw.rect(screen, self.color, car_rect)
        pygame.draw.rect(screen, BLACK, car_rect, 2)

        font = pygame.font.Font(None, 16)
        text = font.render(self.name, True, BLACK)
        text_rect = text.get_rect(center=(self.x, self.y - 30))
        screen.blit(text, text_rect)

        if self.waiting:
            pygame.draw.circle(screen, RED, (int(self.x), int(self.y - 40)), 8)
            pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y - 40)), 8, 2)


class EmergencyVehicle(Car):
    def __init__(self, name, direction):
        super().__init__(name, direction, color=(255, 255, 0))
        self.is_emergency = True