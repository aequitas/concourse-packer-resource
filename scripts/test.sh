#!/bin/sh

# fail if one command fails
set -e

# test
pylama /opt/resource /opt/tests/
export PATH=/opt/tests/mock/:$PATH
py.test -l --tb=short -r fE /opt/tests
