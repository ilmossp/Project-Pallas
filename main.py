from fastapi import FastAPI
from joblib import load

#   Load models
random_forest = load('./models/randome_forest_model.joblib')
gradient_boosting = load('./models/gradient_boosting_model.joblib')

#  Create FastAPI app
app = FastAPI()

#  Create predict endpoint
@app.get("/")
def root():
    return {"message": "Hello ilyass"}