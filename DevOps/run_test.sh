#!/bin/bash

# Check if container is running
if docker ps | grep -q test_hello; then
    echo "Container is running"
else
    echo "Container is not running"
    exit 1
fi

# Test connectivity (replace with the correct hostname and port)
curl -s http://test_hello:80 && echo "Service is reachable" || echo "Service is unreachable"
