#!/bin/bash

PR_NUMBER=$1
REPO=$2
LABELS=$3
TOKEN=$4

curl -L -X POST -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json" https://api.github.com/repos/$REPO/issues/$PR_NUMBER/labels -d "{\"labels\":[\"$LABELS\"]}"
