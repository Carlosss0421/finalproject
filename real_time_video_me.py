import cv2
import imutils
import numpy as np
from PyQt5 import QtGui, QtWidgets
from keras.models import load_model
from keras.utils import img_to_array


class Emotion_Rec:
    def __init__(self, model_path=None):

        # Load data and image parameters
        detection_model_path = 'models/haarcascade_frontalface_default.xml'

        if model_path == None:  # Use default model if path is not specified
            emotion_model_path = 'models/vgg19_CNN.19-0.66.hdf5'
        else:
            emotion_model_path = model_path

        # Load face detection model
        self.face_detection = cv2.CascadeClassifier(detection_model_path)  # Cascade Classifier

        # Load emotion recognition model
        self.emotion_classifier = load_model(emotion_model_path, compile=False)
        # Emotion categories
        self.EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised",
                         "neutral"]

    def run(self, frame_in, canvas, label_face, label_result):
        # Adjust frame size
        frame = imutils.resize(frame_in, width=300)  # Resize frame
        # frame = cv2.resize(frame, (300,300))  # Resize frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

        # Detect faces
        faces = self.face_detection.detectMultiScale(gray, scaleFactor=1.1,
                                                     minNeighbors=5, minSize=(30, 30),
                                                     flags=cv2.CASCADE_SCALE_IMAGE)
        preds = []  # Predicted results
        label = None  # Predicted label
        (fX, fY, fW, fH) = None, None, None, None  # Face position
        if len(faces) > 0:
            # Select the largest detected face ROI
            faces = sorted(faces, reverse=True, key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
            (fX, fY, fW, fH) = faces

            # Extract the region of interest (ROI) from the grayscale image, resize it to 64*64 pixels,
            # and prepare the ROI for classification through the CNN
            roi = gray[fY:fY + fH, fX:fX + fW]
            roi = cv2.resize(roi, (48, 48))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            # Predict probabilities for each emotion category using the model
            preds = self.emotion_classifier.predict(roi)[0]
            label = self.EMOTIONS[preds.argmax()]  # Select the emotion category with the highest probability

        frameClone = frame.copy()  # Copy the frame

        for (i, (emotion, prob)) in enumerate(zip(self.EMOTIONS, preds)):
            # Display probabilities for each category
            text = "{}: {:.2f}%".format(emotion, prob * 100)

            # Draw a bar graph for each emotion category and its corresponding probability
            w = int(prob * 300) + 2
            cv2.rectangle(canvas, (7, (i * 26) + 5), (w, (i * 26) + 26), (224, 200, 130), -1)
            cv2.putText(canvas, text, (10, (i * 26) + 23), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), 1)

            # Draw a rectangle around the face region and display the recognition result
            cv2.putText(frameClone, label, (fX, fY - 10),
                        cv2.FONT_HERSHEY_TRIPLEX, 0.6, (0, 255, 0), 1)
            cv2.rectangle(frameClone, (fX, fY), (fX + fW, fY + fH), (255, 255, 0), 1)

        # Adjust the frame size to fit the interface
        frameClone = cv2.resize(frameClone, (420, 280))

        # Display the face image in the Qt interface
        show = cv2.cvtColor(frameClone, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        label_face.setPixmap(QtGui.QPixmap.fromImage(showImage))
        QtWidgets.QApplication.processEvents()

        # Display the result in the label for result display
        show = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        label_result.setPixmap(QtGui.QPixmap.fromImage(showImage))

        return label
