import traceback
from joblib import load
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from db import fetch_latest_flows, fetch_stats
from pcap import LiveCapture
import threading
from prediction import predict

liveCapture = LiveCapture()
app = FastAPI()

origins = ["http://localhost", "*"]

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
    return {"len": len(liveCapture.queue), "queue": liveCapture.queue}


@app.get("/stop")
def stop_capture():
    if liveCapture.stop_Capture() == True:
        return "process stopped successfully"
    else:
        return "could not stop process, consider terminating the app"


@app.get("/predict")
def predict_from_json(body):
    return {"prediction": predict(body)}


@app.get("/allrecords")
def get_all_records():
    flows = fetch_latest_flows()
    return flows


@app.get("/stats")
def getStats():
    stats = fetch_stats()
    return stats
