from fastapi import FastAPI, Response
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


@app.post("/start")
def start_Capture(response: Response):
    if liveCapture.status():
        response.status_code = 202
        return "process already started"
    else:
        liveCapture.start_Capture()
        return "process started successfully"


@app.post("/stop")
def stop_capture(response: Response):
    if liveCapture.status():
        if liveCapture.stop_Capture() == True:
            return "Process Stopped Successfully"
        else:
            response.status_code = 500
            return "Process Could Not Be Stopped"
    else:
        response.status_code = 202
        return "Process already Stopped"


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


@app.get("/status")
def getStatus():
    status = liveCapture.status()
    return {"status": status}
