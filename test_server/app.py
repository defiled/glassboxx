from flask import Flask, jsonify, request
import glassboxx
import torch

app = Flask(__name__)

# Define a global variable for the model
model = None

def load_model():
    global model
    model_path = '/app/diabetesAI.pt'
    model = torch.load(model_path)
    model.eval()

def background_task(func, *args, **kwargs):
    thread = Thread(target=func, args=args, kwargs=kwargs)
    thread.start()
    return thread

@app.on_event("startup")
def startup():
    # Load the model and initialize GlassBoxx SDK
    load_model()
    # Initialize the GlassBoxx SDK
    glassboxx.init(app, 
                api_key="your_test_api_key", 
                db_string="your_db_string", 
                ui_path='/custom-ui'
                )

@app.route('/test')
def test_endpoint():
    response = {
        "message": "Test endpoint working",
        "log": "Example log data",
        "output": "Example output data"
    }
    return jsonify(response)

@app.route('/run', methods=['POST'])
def run_model():
    input_data = request.json
    # Example usage of GlassBoxx SDK

    # Here you can log inputs, log outputs, and use the 'explain' function
    glassboxx.log(input_data, 'Raw')

    # Convert input data to PyTorch tensor
    input_tensor = torch.tensor([input_data], dtype=torch.float32)
    glassboxx.log(input_tensor, 'PyTorch Tensor')

    # run an async explainer for the input instance
    # glassboxx.explain(model, processed_inputs, 'shap', feature_names)

    # Assuming input_data is processed and ready to be fed into the model
    with torch.no_grad():  # Ensure torch is in inference mode
        output = model(input_data)  # Adjust based on how your model expects input
    
    glassboxx.log(output, 'output')

    # check for factual accuracy, content relavence, etc.
    # is async, so you can await or return output with no delay to review later 
    # glassboxx.validate(input, output)
    # background_task(glassboxx.validate, input_data, output)

    return jsonify({"output": output.tolist()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)



# the above is all for when a model is productionized. We need to test
# or validate the model in the dev environment to via test cases
# or check for labelling errors, bias, or whatever in the training data, also need to grab the training data to
# compare to data in production
# plus we can scan the model for harmfulness, hallucination, prompt injection, etc using openai
# generate test suites etc
#
#