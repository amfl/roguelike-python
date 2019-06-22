#!/bin/sh
# Mounts a fresh copy of the source code and starts an ephemeral container.
# Logs are captured so you can review them at your leisure.

docker run --rm -it \
    -v "$(pwd)/foo.log:/proj/foo.log" \
    -v "$(pwd)/src:/proj/src:ro" \
    -e "TERM=${TERM}" \
    pyrogue:latest \
    python /proj/src/main.py
