# David Kim (jk2537)
# Zoltan Csaki (zcc6)

import RPi.GPIO as GPIO
import pigpio
import time


class HardwarePWM():
    def __init__(self):
        self.pi = pigpio.pi()

    def run(self, pin):
        # for i in range(10000):
        #     print("Hello" + str(i))
        #     self.pi.hardware_PWM(pin, 20000, 500000)
        #     time.sleep(0.0001)
        # self.pi.stop()
        self.pi.hardware_PWM(pin, 20000, 500000)


class MotorDriving():
    def __init__(self):
        """Set up GPIO pins and the PWM instance.

        Parameters:
            none for now
        """
        # Enumerated constants for ease of access

        # Left/right motor definitions
        self.L_M = 0
        self.R_M = 1

        # GPIO pin references
        self.PIN_CW = "clockwise"
        self.PIN_CCW = "counterclockwise"

        # Directions
        self.DIR_CW = GPIO.HIGH
        self.DIR_CCW = GPIO.LOW

        # Actions
        self.FORWARD = 1
        self.BACKWARD = 2
        self.ROTATE_CW = 3
        self.ROTATE_CCW = 4
        self.STOP = 5

        # These are our configurations for the motor driver <-> GPIO pins
        # TODO: Set up the PWM pins differently
        self.motor_pins = [
            {
                # "pwm_pin": 12,
                "clockwise": 16,  # AI2
                "counterclockwise": 20  # AI1
            },
            {
                # "pwm_pin": 13,
                "clockwise": 18,  # BI2
                "counterclockwise": 24  # BI1
            }
        ]

        # self.pwm_pins = [{"pwm_pin": 12}, {"pwm_pin": 13}]

        # Set up GPIO pins for each motor driver connection
        GPIO.setmode(GPIO.BCM)
        for output_pins in self.motor_pins:
            for pin in output_pins.values():
                GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

        # Set up PWM instances for each motor
        # self.motor_pins[self.L_M]["pwm"] = GPIO.PWM(
        #     self.motor_pins[self.L_M]["pwm_pin"], 50)
        # self.motor_pins[self.R_M]["pwm"] = GPIO.PWM(
        #     self.motor_pins[self.R_M]["pwm_pin"], 50)
        # for pin in self.pwm_pins:
        #     pi = pigpio.pi()
        #     pi.hardware_PWM(pin, 20000, 500000)

    def _dc_to_speed(dc):
        raise NotImplementedError()

    def _set_motor(self, motor_id, direction, dc):
        """Set a specified motor to a direction and duty cycle.

        Args:
            motor_id (int): The numerical identifier for the motor
            direction (bool): True/False for clockwise/counterclockwise
            dc (float): The duty cycle for the PWM instance of the motor
        """
        GPIO.output(self.motor_pins[motor_id][self.PIN_CW], direction)
        GPIO.output(self.motor_pins[motor_id][self.PIN_CCW], not direction)
        # self.motor_pins[motor_id]["pwm"].start(dc)

    def drive(self, action, speed=60.0):
        """Drive the robot with the specified action at the specified speed.

        Args:
            action (int): Enumerated ints to represent certain actions
            speed (float): The speed of the robot's movement
        """
        if action == self.FORWARD:
            self._set_motor(self.L_M, self.DIR_CCW, speed)
            self._set_motor(self.R_M, self.DIR_CW, speed)

        elif action == self.BACKWARD:
            self._set_motor(self.L_M, self.DIR_CW, speed)
            self._set_motor(self.R_M, self.DIR_CCW, speed)

        elif action == self.ROTATE_CW:
            self._set_motor(self.L_M, self.DIR_CW, speed)
            self._set_motor(self.R_M, self.DIR_CW, speed)

        elif action == self.ROTATE_CCW:
            self._set_motor(self.L_M, self.DIR_CCW, speed)
            self._set_motor(self.R_M, self.DIR_CCW, speed)

        elif action == self.STOP:
            self._set_motor(self.L_M, self.DIR_CCW, 0.0)
            self._set_motor(self.R_M, self.DIR_CCW, 0.0)


if __name__ == '__main__':
    try:
        md = MotorDriving()
        pwm = HardwarePWM()
        print("Running 12")
        pwm.run(12)
        print("Running 13")
        pwm.run(13)
        print("Driving backward")
        md.drive(md.BACKWARD, speed=50.0)
        time.sleep(5.0)

        print("Driving forward")
        md.drive(md.FORWARD, speed=50.0)
        time.sleep(5.0)
        md.drive(md.STOP)
        GPIO.cleanup()

    except KeyboardInterrupt:
        GPIO.cleanup()
