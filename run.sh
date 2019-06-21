#!/bin/sh

docker run --rm -it -v $(pwd)/src:/proj/src:ro pyrogue:latest python /proj/src/main.py
