from hw_interface import *
import numpy as np
import time


class Navigate():
    def __init__(self):
        self.ultrasonics = Ultrasonic()
        self.motors = MotorDriver()
        self.last_action = Action.STOP

    def drive(self, action, speed):
        self.last_action = action
        self.motors.drive(action, speed)

    def veer(self):
        sorted_ind = np.argsort(self.ultrasonics.distances)
        min_ind = sorted_ind[0]
        max_ind = sorted_ind[2]

        # If there is more open space on the left, veer left
        if max_ind < min_ind:
            self.drive(Action.VEER_LEFT, Speed.MEDIUM)
        # If there is more open space on the right, veer right
        else:
            self.drive(Action.VEER_RIGHT, Speed.MEDIUM)

    def run(self):
        try:
            # Update the ultrasonic sensor readings
            self.ultrasonics.update_ultrasonic()
            print(self.ultrasonics.distances)

            min_index = np.argmin(self.ultrasonics.distances)
            min_val = self.ultrasonics.distances[min_index]

            # If the robot is very close to obstacles on all fronts, go backwards
            if any(dist < .15 for dist in self.ultrasonics.distances) or \
                all(dist < .30 for dist in self.ultrasonics.distances):
                self.drive(Action.DRIVE_BACKWARD, Speed.SLOW)

            # If the robot is close to obstacle on one side rotate away from it
            elif min_val < .30:
                if min_index == self.ultrasonics.L:
                    desired_action = Action.ROTATE_RIGHT
                else:
                    desired_action = Action.ROTATE_LEFT

                if self.last_action in [
                        Action.ROTATE_LEFT, Action.ROTATE_RIGHT
                ] and desired_action != self.last_action:
                    desired_action = self.last_action

                self.drive(desired_action, Speed.FAST)

            # If the robot senses an obstacle on one side, veer away from it
            elif min_val < 1.00:
                self.veer()

            # If there are no obstacles near the robot, go forward
            else:
                self.drive(Action.DRIVE_FORWARD, Speed.MEDIUM)

        except KeyboardInterrupt:
            self.motors.cleanup()


if __name__ == "__main__":
    try:
        nav = Navigate()
        while True:
            nav.run()
            time.sleep(0.1)
    except KeyboardInterrupt:
        nav.motors.cleanup()
