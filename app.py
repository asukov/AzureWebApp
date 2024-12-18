from flask import Flask, request, render_template
from azure.storage.blob import BlobServiceClient
import os

app = Flask(__name__)

# Azure Blob Storage connection details
AZURE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=docintelstorage12345;AccountKey=2YcYFyBKqBs9S7ZsGodcuAS6S0pdn5QcJ4H3WV5xWAY46VlE2YYtlUy7cK6UVzoDQ9c50WpjC18G+AStgoNTng==;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "receipts"

# Initialize the BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file:
        try:
            # Create a blob client using the file name
            blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file.filename)

            # Upload the file to Azure Blob Storage
            blob_client.upload_blob(file, overwrite=True)

            return f"File {file.filename} uploaded successfully!"
        except Exception as e:
            return f"An error occurred: {str(e)}"

    return "Upload failed"

if __name__ == '__main__':
    app.run(debug=True)
