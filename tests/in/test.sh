#!/bin/sh

set -xe

# inject awscli mock
export PATH="$(dirname $0):$PATH"
export DEBUG=1

input='{"version":{"ImageId": "ami-0123456"}}'

mkdir -p /tmp/build/get

output=$(echo $input | /opt/resource/in /tmp/build/get)

test -f /tmp/build/get/id

grep "ami-0123456" /tmp/build/get/id 1>&2

echo $output | jq -er '.version.ImageId == "ami-0123456"'

# test metadata output
echo $output | jq -er '.metadata|map({"key":.name, "value":.value})|from_entries|.Name == "test"'
