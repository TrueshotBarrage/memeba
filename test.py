import time
import RPi.GPIO as GPIO
import pigpio

import motor_driving


def main():
    try:
        # md = motor_driving.MotorDriving()
        # time.sleep(10.0)
        # GPIO.cleanup()

        dc = 500000  # 50% duty cycle
        pwm_pin = 12

        PI = pigpio.pi()
        PI.hardware_PWM(pwm_pin, 20000, dc)

        time.sleep(5.0)

        PI.stop()

    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == "__main__":
    main()