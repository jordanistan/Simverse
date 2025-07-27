#!/bin/sh
uvicorn echopulse:app --host 0.0.0.0 --port 8502 &
streamlit run ui.py --server.port 8501 --server.address 0.0.0.0
