import dlib
import cv2
import imutils
import logging as log

from Config_and_Log import logs, config
from time import sleep, time

logs.initialize_logger("face_detection")


# Fancy box drawing function.
def draw_border(img, pt1, pt2, color, thickness, r, d):
    x1, y1 = pt1
    x2, y2 = pt2

    # Top left drawing
    cv2.line(img, (x1 + r, y1), (x1 + r + d, y1), color, thickness)
    cv2.line(img, (x1, y1 + r), (x1, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)

    # Top right drawing
    cv2.line(img, (x2 - r, y1), (x2 - r - d, y1), color, thickness)
    cv2.line(img, (x2, y1 + r), (x2, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)

    # Bottom left drawing
    cv2.line(img, (x1 + r, y2), (x1 + r + d, y2), color, thickness)
    cv2.line(img, (x1, y2 - r), (x1, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)

    # Bottom right drawing
    cv2.line(img, (x2 - r, y2), (x2 - r - d, y2), color, thickness)
    cv2.line(img, (x2, y2 - r), (x2, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)


def face_detection(browser_driver):
    log.debug("Inside face_detection")

    try:
        # Grab video from your web cam.
        stream = cv2.VideoCapture(0)
        if not stream.isOpened():
            log.error('Unable to load camera.')
            sleep(5)
            pass

        # Face detector using dlib.
        detector = dlib.get_frontal_face_detector()

        # variables for calculation refreshing rate.
        active = False
        start_time = time()

        while True:
            # read frames from live web cam stream.
            (grabbed, frame) = stream.read()

            # resize the frames to be smaller and switch to gray scale.
            frame = imutils.resize(frame, width=700)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Make copies of the frame for transparency processing.
            overlay = frame.copy()
            output = frame.copy()

            # set transparency value.
            alpha = 0.5

            # detect faces in the gray scale frame.
            faces_details = detector(gray, 0)

            # Reset face count.
            i = 0

            # loop over the face detections.
            for num_faces, dimensions in enumerate(faces_details):
                i = num_faces + 1
                x1 = dimensions.left()
                y1 = dimensions.top()
                x2 = dimensions.right() + 1
                y2 = dimensions.bottom() + 1
                # w = dimensions.width()
                # h = dimensions.height()

                # draw a fancy border around the faces.
                draw_border(overlay, (x1, y1), (x2, y2), (162, 255, 0), 2, 10, 10)

            if i > 0 and active is False:
                active = True
                elapsed_time = time() - start_time

                # Reset Context if time elapse > 10.
                if elapsed_time > 10:
                    print("Reset")
                    log.debug("Reset")
                    browser_driver.refresh_instance()

            # elif i >= 0:
            #     pass

            elif i > 0 and active is True:
                pass
            elif i == 0 and active is False:
                pass

            else:
                start_time = time()
                active = False

            # make semi-transparent bounding box.
            cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

            # show the frame.
            # cv2.imshow("Face Detection", output)

            # Exit Face detection.
            key = cv2.waitKey(20)
            if key == int(config.face_detection['exit_key']):  # exit on ESC
                log.debug("Exiting the face detection.")
                break

        # cleanup and releasing the cam resources.
        stream.release()
        cv2.destroyAllWindows()
        log.debug("All the resources are released.")

    except Exception as e:
        log.error("Error in face detection. Error message: %s", e)
