#!/bin/bash

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.

set -e

SYNAP_VERSION="0.1.0"
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
SPHINX_SRC_DIR="$SRC_DIR/sphinx"
SPHINX_OUT_DIR="$DOCS_ROOT/html"

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
pip install build sphinx sphinx-rtd-theme sphinx-autodoc-typehints wheel > /dev/null
pip install mkdocs mkdocstrings[python] mkdocs-material > /dev/null
pip install mkdocs-gen-files mkdocs-literate-nav > /dev/null

echo "Installing SyNAP Python API wheel..."
PY_WHL="$DIST_DIR/synap_python-${SYNAP_VERSION}-${PYTHON_TAG}-${PYTHON_TAG}-${PLAT_TAG}_${HOST_ARCH}.whl"
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

echo "Generating ReStructuredText docs with Sphinx......"
mkdir -p "$SPHINX_SRC_DIR/_static"
sphinx-build --write-all -b html "$SPHINX_SRC_DIR" "$SPHINX_OUT_DIR"
find "$SPHINX_OUT_DIR" -type f -name "*.html" -exec sed -i "s/synap\._synap/synap/g" {} +
echo -e "\033[32mReStrcturedText docs generated successfully\033[0m"

