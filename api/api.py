import os
import dotenv
import pickle
import pandas as pd
from fastapi import FastAPI, HTTPException
from api.schemas import InferenceInput, InferenceOutput

# Load environmental variables
dotenv.load_dotenv()
API_PORT = int(os.getenv("API_PORT"))
MODEL_PATH = str(os.getenv("MODEL_PATH"))


# Initialize the FastAPI
api = FastAPI(
    title="Random Forest Regressor Inference API",
    version="1.0.0",
    description="A simple API to serve a machine learning regression model.",
)


# Load the trained model globally
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)


# Create the POST endpoint for inference
@api.post("/predict", response_model=InferenceOutput, status_code=200)
async def predict(payload: InferenceInput):
    try:
        # Convert Pydantic payload to the format expected by scikit-learn
        input_data = pd.DataFrame(
            {
                "MedInc": [payload.median_income],
                "HouseAge": [payload.housing_median_age],
                "AveRooms": [payload.total_rooms],
                "AveBedrms": [payload.total_bedrooms],
                "Population": [payload.population],
                "AveOccup": [payload.households],
                "Latitude": [payload.latitude],
                "Longitude": [payload.longitude],
            }
        )

        # Perform inference
        prediction_result = model.predict(input_data)

        # Return the structured response
        return InferenceOutput(prediction=float(prediction_result[0]))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failed: {str(e)}")


# Run the API using Uvicorn
if __name__ == "__main__":
    import uvicorn

    # Run server on 0.0.0.0 to allow access from other containers
    uvicorn.run("api.api:api", host="0.0.0.0", port=API_PORT)
