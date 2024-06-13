#!/usr/bin/env bash
set -xeo nounset
podman compose -f ./container/dev.yml down -v --remove-orphans
podman compose -f ./container/dev.yml build
podman compose -f ./container/dev.yml up db
