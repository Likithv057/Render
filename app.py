from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)

# Loading model, encoders, and scaler
model = joblib.load('rf_rent_model.pkl')
encoders = joblib.load('encoders.pkl')
scaler = joblib.load('scaler.pkl')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Input data from form
        data = request.form
        bhk = int(data['bhk'])
        size = float(data['size'])
        floor = int(data['floor'])
        area_type = data['area_type']
        furnish_status = data['furnishing_status']
        tenant_pref = data['tenant_preferred']
        bathroom = int(data['bathroom'])
        contact = data['point_of_contact']

        # Encode categorical variables
        area_type = encoders['Area Type'].transform([area_type])[0]
        furnish_status = encoders['Furnishing Status'].transform([furnish_status])[0]
        tenant_pref = encoders['Tenant Preferred'].transform([tenant_pref])[0]
        contact = encoders['Point of Contact'].transform([contact])[0]

        # Prepare input DataFrame
        input_data = pd.DataFrame({
            'BHK': [bhk],
            'Size': [size],
            'Floor': [floor],
            'Area Type': [area_type],
            'Furnishing Status': [furnish_status],
            'Tenant Preferred': [tenant_pref],
            'Bathroom': [bathroom],
            'Point of Contact': [contact]
        })

        # Scale the input data
        input_scaled = scaler.transform(input_data)
        
        # Predict rent
        rent_log = model.predict(input_scaled)
        predicted_rent = np.expm1(rent_log)[0]  # Get the predicted value

        # Return the predicted rent as JSON
        return jsonify({'predicted_rent': round(predicted_rent, 2)})

    return render_template('index.html', predicted_rent=0)

@app.route('/analysis', methods=['GET'])
def analysis():
    return render_template('graphs.html')

if __name__ == '__main__':
    app.run(debug=True)
