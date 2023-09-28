import pickle
import os


STATIC_DIR = os.getcwd() + '/home/notebooks/'
MODEL_FILE = 'example_classifier_model.pkl'

def predict(rowdata):
    # Import model if it exists
    if os.path.exists(STATIC_DIR + MODEL_FILE):
        model = pickle.load(open(STATIC_DIR + MODEL_FILE, 'rb'))
        print("Model imported")
    else:
        print("No model in static directory")



    # Perform normalization on the rowdata (so that it can be used)



    # Return the prediction
    if rowdata['sex'] == "M":  # temporary example to see if outputting result works, if you inputted male then the result is "you have heart problems"
        return 1 
    else:
        return 0