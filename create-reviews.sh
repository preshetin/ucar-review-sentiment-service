#!/bin/bash

API_URL="http://127.0.0.1:8000/reviews"

while IFS= read -r review
do
  curl -s -X POST "$API_URL" \
    -H "Content-Type: application/json" \
    -d "{\"text\": \"$review\"}"
  echo
done < example-reviews.txt