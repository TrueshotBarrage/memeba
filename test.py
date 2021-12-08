import time
import RPi.GPIO as GPIO

from rpi_hardware_pwm import HardwarePWM
import motor_driving


def main():
    try:
        # md = motor_driving.MotorDriving()
        # time.sleep(10.0)
        # GPIO.cleanup()

        pwm = HardwarePWM(0, hz=6000)
        pwm2 = HardwarePWM(1, hz=6000)
        md = motor_driving.MotorDriving()
        pwm.start(100)  # full duty cycle
        pwm2.start(100)
        md.drive(md.FORWARD)
        time.sleep(5.0)

        md.drive(md.BACKWARD)
        time.sleep(5.0)

        pwm.stop()
        pwm2.stop()
        GPIO.cleanup()

    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
