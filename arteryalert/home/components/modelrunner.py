import os
import pickle
import json
import numpy as np
import pandas as pd
from django.http import JsonResponse
from sklearn.preprocessing import OneHotEncoder

STATIC_DIR = os.getcwd() + '/home/notebooks/'
MODEL_FILE = 'heart_disease_model.pkl'
DATASET_FILE = 'heart.csv'

def predict(rowdata):
    # Load the pre-trained model
    with open(STATIC_DIR + MODEL_FILE, 'rb') as model_file:
        loaded_model = pickle.load(model_file)

    # Load the dataset "heart.csv" to get the original category mappings
    dataset_path = os.path.join(STATIC_DIR, DATASET_FILE)
    df = pd.read_csv(dataset_path)

    # Define categorical and numerical columns
    categorical_cols = ['Sex', 'ChestPainType', 'FastingBS', 'RestingECG', 'ExerciseAngina', 'ST_Slope']
    numerical_cols = ['Age', 'RestingBP', 'Cholesterol', 'MaxHR', 'Oldpeak']

    # Handle user input
    user_input_dict = json.loads(rowdata)

    # Remove fields that are not used for the classification
    user_input_dict.pop('email', None)
    user_input_dict.pop('csrfmiddlewaretoken', None)

    # Transform input data (which is all strings) to the right numerical format
    for key in numerical_cols:
        user_input_dict[key] = int(user_input_dict[key])
    user_input_dict['FastingBS'] = int(user_input_dict['FastingBS'])

    # Perform the same preprocessing as the jupyter notebook, but adding our input row into the X dataframe to preprocess it the same way
    X = df.drop('HeartDisease', axis=1)
    y = df['HeartDisease']

    X.loc[len(X)] = user_input_dict # Append the user data to the dataset

    encoder = OneHotEncoder(drop='first', sparse=False)
    X_encoded = encoder.fit_transform(X[categorical_cols])
    X_processed = np.hstack((X_encoded, X[numerical_cols]))

    # Take the user input out of the X dataframe
    user_input_processed = X_processed[-1]
    user_input_processed = user_input_processed.reshape(1, -1)

    # Use the pre-trained model to make predictions
    prediction = loaded_model.predict(user_input_processed)

    # Use the pre-trained model to get class probabilities
    class_probabilities = loaded_model.predict_proba(user_input_processed)

    # Extract the probability of the positive class (class 1)
    positive_class_probability = class_probabilities[:, 1].tolist()

    # Return the prediction and probability as a JSON response
    return JsonResponse({'prediction': prediction.tolist(), 'probability': positive_class_probability})
