# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code
COPY . .

# Expose ports for Streamlit and FastAPI
EXPOSE 8501
EXPOSE 8502

# Copy the startup script and make it executable
COPY start.sh .
RUN chmod +x ./start.sh

# Run the startup script
CMD ["/app/start.sh"]