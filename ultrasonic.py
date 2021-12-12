import time
from gpiozero import DistanceSensor
import RPi.GPIO as GPIO


class Ultrasonic:
    def __init__(self):
        self.distances = [None, None, None]
        self.left_ultra = DistanceSensor(echo=6, trigger=27, max_distance=4)
        self.mid_ultra = DistanceSensor(echo=19, trigger=17, max_distance=4)
        self.right_ultra = DistanceSensor(echo=5, trigger=4, max_distance=4)

    def update_ultrasonic(self):
        self.distances = [
            self.left_ultra.distance, self.mid_ultra.distance,
            self.right_ultra.distance
        ]


if __name__ == '__main__':
    try:
        ultras = Ultrasonic()
        while True:
            ultras.update_ultrasonic()
            print(ultras.distances)
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
