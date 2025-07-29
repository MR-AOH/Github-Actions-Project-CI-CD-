import threading

class TrafficLight:
    def __init__(self):
        self.color = "Red"
        self.lock = threading.Lock()

    def change_color(self, color):
        with self.lock:
            self.color = color

    def get_color(self):
        with self.lock:
            return self.color