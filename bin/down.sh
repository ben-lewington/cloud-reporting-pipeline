#!/usr/bin/env bash

if [ $# -le 0 ]; then
    echo "Usage: build.sh --offline [compose profile]"; exit 1
fi

set -xeo nounset
podman compose -f ./container/$1.yml down -v --remove-orphans
