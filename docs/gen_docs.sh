#!/bin/bash

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.

set -e

SYNAP_VERSION="0.0.3"
SYNAP_RELEASE="preview"
DOCS_ROOT="$PWD"
VENV_DIR="$DOCS_ROOT/.docs"

cleanup() {
    if [ -n "$VIRTUAL_ENV" ]; then
        echo "Deactivating virtual environment..."
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
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    echo "Installing pip packages..."
    pip install --upgrade pip
    pip install sphinx sphinx-markdown-builder sphinx-rtd-theme
fi
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source "$VENV_DIR/bin/activate"
fi

echo "Installing latest SyNAP Python API wheel..."
pip install --force-reinstall "https://github.com/synaptics-synap/synap-python/releases/download/v$SYNAP_VERSION-$SYNAP_RELEASE/synap_python-$SYNAP_VERSION-cp310-cp310-linux_aarch64.whl"

echo "Building documentation..."
mkdir -p source/_static
make clean
sphinx-build -b markdown source build/markdown
find "build/markdown" -type f -name "*.md" -exec sed -i "s/synap\._synap/synap/g" {} +
