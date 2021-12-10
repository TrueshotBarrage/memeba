from gpiozero import DistanceSensor
import RPi.GPIO as GPIO


class Ultrasonic:
    def __init__(self):

        self.distances = [None, None, None]
        self.left_ultra = DistanceSensor(echo=27, trigger=6, max_distance=4)

    def read_ultrasonic(self):
        print(self.left_ultra.distance)

    def poll_ultrasonics(self):
        pass


if __name__ == '__main__':
    try:
        ultras = Ultrasonic()
        for i in range(10):
            ultras.read_ultrasonic()
    except KeyboardInterrupt:
        GPIO.cleanup()
