#!/bin/bash
docker build -t stegno4 .
docker run -d -p 9304:9304 stegno4
