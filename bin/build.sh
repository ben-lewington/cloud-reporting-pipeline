#!/usr/bin/env bash

if [ $# -le 0 ]; then
    echo "Usage: build.sh [compose profile]"
    exit 1
fi


docker="docker compose -f ./docker/$1.yml"

set -xeo nounset

$docker rm -sfv
$docker build

case "$1" in
    "dev")
        $docker run --rm --no-deps $1 /bin/bash
        ;;
    "deploy")
        if [ $# -le 1 ]; then
            echo "Usage: build.sh [compose profile] [entrypoint script name]"
            exit 1
        fi
        $docker run --rm --no-deps $1 $2
        ;;
esac
