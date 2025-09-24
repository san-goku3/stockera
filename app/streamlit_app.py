import streamlit as st
import requests
import numpy as np

# Title and Description
st.title("IPO Listing Gain Predictor")
st.write("Predict IPO listing gains based on financial and subscription metrics.")

# Input Fields: Collect 9 features for each time step
st.sidebar.header("Enter IPO Features for 10 Time Steps")

# Initialize a list to hold all the features for 10 time steps
features = []

for i in range(10):  # Sequence of 10 time steps
    st.sidebar.subheader(f"Time Step {i + 1}")
    
    # For each time step, gather 9 features
    time_step_features = [
        st.sidebar.number_input(f"Issue Price (t{i})", value=0.0, key=f"issue_price_{i}"),
        st.sidebar.number_input(f"Issue Size (t{i})", value=0.0, key=f"issue_size_{i}"),
        st.sidebar.number_input(f"HNI Subscription (t{i})", value=0.0, key=f"hni_subscription_{i}"),
        st.sidebar.number_input(f"NII Subscription (t{i})", value=0.0, key=f"nii_subscription_{i}"),
        st.sidebar.number_input(f"RII Subscription (t{i})", value=0.0, key=f"rii_subscription_{i}"),
        st.sidebar.number_input(f"Revenue (2 Years Ago) (t{i})", value=0.0, key=f"revenue_2_{i}"),
        st.sidebar.number_input(f"Revenue (1 Year Ago) (t{i})", value=0.0, key=f"revenue_1_{i}"),
        st.sidebar.number_input(f"EPS (2 Years Ago) (t{i})", value=0.0, key=f"eps_2_{i}"),
        st.sidebar.number_input(f"EPS (1 Year Ago) (t{i})", value=0.0, key=f"eps_1_{i}"),
    ]
    
    features.extend(time_step_features)

# Convert the list into a numpy array and reshape it to (10, 9)
features = np.array(features).reshape(10, 9)  # 10 time steps, 9 features per time step

# Now flatten the array to a 1D list with 90 features
features_flattened = features.flatten()

if st.button("Predict"):
    try:
        # Send Data to Flask API for prediction
        response = requests.post(
            "http://127.0.0.1:5000/predict",  # Ensure the Flask API is running locally
            json={"features": features_flattened.tolist()}  # Send as JSON (flattened list format)
        )

        if response.status_code == 200:
            result = response.json()
            st.success(f"Predicted Listing Gain: {result['listing_gain']:.2f}%")
        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error')}")
    except Exception as e:
        st.error(f"Connection Error: {e}")
