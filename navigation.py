from hw_interface import *
from ultrasonic import Ultrasonic
import numpy as np
import time


class Navigate():
    def __init__(self):
        self.ultrasonics = Ultrasonic()
        self.motors = MotorDriver()

    def veer(self):
        sorted_ind = np.argsort(self.ultrasonics.distances)
        min_ind = sorted_ind[0]
        max_ind = sorted_ind[2]

        # If there is more open space on the left, veer left
        if max_ind < min_ind:
            self.motors.drive(Action.VEER_LEFT, Speed.MEDIUM)
        # If there is more open space on the right, veer right
        else:
            self.motors.drive(Action.VEER_RIGHT, Speed.MEDIUM)

    def run(self):
        try:
            while True:
                # Update the ultrasonic sensor readings
                self.ultrasonics.update_ultrasonic()
                print(self.ultrasonics.distances)

                min_index = np.argmin(self.ultrasonics.distances)
                min_val = self.ultrasonics.distances[min_index]
                
                # If the robot is very close to obstacles on all fronts, go backwards
                if all(dist < .30 for dist in self.ultrasonics.distances):
                    self.motors.drive(Action.DRIVE_BACKWARD, Speed.SLOW)
                    
                # If the robot is close to obstacle on one side rotate away from it
                elif min_val < .30:
                    if min_index == 0:
                        self.motors.drive(Action.ROTATE_RIGHT, Speed.FAST)
                    elif min_index == 1:
                        self.motors.drive(Action.ROTATE_LEFT, Speed.FAST)
                    elif min_index == 2:
                        self.motors.drive(Action.ROTATE_LEFT, Speed.FAST)
                        
                # If the robot senses an obstacle on one side, veer away from it
                elif min_val < 1.00:
                    self.veer()
                    
                # If there are no obstacles near the robot, go forward
                else:
                    self.motors.drive(Action.DRIVE_FORWARD, Speed.MEDIUM)
                    
                time.sleep(0.1)

        except KeyboardInterrupt:
            self.motors.cleanup()


if __name__ == "__main__":
    nav = Navigate()
    nav.run()
