import pymysql
import tensorflow as tf
import cv2
import numpy as np
from scipy.special import softmax
import time
from datetime import datetime
from config.config import UpdateUserStatus


class MaskRecognition():
    def __init__(self):
        # Load the face recognition model
        self.face_detector = cv2.dnn.readNetFromCaffe('./weights/deploy.prototxt.txt',
                                                      './weights/res10_300x300_ssd_iter_140000.caffemodel')
        self.model = tf.keras.models.load_model('./models/vgg19.h5')
        self.labels = ['1.yes', '2.no', '3.nose']
        # Load the image overlay list
        self.overlay_list = self.getPngList()
        self.username = None

    def getPngList(self):
        overlay_list = []
        for i in range(3):
            path = "./label_img/%s.png" % (i)
            overlay = cv2.imread(path, cv2.COLOR_RGB2BGR)
            overlay = cv2.resize(overlay, (0, 0), fx=0.3, fy=0.3)
            overlay_list.append(overlay)
        return overlay_list

    def toBlob(self, img):
        # blob dealing
        img_blob = cv2.dnn.blobFromImage(img, 1, (100, 100), (104, 177, 123), swapRB=True)
        img_squeeze = np.squeeze(img_blob).T
        img_rotate = cv2.rotate(img_squeeze, cv2.ROTATE_90_CLOCKWISE)
        img_flip = cv2.flip(img_rotate, 1)
        # Normalized processing
        img_blob = np.maximum(img_flip, 0) / img_flip.max()
        return img_blob

    def recognize(self, username):
        # Normalized processing
        cap = cv2.VideoCapture(0)
        # Video width and height
        frame_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # Rectangle box color list
        rec_colors = [(0, 255, 0), (0, 0, 255), (0, 255, 255)]
        # Record the frame rate time
        start_time = time.time()


        conn = pymysql.connect(
            user="root",
            password="xyz",
            database="finalproject"
        )


        cursor = conn.cursor()


        check_table_query = f"SHOW TABLES LIKE '{username}'"
        cursor.execute(check_table_query)
        table_exists = cursor.fetchone()

        if not table_exists:
            print(f"Table '{username}' does not exist.")

            conn.close()
            return

        while True:
            # Read frame
            ret, frame = cap.read()
            # flip
            frame = cv2.flip(frame, 1)

            # blob
            img_blob = cv2.dnn.blobFromImage(frame, 1, (300, 300), (104, 177, 123), swapRB=True)
            # Recognize Faces
            self.face_detector.setInput(img_blob)
            # Reasoning
            detections = self.face_detector.forward()
            # Number of people
            person_count = detections.shape[2]
            # Number of traversals
            for face_index in range(person_count):
                # Get confidence
                confidence = detections[0, 0, face_index, 2]
                # Pick confidence
                if confidence > 0.5:
                    # Get face position
                    locations = detections[0, 0, face_index, 3:7] * np.array([frame_w, frame_h, frame_w, frame_h])
                    l, t, r, b = locations = locations.astype('int')
                    # Get face area
                    img_crop = frame[t:b, l:r]
                    # blob
                    img_blob = self.toBlob(img_crop)
                    # Prediction
                    img_input = img_blob.reshape(1, 100, 100, 3)
                    result = self.model.predict(img_input)
                    # softmax Processing
                    result = softmax(result[0])
                    # Maximum index
                    max_index = result.argmax()

                    # Set the label
                    overlay = self.overlay_list[max_index]
                    overlay_h, overlay_w = overlay.shape[:2]

                    # Coverage range
                    overlay_l, overlay_t = l, (t - overlay_h - 20)
                    # If the boundary is beyond the boundary, it will not be displayed
                    overlay_r, overlay_b = (l + overlay_w), (overlay_t + overlay_h)
                    if overlay_t > 0 and overlay_r < frame_w:
                        overlay_copy = cv2.addWeighted(frame[overlay_t:overlay_b, overlay_l:overlay_r], 0.7, overlay, 1,
                                                       0)
                        frame[overlay_t:overlay_b, overlay_l:overlay_r] = overlay_copy

                    # Draw face frame
                    cv2.rectangle(frame, (l, t), (r, b), rec_colors[max_index], 3)

            now_time = time.time()
            # Calculate the frame rate
            fps_time = int(1 / (now_time - start_time))
            start_time = now_time
            fps_text = 'fps:' + str(fps_time)
            name_text = 'User: ' + username
            # Get current time
            current_time = datetime.now()
            current_time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
            # Update user table with mask_time and masked values
            print("username:"+username)
            time_text = 'Current Time: ' + current_time_str

            tip_text = 'Press the space bar to close'
            # Display frame rate and current time
            cv2.putText(frame, fps_text, (20, 30), cv2.FONT_ITALIC, 1, (0, 255, 0), 3)
            cv2.putText(frame, name_text, (110, 30), cv2.FONT_ITALIC, 1, (0, 0, 255), 3)
            cv2.putText(frame, time_text, (20, 70), cv2.FONT_ITALIC, 1, (0, 255, 0), 3)
            cv2.putText(frame, tip_text, (20, 110), cv2.FONT_ITALIC, 1, (0, 255, 0), 3)

            cv2.imshow('face_mask', frame)

            if cv2.waitKey(10) & 0xFF == ord(' '):
                cv2.destroyWindow('face_mask')
                insert_query = f"INSERT INTO `{username}` (mask_time, masked) VALUES ('{current_time_str}', 'y')"
                cursor.execute(insert_query)
                conn.commit()
                UpdateUserStatus()
                break

        cap.release()
        cv2.destroyWindow('face_mask')

        conn.close()


