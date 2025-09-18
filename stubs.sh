#!/bin/bash

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.

set -e

SYNAP_VERSION="0.9.0"
HOST_ARCH=$(uname -m)
PLAT_TAG="manylinux_2_35"
PYTHON_MAJOR=$(python -c 'import sys; print(sys.version_info.major)')
PYTHON_MINOR=$(python -c 'import sys; print(sys.version_info.minor)')
PYTHON_VERSION="${PYTHON_MAJOR}.${PYTHON_MINOR}"
PYTHON_TAG="cp${PYTHON_MAJOR}${PYTHON_MINOR}"

ROOT_DIR="$PWD"
VENV_DIR="$ROOT_DIR/.stubs-$PYTHON_VERSION"
DIST_DIR="$ROOT_DIR/dist"
SRC_DIR="$ROOT_DIR/src/synap"
STUBGEN_DIR="$ROOT_DIR/stubgen"
OUTPUT_DIR="$STUBGEN_DIR/stubs"
STUBS_DIR="$OUTPUT_DIR/synap/_synap"

cleanup() {
    if [ -n "$VIRTUAL_ENV" ]; then
        deactivate
    fi
}
trap cleanup EXIT

cd "$ROOT_DIR"

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"
echo "Generating stubs in virtual environment $VENV_DIR"

echo "Installing pybind11-stubgen and dependencies..."
pip install --upgrade pip > /dev/null
pip install pybind11 pybind11-stubgen py-build-cmake typing-extensions numpy > /dev/null

PY_WHL="$DIST_DIR/synap_python-${SYNAP_VERSION}-${PYTHON_TAG}-${PYTHON_TAG}-${PLAT_TAG}_${HOST_ARCH}.whl"
if [ ! -f "$PY_WHL" ]; then
    echo -e "\033[31mError: Wheel file for $HOST_ARCH not found: $PY_WHL\033[0m"
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

echo "Generating stubs..."
mkdir -p "$STUBGEN_DIR/synap"
pybind11-stubgen synap \
    -o "$OUTPUT_DIR" \
    --enum-class-locations \
        Layout:synap._synap.types \
    --enum-class-locations \
        DataType:synap._synap.types \
    --enum-class-locations \
        InputType:synap._synap.preprocessor
find "$STUBS_DIR" -type f -name "*.pyi" -exec sed -i "s/synap\._synap/synap/g" {} +
find "$STUBS_DIR" -type f -name "*.pyi" -exec sed -i "1s|^|# SPDX-License-Identifier: Apache-2.0\n# SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.\n\n|" {} +
cp "$STUBS_DIR/__init__.pyi" "$SRC_DIR/__init__.pyi"
cp "$STUBS_DIR/preprocessor.pyi" "$SRC_DIR/preprocessor/__init__.pyi"
cp "$STUBS_DIR/postprocessor.pyi" "$SRC_DIR/postprocessor/__init__.pyi"
cp "$STUBS_DIR/types.pyi" "$SRC_DIR/types/__init__.pyi"
echo -e "\033[32mStubs generated successfully\033[0m"
