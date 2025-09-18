#!/bin/bash

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.

set -e

SYNAP_VERSION="0.9.0"
SYNAP_RELEASE="stable"
HOST_ARCH=$(uname -m)
PLAT_TAG="manylinux_2_35"
PYTHON_MAJOR=$(python -c 'import sys; print(sys.version_info.major)')
PYTHON_MINOR=$(python -c 'import sys; print(sys.version_info.minor)')
PYTHON_VERSION="${PYTHON_MAJOR}.${PYTHON_MINOR}"
PYTHON_TAG="cp${PYTHON_MAJOR}${PYTHON_MINOR}"

DOCS_ROOT="$PWD"
ROOT_DIR="$DOCS_ROOT/.."
VENV_DIR="$DOCS_ROOT/.docs-$PYTHON_VERSION"
DIST_DIR="$ROOT_DIR/dist"
SRC_DIR="$DOCS_ROOT/src"
BUILD_DIR="$DOCS_ROOT/html"

cleanup() {
    if [ -n "$VIRTUAL_ENV" ]; then
        deactivate
    fi
}
trap cleanup EXIT

cd "$DOCS_ROOT"
if [ "$(basename "$DOCS_ROOT")" != "docs" ]; then
    echo "Error: Please run from the 'docs' folder."
    exit 1
fi
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"
echo "Generating docs in virtual environment $VENV_DIR"

echo "Installing documentation tools..."
pip install --upgrade pip > /dev/null
pip install build sphinx sphinx-rtd-theme sphinx-autodoc-typehints sphinx-autoapi wheel > /dev/null

echo "Generating ReStructuredText docs with Sphinx......"
mkdir -p "$SRC_DIR/_static"
sphinx-build --write-all -b html "$SRC_DIR" "$BUILD_DIR"
find "$BUILD_DIR" -type f -name "*.html" -exec sed -i "s/synap\._synap/synap/g" {} +
echo -e "\033[32mReStrcturedText docs generated successfully\033[0m"
