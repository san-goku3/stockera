#cd majrpoj/app
#venv for this is ipo_env
#streamlit run streamlit_app1.py
import streamlit as st
import requests
import numpy as np

# Define API URL
api_url = "http://127.0.0.1:5000/predict"  # Update if different

def get_predictions(companies_data):
    payload = {"companies": companies_data}
    response = requests.post(api_url, json=payload)
    
    if response.status_code == 200:
        return response.json()["listing_gains"]
    else:
        return response.json().get("error", "Error occurred")

def main():
    st.title("IPO Listing Gain Prediction")

    # Input for company data (9 features per company)
    companies_data = []
    num_companies = st.number_input("Enter the number of companies", min_value=1, max_value=10, value=1)
    
    for i in range(num_companies):
        st.write(f"Company {i + 1}")
        features = []
        for j in range(9):  # 9 features for each company
            # Pass a unique key for each input field to avoid duplicate IDs
            feature_value = st.number_input(f"Feature {j + 1}", min_value=0.0, value=0.0, key=f"company_{i}_feature_{j}")
            features.append(feature_value)
        companies_data.append(features)
    
    if st.button("Predict"):
        if companies_data:
            st.write("Sending data to model for prediction...")
            predictions = get_predictions(companies_data)
            
            if isinstance(predictions, list):
                for i, prediction in enumerate(predictions):
                    st.write(f"Predicted Listing Gain for Company {i + 1}: {prediction:.2f}%")
            else:
                st.write(f"Error: {predictions}")
        else:
            st.write("Please provide data for at least one company.")

if __name__ == "__main__":
    main()
