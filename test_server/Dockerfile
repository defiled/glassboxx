# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container to /app
WORKDIR /app

# Copy the SDK and test_server contents into the container
COPY ./sdk /app/sdk
COPY ./test_server /app/test_server

# Install the dependencies
RUN pip install --no-cache-dir -r /app/test_server/requirements.txt

# Make port 9000 available to the world outside this container
EXPOSE 9000

# Run app.py when the container launches
CMD ["python", "/app/test_server/app.py"]
