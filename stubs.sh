#!/bin/bash

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.

set -e

ROOT_DIR="$PWD"
VENV_DIR="$ROOT_DIR/.stubgen"
SRC_DIR="$ROOT_DIR/src/synap"
BUILD_CONFIG="$ROOT_DIR/build/x86_64-linux-gnu.python3.10.py-build-cmake.local.toml"
BUILD_CACHE="$ROOT_DIR/.py-build-cmake_cache/cp310-cp310-linux_x86_64-x86_64-linux-gnu"
STUBGEN_DIR="$ROOT_DIR/stubgen"
OUTPUT_DIR="$STUBGEN_DIR/stubs"
STUBS_DIR="$OUTPUT_DIR/synap/_synap"
SYNAP_MODULE="synap._synap"

cleanup() {
    if [ -n "$VIRTUAL_ENV" ]; then
        echo "Deactivating and removing virtual environment..."
        deactivate
        rm -rf "$VENV_DIR"
    fi
}
trap cleanup EXIT

cd "$ROOT_DIR"

if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"
echo "Generating stubs in isolated environment $VIRTUAL_ENV"

echo "Installing pip packages..."
pip install --upgrade pip
pip install pybind11 pybind11-stubgen py-build-cmake typing-extensions numpy

if [ ! -f "$BUILD_CACHE/CMakeCache.txt" ]; then
    echo "Configuring build..."
    py-build-cmake --local "$BUILD_CONFIG" configure
fi
echo "Building extension..."
py-build-cmake --local "$BUILD_CONFIG" build

mkdir -p "$STUBGEN_DIR/synap"
cp "$BUILD_CACHE/_synap.cpython-310-x86_64-linux-gnu.so" "$STUBGEN_DIR/synap/"
PYTHONPATH="$STUBGEN_DIR:$PYTHONPATH" pybind11-stubgen "$SYNAP_MODULE" -o "$OUTPUT_DIR"
find "$STUBS_DIR" -type f -name "*.pyi" -exec sed -i "s/synap\._synap/synap/g" {} +
cp "$STUBS_DIR/__init__.pyi" "$SRC_DIR/__init__.pyi"
cp "$STUBS_DIR/preprocessor.pyi" "$SRC_DIR/preprocessor/__init__.pyi"
cp "$STUBS_DIR/postprocessor.pyi" "$SRC_DIR/postprocessor/__init__.pyi"
cp "$STUBS_DIR/types.pyi" "$SRC_DIR/types/__init__.pyi"