# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from app.dbmodels.base import Base

# DATABASE_URL = "postgresql://main-db_owner:IA2FW5CTEBsh@ep-restless-water-a4avem0x-pooler.us-east-1.aws.neon.tech/main-db?sslmode=require"  # Replace with your DB URL
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(bind=engine)

# # Create tables if they don't exist
# Base.metadata.create_all(engine)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.dbmodels.base import Base

DATABASE_URL = "postgresql://main-db_owner:IA2FW5CTEBsh@ep-restless-water-a4avem0x-pooler.us-east-1.aws.neon.tech/main-db?sslmode=require"

# engine setup with pooling & reliability fixes
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # Checks if connection is alive before using
    pool_recycle=300,     # Recycles connections every 5 minutes (Neon timeout safe)
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base.metadata.create_all(engine)
