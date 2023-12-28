import numpy as np
from sklearn.preprocessing import MinMaxScaler
import torch
import pandas as pd

# Load the entire model
model = torch.load('./diabetes_model.pt')

# Set the model to evaluation mode
model.eval()

# Example input data
input_data = np.array([[0.8, 0.983, 0.89, 0.353, 0.0, 0.9, 0.734, 0.883]])

# Assuming you have a trained scaler, use it to scale the input data
train_data = pd.read_csv('./diabetes.csv')

# scaler = MinMaxScaler()
# scaler.fit(train_data.drop('Outcome', axis=1))
# scaled_input = scaler.transform(input_data)

# Convert the scaled input data to a PyTorch tensor
input_tensor = torch.tensor(input_data, dtype=torch.float32)

with torch.no_grad():  # Disable gradient calculation for inference
    output = model(input_tensor)
    print("Model output:", output)
