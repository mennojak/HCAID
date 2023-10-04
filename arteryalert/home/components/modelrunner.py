import os
import pickle
import json
import numpy as np
import pandas as pd
from django.http import JsonResponse
from sklearn.preprocessing import OneHotEncoder

STATIC_DIR = os.getcwd() + '/home/notebooks/'
MODEL_FILE = 'heart_disease_model.pkl'
NORM_FILE = 'normalization_stats.pkl'

def predict(rowdata):
    # Load the pre-trained model
    with open(STATIC_DIR + MODEL_FILE, 'rb') as model_file:
        loaded_model = pickle.load(model_file)

    # Handle user input
    user_input_dict = json.loads(rowdata)

    # Remove fields that are not used for the classification
    user_input_dict.pop('email', None)
    user_input_dict.pop('csrfmiddlewaretoken', None)

    # Define categorical columns for feature encoding
    categorical_cols = ['Sex', 'ChestPainType', 'FastingBS', 'RestingECG', 'ExerciseAngina', 'ST_Slope']

    # Define numerical columns for feature scaling
    numerical_cols = ['Age', 'RestingBP', 'Cholesterol', 'MaxHR', 'Oldpeak']

    # Preprocess the data
    preprocessed_data = preprocess_user_input(user_input_dict, categorical_cols, numerical_cols)
    print(preprocessed_data.values)

    # Use the pre-trained model to make predictions
    prediction = loaded_model.predict(preprocessed_data)

    # Use the pre-trained model to get class probabilities
    class_probabilities = loaded_model.predict_proba(preprocessed_data)

    # Extract the probability of the positive class (class 1)
    positive_class_probability = class_probabilities[:, 1].tolist()

    print(prediction, class_probabilities, positive_class_probability)
    # Return the prediction and probability as a JSON response
    return JsonResponse({'prediction': prediction.tolist(), 'probability': positive_class_probability})


def preprocess_user_input(user_input_dict, categorical_cols, numerical_cols):
    # Create a DataFrame from user input
    user_input_df = pd.DataFrame(user_input_dict, index=[0])

    # Convert numerical columns to numeric types (in case some values are still strings)
    for col in numerical_cols:
        user_input_df[col] = pd.to_numeric(user_input_df[col], errors='coerce')

    # Label Encoding for Categorical Columns
    from sklearn.preprocessing import LabelEncoder

    label_encoder = LabelEncoder()
    for col in categorical_cols:
        user_input_df[col] = label_encoder.fit_transform(user_input_df[col])

    # Load normalization statistics
    with open(STATIC_DIR + NORM_FILE, 'rb') as norm_file:
        normalization_stats = pickle.load(norm_file)

    # Feature Scaling
    numerical_data = user_input_df[numerical_cols]
    mean = normalization_stats['mean']
    std = normalization_stats['std']
    normalized_data = (numerical_data - mean) / std

    # Combine encoded and scaled numerical data
    preprocessed_data = pd.concat([user_input_df.drop(numerical_cols, axis=1), normalized_data], axis=1)

    return preprocessed_data