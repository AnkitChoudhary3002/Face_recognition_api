# Face Recognition API

This project is a small FastAPI service for registering users with a face image and later authenticating them by comparing a new image against the stored face embedding.

## Features

- Register a user with `name`, `email`, and a face image.
- Authenticate a user with `email` and a face image.
- Stores face embeddings in a local SQLite database.
- Rejects invalid images, images with no face, or images with multiple faces.

## Project Structure

```text
face_recognition/
|-- app.py
|-- database.py
|-- face_utils.py
|-- README.md
|-- requirements.txt
```

Main files:

- `app.py` - FastAPI application and API endpoints.
- `database.py` - SQLite database helpers for saving and retrieving users.
- `face_utils.py` - Image loading, face detection, embedding extraction, and comparison helpers.
- `database.db` - Local SQLite database file.
- `uploads/` - Folder for uploaded or temporary image files.
- `requirements.txt` - Python dependencies.

## Requirements

- Python 3.10 or newer
- A virtual environment is recommended

## Environment Variables

The following environment variables can be configured:

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `FACE_THRESHOLD` | float | `0.6` | Euclidean distance threshold for face matching. Lower values require closer matches. |
| `DB_PATH` | string | `face_auth.db` | Path to the SQLite database file. |

Example:

```bash
# Set environment variables before running
set FACE_THRESHOLD=0.5
set DB_PATH=./my_database.db

uvicorn app:app --reload
```

## Installation

1. Create and activate a virtual environment.
2. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run the API

Start the server with Uvicorn:

```bash
uvicorn app:app --reload
```

The API will usually be available at:

```bash
http://127.0.0.1:8000
```

You can also open the interactive docs at:

```bash
http://127.0.0.1:8000/docs
```

## API Endpoints

### `POST /register`

Registers a new user with a face image.

Form fields:

- `name`
- `email`
- `image` - image file upload

Example:

```bash
curl -X POST "http://127.0.0.1:8000/register" ^
	-F "name=John Doe" ^
	-F "email=john@example.com" ^
	-F "image=@face.jpg"
```

### `POST /authenticate`

Checks whether a face image matches the stored embedding for the given email.

Form fields:

- `email`
- `image` - image file upload

Example:

```bash
curl -X POST "http://127.0.0.1:8000/authenticate" ^
	-F "email=john@example.com" ^
	-F "image=@face.jpg"
```

## Response Behavior

- Returns `success: true` when registration or authentication succeeds.
- Returns a `400` response for invalid images, no detected face, or multiple faces.
- Returns a `404` response from `/authenticate` when the email is not found.

## Notes

- Face matching uses Euclidean distance between embeddings.
- The matching threshold can be configured via the `FACE_THRESHOLD` environment variable (default: `0.6`).
- The database path can be configured via the `DB_PATH` environment variable (default: `face_auth.db`).
- If you want to reset the database, delete the local SQLite file and restart the app.
