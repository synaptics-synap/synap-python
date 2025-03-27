#!/bin/bash

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.

set -e

SYNAP_VERSION="0.0.4"
SYNAP_RELEASE="preview"
DOCS_ROOT="$PWD"
ROOT_DIR="$DOCS_ROOT/.."
VENV_DIR="$DOCS_ROOT/.docs"
DIST_DIR="$ROOT_DIR/dist"
HOST_ARCH=$(uname -m)
PLAT_TAG="manylinux_2_35"

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

echo "Installing Sphinx and dependencies..."
pip install --upgrade pip > /dev/null
pip install build sphinx sphinx-markdown-builder sphinx-rtd-theme wheel > /dev/null

echo "Installing latest SyNAP Python API wheel..."
PY_WHL="$DIST_DIR/synap_python-$SYNAP_VERSION-cp310-cp310-${PLAT_TAG}_${HOST_ARCH}.whl"
if [ ! -f "$PY_WHL" ]; then
    echo -e "\033[31mError: Wheel file for $HOST_ARCH not found\033[0m"
    if [ "$HOST_ARCH" == "x86_64" ]; then
        echo -e "       \033[31mBuild wheel with $ROOT_DIR/build.sh --x86_64\033[0m"
    elif [ "$HOST_ARCH" == "aarch64" ]; then
        echo -e "       \033[31mBuild wheel with $ROOT_DIR/build.sh\033[0m"
    else
        echo -e "       \033[31mError: Unsupported architecture '$HOST_ARCH'\033[0m"
    fi
    exit 1
fi
pip install --force-reinstall "$PY_WHL" > /dev/null

cd $DOCS_ROOT
echo "Building documentation..."
mkdir -p source/_static
make clean
sphinx-build -b markdown source build/markdown
find "build/markdown" -type f -name "*.md" -exec sed -i "s/synap\._synap/synap/g" {} +
echo -e "\033[32mDocs generated successfully\033[0m"
