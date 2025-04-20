# Image: python:3.13.3-slim-bullseye
# This Dockerfile is for a Python application that uses the FastAPI framework and requires specific system dependencies.
FROM python:3.13.3-slim-bullseye

# Set environment variables to prevent Python from writing .pyc files and to ensure output is flushed immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container to /app
# This is where the application code will be copied and run
# The WORKDIR instruction sets the working directory for any RUN, CMD, ENTRYPOINT, COPY, and ADD instructions that follow it in the Dockerfile
# If the directory does not exist, it will be created
WORKDIR /app    

# Install system dependencies
# The apt-get update command updates the package list for the apt package manager
# The apt-get install command installs the specified packages
# The --no-install-recommends option prevents the installation of recommended packages, which can help keep the image size smaller
# The apt-get clean command removes the local repository of retrieved package files, which helps reduce the image size
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    git \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .

# Install system dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory in the container
# The . represents the current directory on the host machine, and the second . represents the current directory in the container (which is /app)
COPY . .

# Expose port 8000 for the FastAPI application
# This allows the application to be accessible from outside the container on port 8000
EXPOSE 8000

# The CMD instruction specifies the command to run when the container starts
# In this case, it runs the FastAPI application using uvicorn
# The --host

CMD ["python", "main.py"]