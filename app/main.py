from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.models.ml_model import find_best_matches
import os
from fastapi.middleware.cors import CORSMiddleware

# from prisma import Prisma
# prisma = Prisma()





app = FastAPI()
# @app.on_event("startup")
# async def startup():
#     await prisma.connect()

# @app.on_event("shutdown")
# async def shutdown():
#     await prisma.disconnect()
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
    csv_file = os.path.join(os.path.dirname(__file__), 'dataset', 'synthetic_users_with_weight.csv')
    
    try:
        new_user = user.dict()
        matches = find_best_matches(csv_file, new_user)
        return {"matches": matches.to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding matches: {e}")
    

@app.post('/user/')
async def create_user(user: UserInput):
    try:
        # Create user in the database
        created_user = await prisma.user.create(
            data={
                'Size_Top': user.Size_Top,
                'Size_Bottom': user.Size_Bottom,
                'Age': user.Age,
                'Weight': user.Weight,
                'Height': user.Height,
                'Style_Preference': user.Style_Preference,
                'Preferred_Colors': user.Preferred_Colors
            }
        )
        return created_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {e}")


@app.get("/")
async def read_root():
    return {"message": "Welcome to the Fashion Exchange!"}







#############testing

@app.get("/match/")
async def get_matches(Size_Top: str, Size_Bottom: str, Age: int, Weight: int, Height: int, Style_Preference: str, Preferred_Colors: str):
    csv_file = os.path.join(os.path.dirname(__file__), 'dataset', 'synthetic_users_with_weight.csv')
    

    # sample object

    # {
    #     'Size_Top': 'M',
    #     'Size_Bottom': 'L',
    #     'Height': 168,
    #     'Weight': 70,
    #     'Age': 25,
    #     'Style_Preference': 'Casual',
    #     'Preferred_Colors': 'Blue'
    # }

    try:
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
        
        # Convert matches DataFrame to JSON-serializable format    ##### IMP
        matches_json = matches.to_dict(orient='records')
        
        return {"matches": matches_json, "new_user": new_user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding matches: {e}")