#!/bin/bash
export PYTHONPATH=$PYTHONPATH:.

echo "[1/4] Splitting data..."
python3 data/split_data.py

echo "[2/4] Training best model (Offline)..."
python3 offline_training/train_models.py

echo "[3/4] Starting Streaming Application..."
# Start in background; logs to streaming.log
python3 online_streaming/streaming_app.py > streaming.log 2>&1 &
APP_PID=$!
echo "Streaming app started with PID $APP_PID"

echo "[4/4] Starting Producer..."
python3 producer/producer.py

# Optional: To stop the streaming app later, use 'kill $APP_PID'
