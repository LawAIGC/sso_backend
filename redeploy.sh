#!/bin/bash

# Stop and remove existing container if it exists
docker stop sso-backend 2>/dev/null
docker rm sso-backend 2>/dev/null

# Build new docker image
docker build -t sso-backend .

# Run new container
docker run -d -p 9001:9001 --name sso-backend sso-backend