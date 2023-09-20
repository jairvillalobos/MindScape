"""
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import tensorflow as tf

class EmotionDetector:
    def __init__(self):
        self.configure_gpu()
        self.faceCascade, self.model = self.load_cascade_and_model()
        self.target = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def configure_gpu(self):
        config = tf.compat.v1.ConfigProto()
        config.gpu_options.per_process_gpu_memory_fraction = 0.1
        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            try:
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
            except RuntimeError as e:
                print(e)

    def load_cascade_and_model(self):
        faceCascade = cv2.CascadeClassifier('app/frontal_face/haarcascade_frontalface_default.xml')
        model = load_model('app/keras_model/model_5-49-0.62.hdf5')
        return faceCascade, model

    def detect_emotion(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(gray, scaleFactor=1.1)

        for (x, y, w, h) in faces:
            face_crop = frame[y:y + h, x:x + w]
            face_crop = cv2.resize(face_crop, (48, 48))
            face_crop = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
            face_crop = face_crop.astype('float32') / 255
            face_crop = np.asarray(face_crop).reshape(1, 1, face_crop.shape[0], face_crop.shape[1])
            result = self.target[np.argmax(self.model.predict(face_crop))]

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2, 5)
            cv2.putText(frame, result, (x, y), self.font,
                        1, (200, 0, 0), 3, cv2.LINE_AA)

    def run(self):
        video_capture = cv2.VideoCapture(0)
        try:
            while True:
                ret, frame = video_capture.read()
                self.detect_emotion(frame)
                cv2.imshow('Video', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            video_capture.release()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    detector = EmotionDetector()
    detector.run()
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import tensorflow as tf
import base64
import json
import logging

router = APIRouter()
logging.basicConfig(level=logging.INFO)


class EmotionDetector:
    def __init__(self, model_path, cascade_path):
        self.model = load_model(model_path)
        self.faceCascade = cv2.CascadeClassifier(cascade_path)
        self.target = ['angry', 'disgust', 'fear',
                       'happy', 'sad', 'surprise', 'neutral']
        self.font = cv2.FONT_HERSHEY_SIMPLEX

    def detect_faces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.faceCascade.detectMultiScale(gray, scaleFactor=1.1)
        return faces

    def predict_emotion(self, face_crop):
        face_crop = face_crop.astype('float32') / 255
        face_crop = np.asarray(face_crop).reshape(
            1, 1, face_crop.shape[0], face_crop.shape[1])
        result = self.target[np.argmax(self.model.predict(face_crop))]
        return result

    def draw_rectangle_and_text(self, frame, x, y, w, h, result):
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2, 5)
        cv2.putText(frame, result, (x, y), self.font,
                    1, (200, 0, 0), 3, cv2.LINE_AA)

    def detect_emotion(self, frame):
        faces = self.detect_faces(frame)

        results = []
        for (x, y, w, h) in faces:
            face_crop = frame[y:y + h, x:x + w]
            face_crop = cv2.resize(face_crop, (48, 48))
            face_crop = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
            result = self.predict_emotion(face_crop)

            self.draw_rectangle_and_text(frame, x, y, w, h, result)

            results.append({
                'emotion': result,
                'coordinates': (int(x), int(y), int(w), int(h))
            })

        return frame, results


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    detector = EmotionDetector('keras_model/model_5-49-0.62.hdf5',
                               'frontal_face/haarcascade_frontalface_default.xml')
    video_capture = cv2.VideoCapture(0)
    await websocket.accept()
    try:
        while True:
            ret, frame = video_capture.read()
            if not ret:
                logging.error(
                    "No se pudo obtener un frame de la cámara. Asegúrate de que tu cámara esté conectada y funcionando correctamente.")
                break

            frame_with_emotions_detected, emotions_detected = detector.detect_emotion(
                frame)

            _, buffer = cv2.imencode('.jpg', frame_with_emotions_detected)
            encoded_image = base64.b64encode(buffer).decode('utf-8')

            await websocket.send_text(json.dumps({
                'image': encoded_image,
                'emotions': emotions_detected
            }))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except WebSocketDisconnect:
        logging.error("La conexión WebSocket se ha cerrado inesperadamente.")
    finally:
        video_capture.release()