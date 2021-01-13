#!/usr/bin/env bash

TAG=0.0.1
MODTAG=$(echo "$TAG" | sed -e 's/\W/-/g')
echo $MODTAG
