#!/bin/bash

GCP_PROJECT='visual-essays'

GCR_SERVICE=${1:-kent}
MIN_INSTANCE_LIMIT=0

gcloud config configurations activate visual-essays
gcloud config set project ${GCP_PROJECT}
gcloud config set compute/region us-central1
gcloud config set run/region us-central1

cd "$(dirname "$0")"
mkdir -p build
cd build
rsync -va ../Dockerfile ../../main.py ../../creds.yaml .

gcloud builds submit --tag gcr.io/${GCP_PROJECT}/${GCR_SERVICE}

gcloud beta run deploy ${GCR_SERVICE} \
    --image gcr.io/${GCP_PROJECT}/${GCR_SERVICE} \
    --min-instances ${MIN_INSTANCE_LIMIT} \
    --allow-unauthenticated \
    --platform managed \
    --memory 1Gi

cd ..
rm -rf build