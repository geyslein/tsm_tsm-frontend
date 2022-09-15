#!/usr/bin/env bash
set -e
DIR_SCRIPT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#
# Customize Image/Tag here
#
IMAGE_NAME="git.ufz.de:4567/rdm-software/timeseries-management/tsm-frontend/app:0.0.1"

#
# Build
#
docker build -t "${IMAGE_NAME}" "${DIR_SCRIPT}/"

#
# Push
#
echo
echo "Image in die Registry pushen? [y|N]"
echo "-> ${IMAGE_NAME}"
read -n 1 YESNO
if [ "${YESNO}" == "y" ]; then
    docker push "${IMAGE_NAME}"
fi
