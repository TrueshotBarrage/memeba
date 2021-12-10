import time
import RPi.GPIO as GPIO

import hw_interface as hw


def main():
    md = hw.MotorDriver()
    try:
        md.drive(hw.Action.FORWARD)
    except KeyboardInterrupt:
        md.cleanup()


if __name__ == "__main__":
    main()
