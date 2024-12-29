from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.neighbors import NearestNeighbors
from sqlalchemy.orm import Session
import pandas as pd
import enum

def compatibility_pipeline():
    categorical_features = ['sizeTop', 'sizeBottom']
    numerical_features = ['age', 'weight', 'height']

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features),
            ('num', StandardScaler(), numerical_features)
        ]
    )

    return preprocessor

# Preprocessing pipeline for preferences (style, colors)
def preference_pipeline():
    categorical_features = ['type', 'preferedColor']

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ]
    )

    return preprocessor

# Function to fetch user data from the database
def fetch_user_data(db: Session):
    from app.dbmodels.base import UserAttributes  # Import SQLAlchemy models

    query = (
        db.query(
            UserAttributes.id.label("id"),
            UserAttributes.userId.label("userId"),
            UserAttributes.sizeTop.label("sizeTop"),
            UserAttributes.sizeBottom.label("sizeBottom"),
            UserAttributes.age.label("age"),
            UserAttributes.weight.label("weight"),
            UserAttributes.height.label("height"),
            UserAttributes.type.label("type"),
            UserAttributes.preferedColor.label("preferedColor")
        )
        .all()
    )

    print("Fetched User Data Query Results:")
    print(query[0])  # Print first row to verify the output
    
    # Convert query results to DataFrame
    df = pd.DataFrame(query, columns=[
        "id", "userId", "sizeTop", "sizeBottom", "age", "weight", "height", "type", "preferedColor"
    ])

    # Convert Enum fields to string
    enum_columns = ["sizeTop", "sizeBottom", "type", "preferedColor"]
    for col in enum_columns:
        df[col] = df[col].apply(lambda x: x.value if isinstance(x, enum.Enum) else x)

    return df

# Function to check compatibility based on size, age, weight, height
def check_compatibility(df, new_user, n_neighbors=50):
    preprocessor = compatibility_pipeline()
    
    X = df[['sizeTop', 'sizeBottom', 'age', 'weight', 'height']]
    
    transformed_data = preprocessor.fit_transform(X)

    new_user_data = pd.DataFrame([new_user])[['sizeTop', 'sizeBottom', 'age', 'weight', 'height']]
    transformed_new_user = preprocessor.transform(new_user_data)
    
    knn = NearestNeighbors(n_neighbors=n_neighbors, metric='euclidean')
    knn.fit(transformed_data)
    
    distances, indices = knn.kneighbors(transformed_new_user)
    
    compatible_users = df.iloc[indices[0]]
    return compatible_users

# Function to match based on style and color preference
def match_preferences(compatible_users, new_user, top_n=10):
    preprocessor = preference_pipeline()

    X = compatible_users[['type', 'preferedColor']]
    
    transformed_data = preprocessor.fit_transform(X)

    new_user_data = pd.DataFrame([new_user])[['type', 'preferedColor']]
    transformed_new_user = preprocessor.transform(new_user_data)
    
    distances = pairwise_distances(transformed_new_user, transformed_data, metric='cosine')[0]
    
    compatible_users['Distance'] = distances
    top_matches = compatible_users.sort_values(by='Distance').head(top_n)
    
    return top_matches

# Main function to find top 10 matches
def find_best_matches(db: Session, new_user):
    df = fetch_user_data(db)

    compatible_users = check_compatibility(df, new_user, n_neighbors=100)

    top_matches = match_preferences(compatible_users, new_user, top_n=10)
    
    print("Total users fetched:", len(df))  # Print the count of users fetched
    # return top_matches[['userId', 'sizeTop', 'sizeBottom', 'age', 'weight', 'height', 'type', 'preferedColor']]
    matches = top_matches[['userId']]
    return matches  # Return only user IDs as an array

