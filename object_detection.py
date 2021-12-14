#Import the Open-CV extra functionalities
import os
import time
import threading
import logging

import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera

logger = logging.getLogger()
logging_stream_handler = logging.StreamHandler()
logging_stream_handler.setFormatter(
    logging.Formatter("[%(asctime)s] %(message)s"))
logger.addHandler(logging_stream_handler)
logger.setLevel(logging.INFO)


def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper


class ObjectDetection():
    def __init__(self):
        self.person_in_frame = False

        # Initialize the PiCamera
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 2
        logger.info("Initialized PiCamera")

        # Allow the camera to warmup
        time.sleep(0.1)

        # This is to pull the information about what each object is called
        self.class_names = []
        base_path = "object_detection"
        class_file = os.path.join(base_path, "coco.names")
        with open(class_file, "rt") as f:
            self.class_names = f.read().rstrip("\n").split("\n")

        # This is to pull the information about what each object should look like
        config_path = os.path.join(
            base_path, "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
        weights_path = os.path.join(base_path, "frozen_inference_graph.pb")

        # This is some set up values to get good results
        self.net = cv2.dnn_DetectionModel(weights_path, config_path)
        self.net.setInputSize(320, 320)
        self.net.setInputScale(1.0 / 127.5)
        self.net.setInputMean((127.5, 127.5, 127.5))
        self.net.setInputSwapRB(True)

        self.running = True

    # This is to set up what the drawn box size/colour is and the font/size/colour of the name tag and confidence label
    def get_objects(self, img, thres, nms, draw=False, objects=[]):
        class_ids, confs, bbox = self.net.detect(img,
                                                 confThreshold=thres,
                                                 nmsThreshold=nms)
        logger.info("Net detect worked!")

        if len(objects) == 0:
            objects = self.class_names

        object_info = []
        if len(class_ids) != 0:
            for class_id, confidence, box in zip(class_ids.flatten(),
                                                 confs.flatten(), bbox):
                class_name = self.class_names[class_id - 1]
                if class_name in objects:
                    object_info.append([box, confidence, class_name])
                    if (draw):
                        self.draw(img, class_id, confidence, box)
        logger.info("Did the thingies")

        return img, object_info

    def draw(self, img, class_id, confidence, box):
        cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
        cv2.putText(img, self.class_names[class_id - 1].upper(),
                    (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX, 1,
                    (0, 255, 0), 2)
        cv2.putText(img, str(round(confidence * 100,
                                   2)), (box[0] + 200, box[1] + 30),
                    cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    def person_detected(self, object_info):
        for obj in object_info:
            box, confidence, class_name = obj
            x0, y0, width, height = box
            area = width * height
            area_proportion = area / (640 * 480)
            if area_proportion > 0.3 and confidence > 0.5:
                return True

        return False

    def cleanup(self):
        self.camera.close()

    @threaded
    def stream(self):
        logger.info("Trying to start stream!")
        raw_capture = PiRGBArray(self.camera, size=self.camera.resolution)
        for frame in self.camera.capture_continuous(raw_capture,
                                                    format="bgr",
                                                    use_video_port=True):
            try:
                logger.info("Started stream successfully")

                # Grab an image from the frame
                img = frame.array
                logger.info("Got image")

                # 0.45 = threshold number, 0.2 = nms number
                _, object_info = self.get_objects(img,
                                                  0.45,
                                                  0.2,
                                                  objects=["person"])
                logger.info("Got object info")

                # If a person is detected and large enough in the frame:
                if self.person_detected(object_info):
                    logger.info("Person detected")
                    self.person_in_frame = True
                else:
                    logger.info("No person detected")
                    self.person_in_frame = False

                # Clear the stream in preparation for the next frame
                raw_capture.truncate(0)
                logger.info("Raw capture truncated")

                if not self.running:
                    logger.info("Cleaning up object detec")
                    self.cleanup()
                    break

            except KeyboardInterrupt:
                self.cleanup()
                break


# Below determines the size of the live feed window that will be displayed on the Raspberry Pi OS
if __name__ == "__main__":
    od = ObjectDetection()
    od_thread = od.stream()
    time.sleep(10)
    od.running = False
    od_thread.join()
