#Deriving the latest base image
FROM python:latest

# Set the working directory inside the container
#WORKDIR /app

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .
COPY sub2.py .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables if needed
# ENV MY_ENV_VARIABLE=value

# Specify the command to run on container start
CMD ["python3", "sub2.py"]
