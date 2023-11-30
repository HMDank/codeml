from fastapi import FastAPI, UploadFile, BackgroundTasks
import pandas as pd
import uvicorn
import pickle
import asyncio
import json
from model import car

app = FastAPI()


with open('model.pkl', 'rb') as f:
    rfc = pickle.load(f)
    f.close()
with open('encoder.pkl', 'rb') as file:
    le = pickle.load(file)
    file.close()


@app.get('/')
def home():
    return {'Use /docs'}

input = []

@app.post('/file_upload')
def upload_file(jsfile: UploadFile):
    data = json.load(jsfile.file)
    input.append(data)
    return {"content":data, 'of ':jsfile.filename}


#ASSUMES data ALWAYS IN JSON FORMAT
@app.post('/predict')
def predict_price(data:car):

    #Assign columns to use LE
    categorical_cols = ['brand', 'model', 'origin', 'type', 'gearbox', 'fuel']

    #Assign variables to 
    md = data.manufacture_date
    br = data.brand
    mo = data.model
    ori = data.origin
    typ = data.type
    sea = data.seats
    gear = data.gearbox
    fuel = data.fuel
    odo = data.mileage_v2

    sample = pd.DataFrame([[md, br, mo, ori, typ, sea, gear ,fuel, odo]],
                           columns=['manufacture_date','brand','model','origin','type','seats','gearbox','fuel','mileage_v2'])
   
   #Transform using LE
    for col in categorical_cols:
        sample[col] = le[col].transform(sample[col])

    #Use model to predict
    prediction = rfc.predict(sample)
    return {prediction.item()}

if __name__ == '__main__':
    uvicorn.run(app, host = '127.0.0.1', port = 8000)
