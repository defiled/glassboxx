import os
from flask import Flask, send_from_directory
import requests
from .logger import log
from .explainer import explain
from .database import init_db
from .config import get_config

def init(app, api_key, db_string=None, ui_path='/glassboxx'):
    """
    Initializes the SDK with the given configuration.
    """
    _config = get_config()
    _config['api_key'] = api_key
    _config['db_string'] = db_string
    _config['ui_endpoint'] = ui_path
    _config['db_connection'] = init_db(db_string)

    serve_ui(app, _config['ui_endpoint'])


def serve_ui(app, ui_endpoint):
    """
    Configures the user's app to serve the GlassBoxx UI at the specified endpoint.
    
    :param app: The user's app instance.
    :param ui_endpoint: The endpoint at which to serve the GlassBoxx UI.

    NOTE: might want to make this public and allow users to opt into this at somepoint
    """

    # Define the path to the static files relative to the location of __init__.py
    static_files_path = os.path.join(os.path.dirname(__file__), 'build')

    # Print the current working directory
    current_dir = os.getcwd()
    print(f"Current working directory: {current_dir}")
    
    # Print the contents of the build directory
    if os.path.exists(static_files_path):
        print(f"Contents of GlassBoxx build directory: {os.listdir(static_files_path)}")
    else:
        print(f"GlassBoxx build directory not found at: {static_files_path}")

    print(f"also heres the raw files:  {os.listdir(os.path.dirname(__file__))}")

    # Set up the GlassBoxx UI route on the user's app
    # TODO: The best solution is to download these static files from a CDN upon __init__
    # TODO: Don't want to have to import the specific framework to check if instance of, better way
    if isinstance(app, Flask):
        print('Flask app detected!!!!')
        # Flask app
        @app.route(ui_endpoint)
        def serve_glassboxx_ui():
            """
            Serve the main index.html for the GlassBoxx UI.
            """
            return send_from_directory(static_files_path, 'index.html')

        # Serve JS and CSS files
        @app.route('/static/js/<path:filename>')
        def serve_js(filename):
            return send_from_directory(static_files_path + '/static/js', filename)

        @app.route('/static/css/<path:filename>')
        def serve_css(filename):
            return send_from_directory(static_files_path + '/static/css', filename)
        
        # Serve media files
        @app.route('/static/media/<path:filename>')
        def serve_media(filename):
            media_folder = os.path.join(static_files_path, 'static', 'media')
            return send_from_directory(media_folder, filename)
    elif hasattr(app, 'django'):
        # Django app
        # @TODO: Add similar code to integrate with Django's static file serving mechanism
        pass
    # Add more conditional branches for other types of frameworks like FastAPI

# Provide a function to get the UI path to allow the host web server to serve the glassboxx UI
def get_ui_path():
    """
    Returns the UI path where glassboxx UI should be served.
    """
    return get_config('ui_endpoint')

def download_file_from_cdn(url, local_path):
    """
    Helper function to download a single file from the CDN.
    """
    response = requests.get(url)
    response.raise_for_status()  # Ensure we got a successful response

    os.makedirs(os.path.dirname(local_path), exist_ok=True)  # Create directories if not exist
    with open(local_path, 'wb') as file:
        file.write(response.content)

def download_all_files_from_cdn(cdn_manifest_url, local_dir):
    """
    Download all files listed in the CDN manifest to a local directory.
    """
    cdn_base_url = 'https://my.cdn.provider/path/to/files'
    # cdn_manifest_url = f"{cdn_base_url}/manifest.txt"  # URL to manifest file on CDN

    # Download the manifest file containing the list of files
    manifest_response = requests.get(cdn_manifest_url)
    manifest_response.raise_for_status()
    
    # Assume the manifest is a simple text file with one CDN file path per line
    for file_path in manifest_response.text.splitlines():
        # Construct the full URL for each file
        cdn_file_url = f"{cdn_base_url}/{file_path.strip()}"
        # Define the local file path
        local_file_path = os.path.join(local_dir, file_path.strip())
        
        # Download the file from CDN
        download_file_from_cdn(cdn_file_url, local_file_path)

    print(f"Downloaded all files from CDN to {local_dir}")

__all__ = ['init', 'get_ui_path', 'log', 'explain']
