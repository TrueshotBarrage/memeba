import time
import RPi.GPIO as GPIO

import hw_interface as hw


def main():
    md = hw.MotorDriver()
    try:
        md.drive(hw.Action.ROTATE_CCW)
        time.sleep(5)
        md.drive(hw.Action.STOP)
        md.cleanup()
    except KeyboardInterrupt:
        md.cleanup()


if __name__ == "__main__":
    main()
