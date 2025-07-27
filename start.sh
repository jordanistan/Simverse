#!/bin/sh

# Start the FastAPI server
# It serves both the API and the static frontend files
uvicorn echopulse:app --host 0.0.0.0 --port 8502
