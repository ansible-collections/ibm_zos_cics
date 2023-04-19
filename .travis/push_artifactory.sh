#!/usr/bin/env bash

set -e

pip install https://github.com/ansible/ansible/archive/stable-2.14.tar.gz

ansible-galaxy collection build "$TRAVIS_BUILD_DIR" --force

file_with_prefix="$(find . -type f -iname "ibm-ibm_zos_cics-*")"
file="${file_with_prefix//.\//}"
no_extension="${file//.tar.gz/}"
no_starting="${no_extension//.\//}"
version_number="${no_starting//ibm-ibm_zos_cics-/}"
TRAVIS_NO_DOT="${TRAVIS_JOB_NUMBER//./D}"

echo ""
echo "##########################################################"
echo "############# Uploading build to Artifactory #############"
echo "##########################################################"
echo "#"
echo "# File:    $file"
echo "# Version: $version_number"
echo "#"
echo "##########################################################"

curl -ksSf \
    -H "Authorization: Bearer $ARTIFACTORY_TOKEN" -X PUT \
    -T "$TRAVIS_BUILD_DIR"/"$file" \
    "$ARTIFACTORY_URL"/"$version_number"/"$TRAVIS_NO_DOT"/"$file"
