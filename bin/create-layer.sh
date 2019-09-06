#!/bin/bash

# Run this from within the docker container to create your own updated boto3 Lambda Layer
#
#   root@9efa63288830:/code# ./bin/create-layer.sh
#
# Thanks to Jeremy Turner for most of this
#
if ! [ -x "$(command -v zip)" ]; then
  echo 'Error: zip is not installed....installing' >&2
  apt-get install -y zip
fi

mkdir -p build/python && cd build/python

python3 -m pip install boto3 --target .

# Clean out things we don't need
find . -name __pycache__ | xargs rm -rf
find . -name 's3transfer*' | xargs rm -rf

echo "Zipping...."
cd ..
zip -r9 ../boto3-botocore.zip .

echo 'Publishing layer...'
aws lambda publish-layer-version --layer-name boto3-botocore \
  --description "updated boto3, botocore, and requests package" \
  --zip-file fileb://../boto3-botocore.zip \
  --compatible-runtimes python3.6
