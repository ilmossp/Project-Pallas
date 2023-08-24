from joblib import load
from fastapi import FastAPI
import subprocess



command = 'argus -w - | ra -N 100 -s ra -r captured.argus -s srid,saddr,daddr,state,sload,dload,stcpb,tcprtt,sjit,djit,trans,stcpb,dtcpb,smean,dmean,sport,dsport,proto,dur,sbytes,dbytes,sttl,dttl,Spkts,Dpkts -M xml > captured.xml'
#subprocess.call(command, shell=True)


# Load the model

model = load('models/random_forest_model _dropped.joblib') 

app = FastAPI()


@app.get('/')
def index():
    return {'message': 'This is the homepage of the API'}

