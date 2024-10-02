from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.models.ml_model import find_best_matches
import os
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define the data model for user input
class UserInput(BaseModel):
    Size_Top: str
    Size_Bottom: str
    Age: int
    Weight: float
    Height: float
    Style_Preference: str
    Preferred_Colors: str

# Define the endpoint to get the top 10 matches
@app.post("/match/")
async def get_matches(user: UserInput):
    csv_file = os.path.join(os.path.dirname(__file__), 'dataset', 'user_data.csv')
    
    try:
        new_user = user.dict()
        matches = find_best_matches(csv_file, new_user)
        return {"matches": matches.to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding matches: {e}")
    


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Fashion Exchange!"}







#############testing

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI()

# Assuming the UserInput class exists
class UserInput(BaseModel):
    Size_Top: str
    Size_Bottom: str
    Age: int
    Weight: int
    Height: int
    Style_Preference: str
    Preferred_Colors: str

def find_best_matches(csv_file, new_user):
    # Dummy function for now
    return [{"match": "Best Match 1"}, {"match": "Best Match 2"}]

# GET request to match based on query parameters
@app.get("/match/")
async def get_matches(Size_Top: str, Size_Bottom: str, Age: int, Weight: int, Height: int, Style_Preference: str, Preferred_Colors: str):
    csv_file = os.path.join(os.path.dirname(__file__), 'dataset', 'user_data.csv')
    
    try:
        # Simulating the user input by gathering from query parameters
        new_user = {
            "Size_Top": Size_Top,
            "Size_Bottom": Size_Bottom,
            "Age": Age,
            "Weight": Weight,
            "Height": Height,
            "Style_Preference": Style_Preference,
            "Preferred_Colors": Preferred_Colors
        }

        print(new_user)
        
        matches = find_best_matches(csv_file, new_user)
        print(matches)
        return {"matches": matches , "new_user": new_user} 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding matches: {e}")
