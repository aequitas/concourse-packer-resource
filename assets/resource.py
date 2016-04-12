#!/usr/bin/env python3

import json
import logging as log
import os
import sys
import tempfile
from distutils.version import LooseVersion


class Resource:
    """Base resource implementation."""

    def sort_versions(self, versions):
        """Sort versions using semver sorting."""
        return sorted(versions, key=lambda x: LooseVersion(x))

    def run(self, command_name, json_data=sys.stdin.read(), command_argument=sys.argv[1:]):
        """Parse input/arguments, perform requested command return output."""

        with tempfile.NamedTemporaryFile(delete=False, prefix=command_name + '-') as f:
            f.write(bytes(json_data, 'utf-8'))

        data = json.loads(json_data)

        # allow debug logging to console for tests
        if os.environ.get('RESOURCE_DEBUG', False) or data.get('source', {}).get('debug', False):
            log.basicConfig(level=log.DEBUG)
        else:
            logfile = tempfile.NamedTemporaryFile(delete=False, prefix='log')
            log.basicConfig(level=log.DEBUG, filename=logfile.name)
            stderr = log.StreamHandler()
            stderr.setLevel(log.INFO)
            log.getLogger().addHandler(stderr)

        log.debug('command: %s', command_name)
        log.debug('input: %s', data)
        log.debug('args: %s', command_argument)
        log.debug('environment: %s', os.environ)

        # combine source and params
        source = data.get('source', {})
        params = data.get('params', {})
        version = data.get('version', {})

        if command_name == 'check':
            response = self.check(source, version)
        elif command_name == 'in':
            response = self.in_cmd(command_argument[0], source, params, version)
        elif command_name == 'out':
            os.chdir(command_argument[0])
            response = self.out_cmd(source, params)
        else:
            raise Exception('invalid invocation')

        log.debug('response: %s', response)

        return json.dumps(response)
