#!/bin/bash

image=$1

data=$(base64 "$image")

echo '{"data": "'$data'"}' > payload.json

response=$(curl -s -X POST http://localhost:5000/v1/images/ -d @payload.json -H 'Content-Type: application/json')

echo $response