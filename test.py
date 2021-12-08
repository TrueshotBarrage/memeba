import time
import RPi.GPIO as GPIO

import motor_driving


def main():
    try:
        md = motor_driving.MotorDriving()
        time.sleep(10.0)
        GPIO.cleanup()

    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == "__main__":
    main()