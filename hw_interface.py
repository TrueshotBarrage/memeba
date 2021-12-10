# David Kim (jk2537)
# Zoltan Csaki (zcc6)
import time
from enum import Enum, auto

import RPi.GPIO as GPIO
import pigpio

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
    FORWARD = auto()
    BACKWARD = auto()
    ROTATE_CW = auto()
    ROTATE_CCW = auto()
    STOP = auto()


class HardwarePWM():
    def __init__(self, pin, freq=20000, dc=100.0):
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

    def drive(self, action, speed=60):
        """Drive the robot with the specified action at the specified speed.

        Args:
            action (enum): Enumerated action to represent robot behavior
            speed (float): The speed of the robot's movement
        """
        if action == Action.FORWARD:
            self._set_motor(Motor.LEFT, Rot.CCW, speed)
            self._set_motor(Motor.RIGHT, Rot.CW, speed)

        elif action == Action.BACKWARD:
            self._set_motor(Motor.LEFT, Rot.CW, speed)
            self._set_motor(Motor.RIGHT, Rot.CCW, speed)

        elif action == Action.ROTATE_CW:
            self._set_motor(Motor.LEFT, Rot.CW, speed)
            self._set_motor(Motor.RIGHT, Rot.CW, speed)

        elif action == Action.ROTATE_CCW:
            self._set_motor(Motor.LEFT, Rot.CCW, speed)
            self._set_motor(Motor.RIGHT, Rot.CCW, speed)

        elif action == Action.STOP:
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
        print("Driving backward")
        md.drive(Action.BACKWARD, speed=50.0)
        time.sleep(5.0)

        print("Driving forward")
        md.drive(Action.FORWARD, speed=50.0)
        time.sleep(5.0)

        print("Stopping")
        md.drive(Action.STOP)

        print("Cleaning up")
        md.cleanup()

    except KeyboardInterrupt:
        md.cleanup()
