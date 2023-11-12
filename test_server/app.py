from flask import Flask, jsonify
import glassboxx
import os

app = Flask(__name__)

# Initialize the GlassBoxx SDK
glassboxx.init(app, api_key="your_test_api_key", db_string="your_db_connection_string", ui_path='/glassboxx')

# Define the path to the static files relative to the location of glassboxx package
static_files_path = os.path.dirname(glassboxx.__file__)

# Log the contents of the glassboxx package
print(f"Contents of GlassBoxx directory: {os.listdir(static_files_path)}")

@app.route('/test')
def test_endpoint():
    # Example usage of your SDK
    # Here you can log inputs, log outputs, and use the 'explain' function
    # Use the example AI model to generate some data
    response = {
        "message": "Test endpoint working",
        "log": "Example log data",
        "output": "Example output data"
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)