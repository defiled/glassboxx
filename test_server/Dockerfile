# # Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container to /app
WORKDIR /app

# Copy the SDK and test_server contents into the container
COPY ./sdk /app/sdk
COPY ./test_server /app/test_server

# Install requirements and cache them on the host machine.
# No more wasting 5 mins installing tensorflow/pytorch if you dont want to.
RUN --mount=type=cache,target=/root/.cache/pip \
pip install -r /app/test_server/requirements.txt

# Make port 9000 available to the world outside this container
EXPOSE 9000

# Run app.py when the container launches
CMD ["python", "/app/test_server/app.py"]
# CMD ['pip3', "list"]
