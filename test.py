import time
import RPi.GPIO as GPIO

from rpi_hardware_pwm import HardwarePWM
import motor_driving


def main():
    try:
        # md = motor_driving.MotorDriving()
        # time.sleep(10.0)
        # GPIO.cleanup()

        pwm = HardwarePWM(0, hz=1000)
        pwm.start(100) # full duty cycle
        time.sleep(5.0)
        pwm.change_duty_cycle(100)
        time.sleep(5.0)
        pwm.stop()

    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == "__main__":
    main()