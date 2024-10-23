import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.compose import ColumnTransformer
from sklearn.metrics import pairwise_distances

# Load dataset from CSV
def load_data(csv_file):
    return pd.read_csv(csv_file)

# Preprocessing pipeline for compatibility (size, age, weight, height)
def compatibility_pipeline():
    categorical_features = ['Size_Top', 'Size_Bottom']
    numerical_features = ['Age', 'Weight', 'Height']  # Added 'Height' as a numerical feature

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(), categorical_features),
            ('num', StandardScaler(), numerical_features)
        ])

    return preprocessor

# Preprocessing pipeline for preferences (style, colors)
def preference_pipeline():
    categorical_features = ['Style_Preference', 'Preferred_Colors']

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(), categorical_features)
        ])

    return preprocessor

# Function to check compatibility based on size, age, weight, height
def check_compatibility(df, new_user, n_neighbors=50):
    preprocessor = compatibility_pipeline()
    
    X = df[['Size_Top', 'Size_Bottom', 'Age', 'Weight', 'Height']]
    
    transformed_data = preprocessor.fit_transform(X)
    new_user_data = pd.DataFrame([new_user])[['Size_Top', 'Size_Bottom', 'Age', 'Weight', 'Height']]
    transformed_new_user = preprocessor.transform(new_user_data)
    
    knn = NearestNeighbors(n_neighbors=n_neighbors, metric='euclidean')
    knn.fit(transformed_data)
    
    distances, indices = knn.kneighbors(transformed_new_user)
    compatible_users = df.iloc[indices[0]]
    
    return compatible_users

# Function to match based on style and color preference
def match_preferences(compatible_users, new_user, top_n=10):
    preprocessor = preference_pipeline()

    X = compatible_users[['Style_Preference', 'Preferred_Colors']]
    transformed_data = preprocessor.fit_transform(X)
    
    new_user_data = pd.DataFrame([new_user])[['Style_Preference', 'Preferred_Colors']]
    transformed_new_user = preprocessor.transform(new_user_data)
    
    distances = pairwise_distances(transformed_new_user, transformed_data, metric='cosine')[0]
    
    compatible_users['Distance'] = distances
    top_matches = compatible_users.sort_values(by='Distance').head(top_n)
    
    return top_matches

# Main function to find top 10 matches
def find_best_matches(csv_file, new_user):
    df = load_data(csv_file)

    compatible_users = check_compatibility(df, new_user, n_neighbors=100)

    top_matches = match_preferences(compatible_users, new_user, top_n=10)
    
    return top_matches[['User_ID', 'Size_Top', 'Size_Bottom', 'Age', 'Weight', 'Height', 'Style_Preference', 'Preferred_Colors']]
