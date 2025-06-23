#!/bin/bash
# Should build/run the Pokemon REST API until manually stopped

echo "----------Building Pokemon API Docker image----------"
docker build -f docker/Dockerfile.api -t pokemon-api .
echo "Starting up the Pokemon REST API..."
echo "API will be available at http://localhost:5000"
echo "Press Ctrl+C to stop the server"

# Runs until manually stopped)
docker run --rm -p 5001:5000 --name pokemon-api-container pokemon-api