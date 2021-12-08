import time
import RPi.GPIO as GPIO
import pigpio

import motor_driving


def main():
    try:
        # md = motor_driving.MotorDriving()
        # time.sleep(10.0)
        # GPIO.cleanup()

        dc = 200000  # 20% duty cycle
        pwm_pin = 12

        PI = pigpio.pi()
        PI.set_mode(pwm_pin, pigpio.OUTPUT)
        PI.hardware_PWM(pwm_pin, 400, dc)
        PI.write(pwm_pin, 1)
        time.sleep(5.0)

        PI.stop()

    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == "__main__":
    main()