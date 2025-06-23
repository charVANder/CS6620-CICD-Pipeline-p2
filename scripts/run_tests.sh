#!/bin/bash
# Should build/run the Pokemon API tests
# Exits w/ 0 if tests pass, non-zero if tests fail

echo "----------Building the Test Pokemon API Docker image----------"
docker build -f docker/Dockerfile.tests -t pokemon-api-tests .
echo "Running tests..."

if docker run --rm pokemon-api-tests; then
    echo "All tests have passed! Exit code: 0"
    exit 0
else
    echo "Testing has failed! Exit code: non-zero"
    exit 1
fi