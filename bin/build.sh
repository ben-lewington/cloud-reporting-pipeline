#!/usr/bin/env bash

if [ $# -le 0 ] || ([ $# -le 1 ] && [ "$1" == "--offline" ]); then
    echo "Usage: build.sh < --offline > [compose profile]"; exit 1; fi

build_flags="--pull"
if [ "$1" == "--offline" ]; then
    build_flags= ; shift; fi

down_flags="-v --remove-orphans"
run_flags="--rm --no-deps"

compose="podman compose -f ./container/$1.yml"

set -xeo nounset

$compose down $down_flags
$compose build $build_flags

$compose up -d
case "$1" in
    "base")
        $compose run $run_flags --entrypoint=/bin/bash python-uv
        ;;
    "dev")
        $compose run $run_flags migrator
        $compose run $run_flags --entrypoint=/bin/bash reports
        ;;
    "deploy")
        if [ $# -le 1 ]; then
            echo "Usage: build.sh [compose profile] [entrypoint script name]"; exit 1
        fi
        $compose run $run_flags $1 $2
        ;;
    *)
        echo "unknown stack file name \"$1\""; exit 1
        ;;
esac
