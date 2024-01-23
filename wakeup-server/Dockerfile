# Use an official Python runtime as the base image
FROM python:3.9.5-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

EXPOSE 5001

# Set the command to run the application
CMD [ "python", "run.py" ]
