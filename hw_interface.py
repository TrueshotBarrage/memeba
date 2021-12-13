# David Kim (jk2537)
# Zoltan Csaki (zcc6)
import time
from enum import Enum, auto

import RPi.GPIO as GPIO
import pigpio
from gpiozero import DistanceSensor

# Enumerated constants for ease of access


# Left/right motor definitions
class Motor(int, Enum):
    LEFT = 0
    RIGHT = 1


# GPIO pin references
class Pin(str, Enum):
    CW = "clockwise"
    CCW = "counterclockwise"


# Directions
class Rot(int, Enum):
    CW = 1
    CCW = 0


# Actions
class Action(Enum):
    DRIVE_FORWARD = auto()
    DRIVE_BACKWARD = auto()
    ROTATE_LEFT = auto()
    ROTATE_RIGHT = auto()
    VEER_LEFT = auto()
    VEER_RIGHT = auto()
    STOP = auto()


class Speed(int, Enum):
    VEER_DIFF = 5
    SLOW = 60
    MEDIUM = 65
    FAST = 80
    FLASH = 100


class HardwarePWM():
    def __init__(self, pin, freq=20000, dc=50):
        """Set up the PWM instance in the hardware for the motor controls.

        Args:
            pin (int/list): GPIO pin number(s) to set up as PWM instance(s)
            freq (float): Initial frequency of the PWM instance
            dc (float): Initial duty cycle 
        
        Fields:
            pi (pigpio): PiGPIO base class object
            pins (list): List of PWM GPIO pins
        """
        assert 0.0 <= dc <= 100, f"Duty cycle ({dc}) must be between 0 and 100"

        # Start the pigpio instance
        self.pi = pigpio.pi()

        # Ensure pins are correctly wrapped inside a list
        if isinstance(pin, int):
            pin = [pin]
        assert isinstance(pin, list)

        # Assign parameters as fields
        self.pins = pin
        self.freq = freq
        self.dc = dc

    def start(self, dc=None):
        """Start the PWM instances.
        
        Args:
            dc (float): Duty cycle (%) between [0 and 100]
        """
        if dc is not None:
            self.dc = dc

        for p in self.pins:
            self.pi.hardware_PWM(p, int(self.freq), int(self.dc) * 10000)

    def change_dc(self, new_dc):
        """Change the duty cycle of the PWM instance.

        Args:
            new_dc (float): Duty cycle (%) between [0 and 100]
        """
        assert 0.0 <= new_dc <= 100.0, \
            f"Duty cycle ({new_dc}) must be between 0 and 100"
        self.dc = new_dc
        self.start()

    def change_freq(self, new_freq):
        """Change the frequency of the PWM instance.
        
        Args:
            new_freq (float): Frequency (Hz)
        """
        self.freq = new_freq
        self.start()

    def cleanup(self):
        """Clean up the PWM instance."""
        self.pi.stop()


class Ultrasonic:
    def __init__(self):
        self.distances = [None, None, None]
        self.left_ultra = DistanceSensor(echo=6, trigger=27, max_distance=4)
        self.mid_ultra = DistanceSensor(echo=19, trigger=17, max_distance=4)
        self.right_ultra = DistanceSensor(echo=5, trigger=4, max_distance=4)
        self.L = 0
        self.M = 1
        self.R = 2

    def update_ultrasonic(self):
        self.distances = [
            self.left_ultra.distance, self.mid_ultra.distance,
            self.right_ultra.distance
        ]


class MotorDriver():
    def __init__(self):
        """Class to control and drive the motors of the robot. 
        On initialization, set up the PWM instance for the motor driver module.

        Parameters:
            none for now
        """
        # These are our configurations for the motor driver <-> GPIO pins
        self.motor_pins = [
            {
                Pin.CW: 16,  # AI2
                Pin.CCW: 20  # AI1
            },
            {
                Pin.CW: 18,  # BI2
                Pin.CCW: 24  # BI1
            }
        ]

        # These are our hardware PWM instances and GPIO pin numbers
        self.pwm = [HardwarePWM(12), HardwarePWM(13)]

        # Set up GPIO pins for each motor driver connection
        GPIO.setmode(GPIO.BCM)
        for output_pins in self.motor_pins:
            for pin in output_pins.values():
                GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

    def _set_motor(self, motor_id, direction, dc):
        """Set a specified motor to a direction and duty cycle.

        Args:
            motor_id (enum): Enumerated motor identifier -> Left/Right
            direction (enum): Enumerated direction of rotation -> CW/CCW
            dc (float): The duty cycle for the PWM instance of the motor
        """
        rot_cw = direction == Rot.CW
        GPIO.output(self.motor_pins[motor_id][Pin.CW], rot_cw)
        GPIO.output(self.motor_pins[motor_id][Pin.CCW], not rot_cw)
        self.pwm[motor_id].start(dc)

    def drive(self, action, speed=50):
        """Drive the robot with the specified action at the specified speed.

        Args:
            action (enum): Enumerated action to represent robot behavior
            speed (float): The speed of the robot's movement
        """
        if action == Action.DRIVE_FORWARD:
            print(f"Driving forward at {speed}%")
            self._set_motor(Motor.LEFT, Rot.CCW, speed)
            self._set_motor(Motor.RIGHT, Rot.CW, speed)

        elif action == Action.DRIVE_BACKWARD:
            print(f"Driving backward at {speed}%")
            self._set_motor(Motor.LEFT, Rot.CW, speed)
            self._set_motor(Motor.RIGHT, Rot.CCW, speed)

        elif action == Action.ROTATE_LEFT:
            print(f"Rotating left at {speed}%")
            self._set_motor(Motor.LEFT, Rot.CW, speed)
            self._set_motor(Motor.RIGHT, Rot.CW, speed)

        elif action == Action.ROTATE_RIGHT:
            print(f"Rotating right at {speed}%")
            self._set_motor(Motor.LEFT, Rot.CCW, speed)
            self._set_motor(Motor.RIGHT, Rot.CCW, speed)

        elif action == Action.VEER_LEFT:
            print(f"Veering left at ({speed} +/- {Speed.VEER_DIFF})%")
            self._set_motor(Motor.LEFT, Rot.CCW, speed - Speed.VEER_DIFF)
            self._set_motor(Motor.RIGHT, Rot.CW, speed + Speed.VEER_DIFF)

        elif action == Action.VEER_RIGHT:
            print(f"Veering right at ({speed} +/- {Speed.VEER_DIFF})%")
            self._set_motor(Motor.LEFT, Rot.CCW, speed + Speed.VEER_DIFF)
            self._set_motor(Motor.RIGHT, Rot.CW, speed - Speed.VEER_DIFF)

        elif action == Action.STOP:
            print(f"Stopping")
            self._set_motor(Motor.LEFT, Rot.CCW, 0)
            self._set_motor(Motor.RIGHT, Rot.CCW, 0)

    def cleanup(self):
        """Clean up GPIO & PWM instances."""
        GPIO.cleanup()
        for pwm_instance in self.pwm:
            pwm_instance.cleanup()


if __name__ == '__main__':
    md = MotorDriver()
    try:
        # Driving forward
        md.drive(Action.DRIVE_FORWARD, Speed.MEDIUM)
        time.sleep(2.0)

        # Driving backward
        md.drive(Action.DRIVE_BACKWARD, Speed.MEDIUM)
        time.sleep(2.0)

        # Veering left
        md.drive(Action.VEER, Speed.VEER_SLOW, Speed.VEER_FAST)
        time.sleep(2.0)

        # Veering right
        md.drive(Action.VEER, Speed.VEER_FAST, Speed.VEER_SLOW)
        time.sleep(2.0)

        # Rotating left
        md.drive(Action.ROTATE_LEFT, Speed.FAST)
        time.sleep(1.0)

        # Rotating right
        md.drive(Action.ROTATE_RIGHT, Speed.FAST)
        time.sleep(1.0)

        # Stopping
        md.drive(Action.STOP)

        # Cleaning up
        md.cleanup()

    except KeyboardInterrupt:
        md.cleanup()
