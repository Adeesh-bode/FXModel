from sqlalchemy import Column, String, Float, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
import enum
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.compose import ColumnTransformer
from sklearn.metrics import pairwise_distances
from sqlalchemy.orm import Session
Base = declarative_base()

class Size(enum.Enum):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"
    SIZENOTREQUIRED = "SIZENOTREQUIRED"

class Color(enum.Enum):
    Red = "Red"
    Blue = "Blue"
    Green = "Green"
    Yellow = "Yellow"
    Orange = "Orange"
    Purple = "Purple"
    Pink = "Pink"
    Brown = "Brown"
    Black = "Black"
    White = "White"
    Grey = "Grey"

class PreferenceType(enum.Enum):
    Casual = "Casual"
    Formal = "Formal"
    Funky = "Funky"
    Sporty = "Sporty"
    Traditional = "Traditional"
    Streetwear = "Streetwear"

# Database model
class UserAttributes(Base):
    __tablename__ = 'UserAttributes'
    id = Column(String, primary_key=True)
    userId = Column(String, ForeignKey('User.id'), unique=True, nullable=False)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    age = Column(Integer, nullable=False)
    sizeTop = Column(String, nullable=False)
    sizeBottom = Column(String, nullable=False)
    preferedColor = Column(String, nullable=False)
    type = Column(String, nullable=False)
