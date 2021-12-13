from hw_interface import *
from ultrasonic import Ultrasonic
import numpy as np
import random
import time


class Navigate():
    def __init__(self):
        self.ultrasonics = Ultrasonic()
        self.motors = MotorDriver()

    def get_veer_ratio(self):
        sorted_ind = np.argsort(self.ultrasonics.distances)
        min_ind = sorted_ind[0]
        max_ind = sorted_ind[2]
        if max_ind < min_ind:
            print("Veering left")
            self.motors.drive(Action.VEER, Speed.VEER_SLOW, Speed.VEER_FAST)
        else:
            print("Veering right")
            self.motors.drive(Action.VEER, Speed.VEER_FAST, Speed.VEER_SLOW)

    def run(self):
        try:
            while True:
                self.ultrasonics.update_ultrasonic()
                print(self.ultrasonics.distances)
                min_val = min(self.ultrasonics.distances)
                min_index = np.argmin(self.ultrasonics.distances)
                if min_val < .30:
                    if min_index == 0:
                        self.motors.drive(Action.ROTATE_CW, Speed.FAST)
                    elif min_index == 1:
                        random_turn = random.choice(
                            # [Action.ROTATE_CW, Action.ROTATE_CCW])
                            [Action.ROTATE_CW])
                        self.motors.drive(random_turn, Speed.FAST)
                    elif min_index == 2:
                        self.motors.drive(Action.ROTATE_CCW, Speed.FAST)
                elif min_val < .60:
                    self.motors.drive(Action.VEER, Speed.SLOW,
                                      self.get_veer_ratio())
                elif min_val < 1.00:
                    self.motors.drive(Action.VEER, Speed.MEDIUM,
                                      self.get_veer_ratio())
                else:
                    self.motors.drive(Action.VEER, Speed.MEDIUM)
                time.sleep(0.1)

        except KeyboardInterrupt:
            self.motors.cleanup()


if __name__ == "__main__":
    nav = Navigate()
    nav.run()
