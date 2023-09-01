from joblib import load
from fastapi import FastAPI
from pcap import process_init, process_output



process = process_init()


process_output(process.stdout)


# Load the model
model = load('models/random_forest_model _dropped.joblib') 

app = FastAPI()

@app.get('/')
def index():
    return {'message': 'This is the homepage of the API'}

