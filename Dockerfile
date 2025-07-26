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

# Create and make the startup script executable
RUN echo '#!/bin/sh' > start.sh && \
    echo 'uvicorn echopulse:app --host 0.0.0.0 --port 8502 &' >> start.sh && \
    echo 'streamlit run ui.py --server.port 8501 --server.address 0.0.0.0' >> start.sh && \
    chmod +x start.sh

# Run the startup script
CMD ["./start.sh"]