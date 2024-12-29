from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.dbmodels.base import Base

DATABASE_URL = "postgresql://main-db_owner:IA2FW5CTEBsh@ep-restless-water-a4avem0x.us-east-1.aws.neon.tech/main-db?sslmode=require"  # Replace with your DB URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Create tables if they don't exist
Base.metadata.create_all(engine)
