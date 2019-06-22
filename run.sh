#!/bin/sh

docker run --rm -it \
    -v "$(pwd)/foo.log:/proj/foo.log" \
    -v "$(pwd)/src:/proj/src:ro" \
    pyrogue:latest \
    python /proj/src/main.py
