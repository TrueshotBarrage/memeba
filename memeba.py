import threading
import time
from enum import Enum, auto

from navigation import Navigate
from object_detection import ObjectDetection
from meme_generator import MemeGenerator


# States
class State(Enum):
    Meme = auto()
    Nav = auto()


class Memeba():
    def __init__(self):
        self.nav = Navigate()
        self.meme_generator = MemeGenerator()
        self.state = State.Nav

        self.meme_time = self.nav_time = time.time()
        self.MIN_NAV_TIME = 5
        self.MIN_MEME_TIME = 5
        self.MAX_MEME_TIME = 10

        self.object_detection = ObjectDetection()
        self.object_detection_thread = threading.Thread(
            target=self.object_object_detection.stream, args=())
        self.object_detection_thread.start()

    def run(self, freq):
        while True:
            try:
                # Guarantee nav has run at least MIN_NAV_TIME before changing states
                if self.state == State.Nav \
                    and time.time() - self.nav_time < self.MIN_NAV_TIME:
                    self.nav.run()

                # If we have been showing the meme for at least 10 seconds, run nav
                elif self.state == State.Meme \
                    and time.time() - self.meme_time > self.MAX_MEME_TIME:
                    self.nav_time = time.time()
                    self.state = State.Nav
                    self.nav.run()

                else:
                    person_detected = self.object_detection.person_in_frame

                    # If person detected and nav running, switch to meme mode
                    if person_detected and self.state == State.Nav:
                        self.meme_generator.show_meme(self.MIN_MEME_TIME)
                        self.state = State.Meme
                        self.meme_time = time.time()

                    # If no person detected and meme running, switch to nav mode
                    elif not person_detected and self.state == State.Meme:
                        self.state = State.Nav
                        self.nav_time = time.time()
                        self.nav.run()

                    elif self.state == State.Nav:
                        self.nav.run()

                time.sleep(freq)

            finally:
                self.cleanup()

    def cleanup(self):
        self.object_detection_thread.running = False
        self.nav.motors.cleanup()

        # Wait until object detection thread is completely executed
        self.object_detection_thread.join()
        print("Object detection thread successfully killed")


if __name__ == "__main__":
    memeba = Memeba()
    memeba.run(0.1)