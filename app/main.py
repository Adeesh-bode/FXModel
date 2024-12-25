from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from app.models.ml_model import find_best_matches
import os
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI application
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # allow_cookies=True,
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

# Utility function to load dataset path
def get_csv_file_path():
    return os.path.join(os.path.dirname(__file__), 'dataset', 'synthetic_users_with_weight.csv')

# Endpoint: Root
@app.get("/")
async def read_root():
    return {"message": "Welcome to the Fashion Exchange!"}

# Endpoint: Get matches via POST
@app.post("/match/")
async def get_matches(user: UserInput):
    csv_file = get_csv_file_path()

    try:
        new_user = user.model_dump()
        matches = find_best_matches(csv_file, new_user)
        return {"matches": matches.to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding matches: {e}")

# Endpoint: Get matches via GET (for testing purposes)
# @app.get("/match/")
# async def get_matches_testing(
#     Size_Top: str = Query(...),
#     Size_Bottom: str = Query(...),
#     Age: int = Query(...),
#     Weight: float = Query(...),
#     Height: float = Query(...),
#     Style_Preference: str = Query(...),
#     Preferred_Colors: str = Query(...),
# ):
#     csv_file = get_csv_file_path()

#     try:
#         new_user = {
#             "Size_Top": Size_Top,
#             "Size_Bottom": Size_Bottom,
#             "Age": Age,
#             "Weight": Weight,
#             "Height": Height,
#             "Style_Preference": Style_Preference,
#             "Preferred_Colors": Preferred_Colors,
#         }

#         matches = find_best_matches(csv_file, new_user)
#         matches_json = matches.to_dict(orient="records")

#         return {"matches": matches_json, "new_user": new_user}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error finding matches: {e}")
