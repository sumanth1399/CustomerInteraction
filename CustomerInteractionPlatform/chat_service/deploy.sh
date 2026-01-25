#!/bin/bash

# Set your Firebase/GCP project ID
PROJECT_ID="customerinteraction"

# Set the region (us-central1, us-east1, etc.)
REGION="us-central1"

# Set the service name
SERVICE_NAME="chat_service"

echo "Building and deploying $SERVICE_NAME to Cloud Run..."

# Set the project
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com

# Navigate to chat-service directory
cd "$(dirname "$0")"

# Build and deploy using Cloud Build
gcloud builds submit --config cloudbuild.yaml

echo "Deployment complete!"
echo "Service URL will be shown after deployment"