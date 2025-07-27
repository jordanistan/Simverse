# Use an official Python runtime as a parent image
# Stage 1: Build the React Frontend
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy package files and install dependencies
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install

# Copy the rest of the frontend source code
COPY frontend/ .

# Build the static assets
RUN npm run build

# Stage 2: Build the Python Backend
FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend source code
COPY *.py ./

# Copy the built frontend assets from the builder stage
COPY --from=frontend-builder /app/frontend/dist /app/static

# Copy the startup script and make it executable
COPY start.sh .
RUN chmod +x ./start.sh

# Expose the necessary port
EXPOSE 8502

# Run the start script
CMD ["./start.sh"]