#!/bin/sh

# fail if one command fails
set -e

# shell tests
for test in /opt/tests/*/test.sh;do
    log=$(mktemp /tmp/test-log.XXXXXX)

    echo running "$test"
    if ! "$test" 2>"$log";then
        cat "$log" 1>&2
        exit 1
    fi
done

# python tests
pylama /opt/resource /opt/tests/
export PATH=/opt/tests/mock/:$PATH
export RESOURCE_DEBUG=true
py.test -l --tb=short -r fE /opt/tests
