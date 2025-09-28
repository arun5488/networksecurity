import os
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from src.networksecurity import logger
from src.networksecurity import constants as const
from src.networksecurity.pipeline.training_pipeline import TrainingPipeline
from src.networksecurity.utils.common import load_object
from fastapi.templating import Jinja2Templates
from src.networksecurity.pipeline.prediction_pipeline import PredictionPipeline

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


templates = Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train():
    try:
        logger.info("Inside train method in app.py")
        TrainingPipeline().initiate_training_pipeline()
        return Response("Training completed successfully")
    except Exception as e:
        logger.error(f"error occured in train method in app.py:{e}")
        raise e

@app.post("/predict")
async def predict(request:Request,file:UploadFile=File(...)):
    try:
        logger.info("Inside predict method in app.py")
        df = pd.read_csv(file.file)
        estimator = PredictionPipeline()
        y_pred = estimator.predict(df)
        df['Predicted']=y_pred
        table_html = df.to_html()
        return templates.TemplateResponse("table.html",{"request":request, "table":table_html})
    except Exception as e:
        logger.error(f"error occured in train method in app.py:{e}")
        raise e



if __name__=="__main__":
    app_run(app,host="0.0.0.0",port=8080)