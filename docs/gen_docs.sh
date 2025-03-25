#!/bin/bash

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.

set -e

SYNAP_VERSION="0.0.3"
SYNAP_RELEASE="preview"
DOCS_ROOT="$PWD"
VENV_DIR="$DOCS_ROOT/.docs"
DIST_DIR="$DOCS_ROOT/../dist"

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
    pip install build sphinx sphinx-markdown-builder sphinx-rtd-theme wheel
fi
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source "$VENV_DIR/bin/activate"
fi

echo "Installing latest SyNAP Python API wheel..."
arch=$(uname -m)
cd "$DOCS_ROOT/.."
if [ "$arch" = "x86_64" ]; then
    bash ./build.sh --clean --local
    wheel="$DIST_DIR/synap_python-$SYNAP_VERSION-cp310-cp310-linux_x86_64.whl"
elif [ "$arch" = "aarch64" ]; then
    bash ./build.sh --clean
    wheel="$DIST_DIR/synap_python-$SYNAP_VERSION-cp310-cp310-linux_aarch64.whl"
else
    echo "Error: Unsupported architecture '$arch'."
    exit 1
fi

if [ ! -f "$wheel" ]; then
    echo "Error: SyNAP Python API wheel not found at '$wheel'."
    exit 1
fi
pip install --force-reinstall "$wheel"

cd $DOCS_ROOT
echo "Building documentation..."
mkdir -p source/_static
make clean
sphinx-build -b markdown source build/markdown
find "build/markdown" -type f -name "*.md" -exec sed -i "s/synap\._synap/synap/g" {} +
