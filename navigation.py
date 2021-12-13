from hw_interface import *
from ultrasonic import Ultrasonic
import numpy as np
import random


class Navigate():
    def __init__(self):
        self.ultrasonics = Ultrasonic()
        self.motors = MotorDriver()

    def get_veer_ratio(self):
        min_val_1 = min(self.ultrasonics.distances)
        min_index_1 = np.argmin(self.ultrasonics.distances)
        min_val_2 = sorted(self.ultrasonics.distances)[1]
        min_index_2 = np.argsort(self.ultrasonics.distances)[1]
        if min_index_1 < min_index_2:
            return (min_val_1 / min_val_2)
        else:
            return (min_val_2 / min_val_1)

    def run(self):
        try:
            while True:
                min_val = min(self.ultrasonics.distances)
                min_index = np.argmin(self.ultrasonics.distances)
                if min_val < 30:
                    if min_index == 0:
                        self.motors.drive(Action.ROTATE_CW, Speed.SLOW)
                    if min_index == 1:
                        random_turn = random.choice(
                            [Action.ROTATE_CW, Action.ROTATE_CCW])
                        self.motors.drive(random_turn, Speed.SLOW)
                    if min_index == 2:
                        self.motors.drive(Action.ROTATE_CCW, Speed.SLOW)
                    self.motors.drive(Action.ROTATE_CCW, Speed.SLOW)
                elif min_val < 60:
                    self.motors.drive(Action.VEER, Speed.SLOW,
                                      self.get_veer_ratio())
                elif min_val < 100:
                    self.motors.drive(Action.VEER, Speed.MEDIUM,
                                      self.get_veer_ratio())
                else:
                    self.motors.drive(Action.VEER, Speed.MEDIUM)
        except KeyboardInterrupt:
            self.motors.cleanup()


if __name__ == "__main__":
    nav = Navigate()
    nav.run()
