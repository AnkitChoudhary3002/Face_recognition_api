from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
import tempfile
import sqlite3
import os

from database import init_db, insert_user, get_user_embedding
from face_utils import (
    load_image,
    extract_embedding,
    compare_embeddings,
    NoFaceDetected,
    MultipleFacesDetected,
    InvalidImage,
)

THRESHOLD = 0.6

app = FastAPI()

init_db()


def save_image_temporarily(image: UploadFile) -> str:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(image.file.read())
        return tmp.name


@app.post("/register")
async def register(
    name: str = Form(...),
    email: str = Form(...),
    image: UploadFile = File(...),
):

    tmp_path = None 
    try:
        tmp_path = save_image_temporarily(image)
        img_array = load_image(tmp_path)
        embedding = extract_embedding(img_array)

        insert_user(name, email, embedding)
        return {"success": True, "email": email}

    except sqlite3.IntegrityError:
        return JSONResponse(status_code=409, content={
            "success": False,
            "message": "This email is already registered"
        })

    except NoFaceDetected:
        return JSONResponse(status_code=400, content={
            "success": False,
            "message": "No face detected in the image"
        })

    except MultipleFacesDetected:
        return JSONResponse(status_code=400, content={
            "success": False,
            "message": "Multiple faces detected — please use a photo with only one face"
        })

    except InvalidImage:
        return JSONResponse(status_code=400, content={
            "success": False,
            "message": "Could not read the image — make sure it's a valid photo"
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={
            "success": False,
            "message": str(e)
        })

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)


@app.post("/authenticate")
async def authenticate(
    email: str = Form(...),
    image: UploadFile = File(...),
):
   
    tmp_path = None
    try:
        record = get_user_embedding(email)
        if record is None:
            return JSONResponse(status_code=404, content={
                "success": False,
                "message": "No account found with this email"
            })

        # record is (email, embedding) — we only need the embedding here
        _, stored_embedding = record

        tmp_path = save_image_temporarily(image)
        img_array = load_image(tmp_path)
        new_embedding = extract_embedding(img_array)

        distance = compare_embeddings(stored_embedding, new_embedding)

        if distance < THRESHOLD:
            return {
                "success": True,
                "email": email,
                "distance": round(distance, 4),
                "message": "Face matched successfully"
            }
        else:
            return JSONResponse(status_code=401, content={
                "success": False,
                "email": email,
                "distance": round(distance, 4),
                "message": "Face did not match"
            })

    except NoFaceDetected:
        return JSONResponse(status_code=400, content={
            "success": False,
            "message": "No face detected in the image"
        })

    except MultipleFacesDetected:
        return JSONResponse(status_code=400, content={
            "success": False,
            "message": "Multiple faces detected — please use a photo with only one face"
        })

    except InvalidImage:
        return JSONResponse(status_code=400, content={
            "success": False,
            "message": "Could not read the image — make sure it's a valid photo"
        })

    except Exception as e:
        return JSONResponse(status_code=500, content={
            "success": False,
            "message": str(e)
        })

    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)