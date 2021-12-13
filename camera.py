#Import the Open-CV extra functionalities
import os
import time

import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera

# This is to pull the information about what each object is called
class_names = []
base_path = "object_detection"
class_file = os.path.join(base_path, "coco.names")
with open(class_file, "rt") as f:
    class_names = f.read().rstrip("\n").split("\n")

# This is to pull the information about what each object should look like
config_path = os.path.join(base_path,
                           "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt")
weights_path = os.path.join(base_path, "frozen_inference_graph.pb")

# This is some set up values to get good results
net = cv2.dnn_DetectionModel(weights_path, config_path)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


# This is to set up what the drawn box size/colour is and the font/size/colour of the name tag and confidence label
def get_objects(img, thres, nms, draw=True, objects=[]):
    class_ids, confs, bbox = net.detect(img,
                                        confThreshold=thres,
                                        nmsThreshold=nms)
    # Below has been commented out, if you want to print each sighting of an object to the console you can uncomment below
    # print(class_ids, bbox)
    if len(objects) == 0:
        objects = class_names
    object_info = []
    if len(class_ids) != 0:
        for class_id, confidence, box in zip(class_ids.flatten(),
                                             confs.flatten(), bbox):
            class_name = class_names[class_id - 1]
            if class_name in objects:
                object_info.append([box, class_name])
                if (draw):
                    cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
                    cv2.putText(img, class_names[class_id - 1].upper(),
                                (box[0] + 10, box[1] + 30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(img, str(round(confidence * 100,
                                               2)), (box[0] + 200, box[1] + 30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    return img, object_info


def person_is_looking(img, object_info):
    for i, object in enumerate(object_info):
        box, class_name = object
        if class_name == "person":
            x0, y0, x1, y1 = box
            width = x1 - x0
            height = y1 - y0
            area = width * height
            area_proportion = area / (640 * 480)
            print(f"(Obj{i}) Area: {area}\n",
                  f"(Obj{i}) Frame percentage: {area_proportion * 100}%")


# Below determines the size of the live feed window that will be displayed on the Raspberry Pi OS
if __name__ == "__main__":
    # cap = cv2.VideoCapture(0)
    # cap.set(3, 640)
    # cap.set(4, 480)
    # cap.set(10,70)

    # Initialize the PiCamera
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 2
    raw_capture = PiRGBArray(camera, size=camera.resolution)

    # Allow the camera to warmup
    time.sleep(0.1)

    # Below is the never ending loop that determines what will happen when an object is identified.
    # while True:
    #     # success, img = cap.read()

    #     # Below provides a huge amount of controll. the 0.45 number is the threshold number, the 0.2 number is the nms number)
    #     result, object_info = get_objects(img,
    #                                       0.45,
    #                                       0.2,
    #                                       objects=["shoe", "person"])
    #     # print(object_info)
    #     cv2.imshow("Output", img)
    #     cv2.waitKey(1)
    #     # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     #     pass

    for frame in camera.capture_continuous(raw_capture,
                                           format="bgr",
                                           use_video_port=True):
        try:
            # Grab an image from the camera
            img = frame.array

            # Below provides a huge amount of control.
            # 0.45 = threshold number, 0.2 = nms number
            # start = time.time()
            result, object_info = get_objects(img,
                                              0.45,
                                              0.2,
                                              objects=["shoe", "person"])
            person_is_looking(result, object_info)
            # elapsed_time = time.time() - start
            # print(f"Elapsed time: {elapsed_time}")
            print(f"Object: {object_info}")

            # Show the frame
            cv2.imshow("Output", result)
            cv2.waitKey(1)

            # Clear the stream in preparation for the next frame
            raw_capture.truncate(0)

        # If the q key was pressed, break from the loop
        except KeyboardInterrupt:
            break