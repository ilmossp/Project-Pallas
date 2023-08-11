from fastapi import FastAPI
from joblib import load
import pandas as pd
from sklearn.calibration import LabelEncoder

nominal_features = ['srcip', 'dstip', 'proto', 'state', 'service']



#preprocesssing
def preprocess(request):
    data = pd.read_json(request)
    data.dropna()
    label_encoder = LabelEncoder()
    for feature in nominal_features:
        data[feature] = label_encoder.fit_transform(data[feature])
        

#   Load models
#random_forest = load('./models/random_forest_model.joblib')
#gradient_boosting = load('./models/gradient_boosting_model.joblib')

#  Create FastAPI app
app = FastAPI()

#  Create predict endpoint
@app.get("/")
def root():
    return {"message": "Hello ilyass"}