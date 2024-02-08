# Use an official Python runtime as the base image
FROM python:3.9.5-slim-buster

RUN apt-get update && apt-get install -y sqlite3
# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY ./wakeup-server/requirements.txt .
COPY ./zeromq /app/zeromq
RUN pip install /app/zeromq

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY ./wakeup-server .

RUN test -f /app/wakeup.db && rm /app/wakeup.db || echo "no db file found"

EXPOSE 5001

# Set the command to run the application
CMD [ "python", "run.py" ]
