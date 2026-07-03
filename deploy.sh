#!/bin/bash
# InfraBase Deployment Script
# Usage: ./deploy.sh <image-tag>

set -e

IMAGE_TAG=${1:-latest}
CONTAINER_NAME="infrabase-app"
PORT="5000"
OCIR_REPO="your-region.ocir.io/your-tenancy-namespace/infrabase"

echo "=== InfraBase Deployment ==="
echo "Pulling image: ${OCIR_REPO}:${IMAGE_TAG}"

docker pull "${OCIR_REPO}:${IMAGE_TAG}"

echo "Stopping existing container..."
docker stop "${CONTAINER_NAME}" 2>/dev/null || true
docker rm "${CONTAINER_NAME}" 2>/dev/null || true

echo "Starting new container..."
docker run -d \
    --name "${CONTAINER_NAME}" \
    --restart unless-stopped \
    -p "${PORT}:5000" \
    "${OCIR_REPO}:${IMAGE_TAG}"

echo "Cleaning up old images..."
docker image prune -f

echo "=== Deployment complete! ==="
echo "App running on port ${PORT}"