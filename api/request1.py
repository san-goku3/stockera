import requests
import numpy as np

# Define the API endpoint
url = "http://127.0.0.1:5000/predict"

# Example input data (for one company, 10 time steps, 9 features each)
company_data = [
    [150, 200, 1.2, 0.8, 1.5, 500000, 550000, 15, 12],  # Time Step 1
    [160, 210, 1.3, 0.9, 1.6, 510000, 560000, 16, 13],  # Time Step 2
    [170, 220, 1.4, 1.0, 1.7, 520000, 570000, 17, 14],  # Time Step 3
    [180, 230, 1.5, 1.1, 1.8, 530000, 580000, 18, 15],  # Time Step 4
    [190, 240, 1.6, 1.2, 1.9, 540000, 590000, 19, 16],  # Time Step 5
    [200, 250, 1.7, 1.3, 2.0, 550000, 600000, 20, 17],  # Time Step 6
    [210, 260, 1.8, 1.4, 2.1, 560000, 610000, 21, 18],  # Time Step 7
    [220, 270, 1.9, 1.5, 2.2, 570000, 620000, 22, 19],  # Time Step 8
    [230, 280, 2.0, 1.6, 2.3, 580000, 630000, 23, 20],  # Time Step 9
    [240, 290, 2.1, 1.7, 2.4, 590000, 640000, 24, 21],  # Time Step 10
]

# Convert company data into a numpy array
company_data_np = np.array(company_data)

# Check the shape of the data before reshaping
print("Original Shape:", company_data_np.shape)

# Reshaping data to fit the model input (1 batch, 10 time steps, 9 features)
reshaped_data = company_data_np.reshape(1, 10, 9)

# Check the reshaped data
print("Reshaped Shape:", reshaped_data.shape)

# Prepare the JSON payload
payload = {"companies": reshaped_data.tolist()}

# Send POST request
response = requests.post(url, json=payload)

# Display the result
if response.status_code == 200:
    print("Predicted Listing Gains:", response.json().get("listing_gains"))
else:
    print("Error:", response.json().get("error", "Unknown error"))
