import time
import RPi.GPIO as GPIO

from rpi_hardware_pwm import HardwarePWM
import hw_interface as hw


def main():
    md = hw.MotorDriver()
    try:
        pass
    except KeyboardInterrupt:
        md.cleanup()


if __name__ == "__main__":
    main()
