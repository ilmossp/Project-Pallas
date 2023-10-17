from joblib import load
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from pcap import LiveCapture
import threading

liveCapture = LiveCapture()

# Load the model
model = load("models/random_forest_model_dropped.joblib")
app = FastAPI()

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods="*",
)


@app.on_event("startup")
async def startup_event():
    global thread
    liveCapture.start_Capture()
    thread = threading.Thread(target=liveCapture.fill_queue)
    thread.start()


@app.get("/")
def index():
    return {"message": "This is the homepage of the API"}


@app.get("/queue")
def get_queue(response: Response):
    if len(liveCapture.queue) < 100:
        response.status_code = status.HTTP_202_ACCEPTED
        return {"message": "Queue still loading"}
    return {"queue": liveCapture.queue}


@app.get("/stop")
def stop_capture():
    return liveCapture.stop_Capture()


@app.get("/predict")
def predict(body):
    return {"prediction": model.predict(body)}
