import numpy as np
from flask import Flask, request, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))

# Get the exact list of columns the model was trained on
MODEL_COLUMNS = list(model.feature_names_in_) 

# Dynamically figure out what your core columns are named in the model
# (Checks if they are named 'total_sqft' or 'sqft', 'bhk', 'bath', etc.)
sqft_col = next((col for col in MODEL_COLUMNS if 'sqft' in col.lower() or 'area' in col.lower()), None)
bhk_col = next((col for col in MODEL_COLUMNS if 'bhk' in col.lower() or 'bed' in col.lower()), None)
bath_col = next((col for col in MODEL_COLUMNS if 'bath' in col.lower()), None)

# Cleanly extract locations from the remaining columns
core_cols = {sqft_col, bhk_col, bath_col}
LOCATIONS = [col for col in MODEL_COLUMNS if col not in core_cols]

@app.route('/home')
def home():
    return render_template("index.html", locations=LOCATIONS, prediction_text="")

@app.route("/predict", methods=["POST"])
def predict():
    sqft = int(request.form['ulsqft']) 
    beds = int(request.form['ulbhk'])
    baths = int(request.form['ulbath'])
    selected = request.form['ullocation']

    # 1. Initialize the dictionary using ONLY the exact keys from MODEL_COLUMNS
    feature_dict = {col: 0 for col in MODEL_COLUMNS}
    
    # 2. Map values securely using the detected column keys
    if sqft_col: feature_dict[sqft_col] = sqft
    if bhk_col:  feature_dict[bhk_col] = beds
    if bath_col: feature_dict[bath_col] = baths

    # 3. Apply the location hot-encoding match
    if selected in feature_dict:
        feature_dict[selected] = 1
        
    # 4. Extract the values in the exact structural order of MODEL_COLUMNS
    features = np.array([list(feature_dict.values())])
    
    prediction = model.predict(features)
    output = round(prediction[0], 2)

    return render_template("index.html", locations=LOCATIONS, prediction_text=f"Estimated Price: {output} Lakhs")

if __name__ == '__main__':
    app.run(debug=True)