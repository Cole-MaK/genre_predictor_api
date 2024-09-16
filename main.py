from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.pipeline.predict_pipeline import PredictPipeline, CustomData
import uvicorn

app = FastAPI()

class SongRequest(BaseModel):
    song_name: str
    artist: str
    
@app.get('/')
def home():
    return {'health_check': 'OK'}

@app.post("/predict")
async def predict_song(request: SongRequest):
    try:
        custom_data = CustomData(
            song_name=request.song_name,
            artist=request.artist
        )
        song_df = custom_data.get_song_data()
        predict_pipeline = PredictPipeline()
        prediction = predict_pipeline.predict(song_df)
        return {"prediction": prediction}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # return {'song_name':request.song_name, 'artist':request.artist}