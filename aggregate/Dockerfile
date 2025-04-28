FROM python:3.9-alpine

# Set environment variables to prevent Python from writing .pyc files and buffering output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apk update && apk add --no-cache gcc musl-dev libffi-dev

# Copy requirements file and install Python dependencies
COPY requirements.pip /app/requirements.pip
RUN pip install --no-cache-dir -r /app/requirements.pip

# Copy application source code
COPY src /app/src

# Set the working directory
WORKDIR /app/src

# Expose the application port
EXPOSE 5000

# Command to run the application
CMD ["python3", "run.py"]
