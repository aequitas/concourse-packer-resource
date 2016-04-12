#!/bin/sh

# fail if one command fails
set -e

# install requirements
pip --disable-pip-version-check freeze > installed.txt
pip --disable-pip-version-check install --no-cache-dir -r requirements_dev.txt
pip --disable-pip-version-check freeze > installed_dev.txt
comm -1 -3 installed.txt installed_dev.txt > uninstall.txt
