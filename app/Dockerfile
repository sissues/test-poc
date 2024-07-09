# Use the official Python image from the Docker Hub
FROM python:3.8

# Set the working directory
WORKDIR /app

# Install pipenv
RUN pip install pipenv

# Copy the Pipfile and Pipfile.lock into the container
COPY src/Pipfile src/Pipfile.lock ./

# Install dependencies
RUN pipenv install --deploy --ignore-pipfile

# Copy the rest of the application code into the container
COPY src/ .

# Define the command to run the application
CMD ["pipenv", "run", "python", "api.py"]
