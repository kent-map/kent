#!/bin/bash

cd "$(dirname "$0")"
mkdir -p build
rsync -va Dockerfile build
rsync -va ../app.py build

docker build -t kent-webapp build
docker run -it -p 8080:8080 kent-webapp

rm -rf build