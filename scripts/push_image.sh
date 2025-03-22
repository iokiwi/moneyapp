#!/usr/bin/env bash

# gcloud auth login
# gcloud auth configure-docker australia-southeast1-docker.pkg.dev

IMAGE_NAME=moneyapp-app:latest
REPOSITORY_NAME=simon-test
GCP_REGION=$(gcloud config get-value compute/region)

PROJECT_ID=$(gcloud config get-value project)
REPO_ROOT=$(git rev-parse --show-toplevel)

GCR_IMAGE="$GCP_REGION-docker.pkg.dev/$PROJECT_ID/$REPOSITORY_NAME/$IMAGE_NAME"

docker buildx build --platform linux/amd64 -t "$IMAGE_NAME" "$REPO_ROOT"
docker tag "$IMAGE_NAME" "$GCR_IMAGE"
docker push "$GCR_IMAGE"
