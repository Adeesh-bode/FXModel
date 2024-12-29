from fastapi import FastAPI , Depends, HTTPException
from app.ml_models.ml_model import find_best_matches
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.core.db_config import SessionLocal


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

def get_db():
    db = SessionLocal()
    try:
        yield db
        print("DB connection successful")
    finally:
        db.close()

from pydantic import BaseModel

from app.dbmodels.base import Size, PreferenceType , Color
class UserInput(BaseModel):
    sizeTop: Size
    sizeBottom: Size
    age: int
    weight: float
    height: float
    type: PreferenceType
    preferedColor: Color


@app.get("/")
async def root():
    return {"message": "Welcome!"}

@app.post("/health-db/")
async def health_check(db: Session = Depends(get_db)):
    try:
        # new_user = user.
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")

@app.post("/match/")
async def get_matches(user: UserInput, db: Session = Depends(get_db)):
    new_user = user.model_dump()

    # print(new_user)

    try:
        matches = find_best_matches(db, new_user)
        return {"matches": matches.to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error finding matches: {e}")