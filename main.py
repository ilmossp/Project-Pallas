import traceback
from joblib import load
from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from db import fetch_latest_flows
from pcap import LiveCapture
import threading
import copy

liveCapture = LiveCapture()

# Load the model
model = load("models/final_random_forest_model.joblib")
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
    if len(liveCapture.queue) < 100:
        response.status_code = status.HTTP_202_ACCEPTED
        return {"message": "Queue still loading"}
    df = liveCapture.preprocessBatch()
    predictions = model.predict(df).tolist()
    if len(predictions) == len(liveCapture.queue):
        queue = copy.deepcopy(liveCapture.queue)
        for item in queue:
            item["Label"] = predictions[queue.index(item)]
        return queue
    else:
        return {"message": "could not predict"}


@app.get("/stop")
def stop_capture():
    return liveCapture.stop_Capture()


@app.get("/predict")
def predict(body):
    return {"prediction": model.predict(body)}


@app.get("/dataframe")
def get_dataframe():
    try:
        df = liveCapture.preprocessBatch()
        predictions = model.predict(df)
        return predictions.tolist()
    except:
        traceback.print_exc()
        return "an error has occured"


@app.get("/allrecords")
def get_all_records():
    flows = fetch_latest_flows()
    return flows
