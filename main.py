from joblib import load
from fastapi import FastAPI
from pcap import LiveCapture
import threading

liveCapture = LiveCapture()

#Load the model
model = load('models/random_forest_model_dropped.joblib') 
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    global thread
    liveCapture.start_Capture() 
    thread = threading.Thread(target=liveCapture.fill_queue)
    thread.start()
@app.get('/')
def index():
    return {'message': 'This is the homepage of the API'}


@app.get('/queue')
def get_queue():
    return {"size": len(liveCapture.queue),"queue":liveCapture.queue}
@app.get('hello')
def hello():
    return {"msg": "hello"}

@app.get('/stop')
def stop_capture():
    return liveCapture.stop_Capture()
@app.get('/predict')
def predict(body):
    return {"prediction":model.predict(body)}

