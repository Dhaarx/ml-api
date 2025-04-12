import pickle
from flask import Flask,request,jsonify
import warnings
import os
from flask_cors import CORS
warnings.filterwarnings('ignore')

app = Flask(__name__)
CORS(app)

# Load model and encoders
model = pickle.load(open('fertilizer_model.pkl', 'rb'))
le_soil = pickle.load(open('soil_encoder.pkl', 'rb'))
le_crop = pickle.load(open('crop_encoder.pkl', 'rb'))
le_ferti = pickle.load(open('fertilizer_encoder.pkl', 'rb'))


@app.route('/')
def home():
    return "Welcome to the Fertilizer Prediction API!"

@app.route('/favicon.ico')
def favicon():
    return '', 204  # No content for favicon

@app.route('/predict',methods=['POST'])
def predict_fertilizer():
    data=request.get_json()

    soil=data.get('soil')
    crop=data.get('crop')

    try:
        soil_encode=le_soil.transform([soil])[0]
        crop_encode=le_crop.transform([crop])[0]
    except ValueError:
        return jsonify({'error':'Invalid soil or crop name'}),400
    
    pred_encoded=model.predict([[soil_encode,crop_encode]])[0]
    predicted_fertilizer=le_ferti.inverse_transform([pred_encoded])[0]

    print(predicted_fertilizer)
    return jsonify({'fertilizer': predicted_fertilizer})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  
    app.run(host='0.0.0.0', port=port)


