import numpy as np
from PIL import Image
import face_recognition


class FaceUtilsError(Exception):
    pass

class NoFaceDetected(FaceUtilsError):
    pass

class MultipleFacesDetected(FaceUtilsError):
    pass

class InvalidImage(FaceUtilsError):
    pass


def load_image(file_path):
    try:
        image = Image.open(file_path).convert("RGB")
        return np.array(image)
    except Exception as e:
        raise InvalidImage(f"Could not read image: {e}")


def detect_single_face(image):
    boxes = face_recognition.face_locations(image)

    if len(boxes) == 0:
        raise NoFaceDetected("No face found in the image")

    if len(boxes) > 1:
        raise MultipleFacesDetected("More than one face found — please use a photo with only one face")

    return boxes[0]


def extract_embedding(image):
    detect_single_face(image)

    encodings = face_recognition.face_encodings(image)

    if len(encodings) == 0:
        raise NoFaceDetected("Face was detected but could not be encoded")

    return encodings[0]


def compare_embeddings(embedding1, embedding2):

    emb1 = np.array(embedding1, dtype=np.float32)
    emb2 = np.array(embedding2, dtype=np.float32)

    distance = float(np.linalg.norm(emb1 - emb2))
    return distance