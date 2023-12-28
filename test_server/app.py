from flask import Flask, jsonify, request
import glassboxx
import torch
from sklearn.preprocessing import MinMaxScaler
import traceback
import pandas as pd
import sys
import numpy as np

app = Flask(__name__)

print("PyTorch version:", torch.__version__)
print(sys.version)

# Load the model 
model = torch.load('/app/test_server/diabetes_model.pt')
print("Model Architecture:", model)
model.eval()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Initialize your MinMaxScaler
# Note: Ideally, you should fit this scaler to your training data or use the same parameters as used during training
scaler = MinMaxScaler()

# Load your training data or a representative subset to fit the scaler
# Replace 'diabetes.csv' with the path to your training data
train_data = pd.read_csv('/app/test_server/diabetes.csv')
scaler.fit(train_data.drop('Outcome', axis=1))

# initialize GlassBoxx SDK
glassboxx.init(
    app, 
    api_key="your_test_api_key", 
    db_string="postgresql://postgres:T5fkbECXseomHEz1@org-pegasus-ventures-inst-glassboxx.data-1.use1.tembo.io:5432/postgres", 
    ui_path='/custom-ui'
)

# test_input = torch.ones((1, 8), dtype=torch.float32).to(device)
# try:
#     test_output = model(test_input).detach().cpu().numpy()
#     print('Test Output:', test_output)
# except Exception as e:
#     print('Error with test input:', e)


# def background_task(func, *args, **kwargs):
#     thread = Thread(target=func, args=args, kwargs=kwargs)
#     thread.start()
#     return thread

@app.route('/run', methods=['POST'])
def run_model():
    try:
        # Example usage of GlassBoxx SDK
        # input_data = request.json
        input_data = [[0.8, 0.983, 0.89, 0.353, 0.0, 0.9, 0.734, 0.883]]
        # input_data = np.array([[0.8, 0.983, 0.89, 0.353, 0.0, 0.9, 0.734, 0.883]])


        # Here you can log inputs, log outputs, and use the 'explain' function
        glassboxx.log(input_data, 'Raw')
        print('Received input_data:', input_data)

        # Scale the input data
        # input_data_scaled = scaler.transform([input_data])
        input_data_scaled = scaler.transform(input_data)

        # Convert input data to PyTorch tensor
        input_tensor = torch.tensor(input_data_scaled, dtype=torch.float32).to(device)
        glassboxx.log(input_tensor, 'PyTorch Tensor')
        print('Transformed input_tensor:', input_tensor)
        print('input_tensor shape:', input_tensor.shape)
        print('input_tensor dtype:', input_tensor.dtype)

        # run an async explainer for the input instance
        # glassboxx.explain(model, processed_inputs, 'shap', feature_names)

        # run the model
        output = model(input_tensor).detach().cpu().numpy()
        glassboxx.log(output, 'output')
        print('Model output:', output)

        return jsonify({"output": output.tolist()})
    except Exception as e:
        print(f"Error running inference for Pytorch model: {e}")
        traceback.print_exc()  # Print the full traceback
        return jsonify({"error": str(e)}), 500

    # check for factual accuracy, content relavence, etc.
    # is async, so you can await or return output with no delay to review later 
    # glassboxx.validate(input, output)
    # background_task(glassboxx.validate, input_data, output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)


# the above is all for when a model is productionized. We need to test
# or validate the model in the dev environment to via test cases
# or check for labelling errors, bias, or whatever in the training data, also need to grab the training data to
# compare to data in production
# plus we can scan the model for harmfulness, hallucination, prompt injection, etc using openai
# generate test suites etc