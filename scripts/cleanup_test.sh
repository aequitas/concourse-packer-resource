#!/bin/sh

# fail if one command fails
set -e

# cleanup
pip --disable-pip-version-check uninstall -y -r uninstall.txt
rm -fr /tmp/* /opt/tests/
