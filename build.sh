#!/bin/bash

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.

set -e

PYTHON_DEV_URL="https://github.com/tttapa/python-dev/releases/download/0.0.7/python-dev-3.10.15-aarch64-rpi3-linux-gnu.tar.gz"
TOOLCHAIN_URL="https://developer.arm.com/-/media/Files/downloads/gnu/11.3.rel1/binrel/arm-gnu-toolchain-11.3.rel1-x86_64-aarch64-none-linux-gnu.tar.xz"

ROOT_DIR="$PWD"
PYBIND11_DIR="$ROOT_DIR/extern/pybind11"
VENV_DIR="$ROOT_DIR/.venv"
BUILD_DIR="$ROOT_DIR/build"
PYTHON_DEV_DIR="$BUILD_DIR/python-dev"
TOOLCHAIN_DIR="$BUILD_DIR/toolchain"
CACHE_DIR="$ROOT_DIR/.py-build-cmake_cache"
DIST_DIR="$ROOT_DIR/dist"

VERBOSE=false
CLEAN=false
LOCAL=false

if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "\033[33m[Warning]\033[0m Not running in a Python virtual environment, system python installation may be modified"
    echo -e "          Continue? [Y/n]: "
    read -r response
    if [ "$response" != "Y" ] && [ "$response" != "y" ]; then
        exit 0
    fi
fi

while [[ $# -gt 0 ]]; do
    case $1 in
        --clean)
            CLEAN=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --local)
            LOCAL=true
            shift
            ;;
        *)
            echo "Usage: $0 [--clean] [--verbose]"
            exit 1
            ;;
    esac
done

run_cmd() {
    local command=$1
    local message=$2
    local log_file=$3
    local delay=0.1
    local spinstr='|/-\'

    echo -n "$message ... "
    if $VERBOSE; then
        ($command > >(tee -a "$log_file") 2> >(tee -a "$log_file" >&2)) &
        local pid=$!
    else
        ($command > "$log_file" 2>&1) &
        local pid=$!
        while kill -0 "$pid" 2>/dev/null; do
            for i in $(seq 0 3); do
                printf "\r$message ... [%c] " "${spinstr:i:1}"
                sleep "$delay"
            done
        done
    fi

    set +e
    wait $pid
    local exit_code=$?
    set -e

    if [ $exit_code -eq 0 ]; then
        rm -f "$log_file"
        printf "\r$message ... \033[32mSuccess!\033[0m\n"
    else
        printf "\r$message ... \033[31mFailed!\033[0m\nCheck log: $log_file\n"
        exit $exit_code
    fi
}

verify_archive() {
    archive_dir=$1
    archive_link=$2
    archive_name="temp.tar.gz"
    if [ ! -d "$archive_dir" ]; then
        mkdir -p "$archive_dir"
        wget -O "$archive_name" "$archive_link"
        tar -C "$archive_dir" -xvf "$archive_name" --strip-components=1
        rm "$archive_name"
    fi
}

setup_toolchain() {
    cd $BUILD_DIR
    verify_archive $PYTHON_DEV_DIR $PYTHON_DEV_URL
    verify_archive $TOOLCHAIN_DIR $TOOLCHAIN_URL
}

setup_venv() {
    pip install --upgrade pip
    pip install build wheel
}

build_extensions() {
    cd $ROOT_DIR
    if $LOCAL; then
        python -m build -w . -C "local=$BUILD_CONFIG"
    else
        python -m build -w . -C "cross=$BUILD_CONFIG"
    fi
}

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
LOG_DIR="$ROOT_DIR/logs/$TIMESTAMP"
mkdir -p "$LOG_DIR"

run_cmd "git submodule update --init --recursive" "Updating submodules" "$LOG_DIR/submodule_update.log"

run_cmd "setup_toolchain" "Setting up toolchain" "$LOG_DIR/toolchain_setup.log"
export PYTHON_DEV_DIR
export TOOLCHAIN_DIR

run_cmd "setup_venv" "Setting up virtual environment" "$LOG_DIR/venv_activation.log"

if $CLEAN; then
    if $LOCAL; then
        rm -rf "$CACHE_DIR/cp310-cp310-linux_x86_64-x86_64-linux-gnu"
        echo "Cleaned dist directory for fresh build"
    else
        rm -rf "$CACHE_DIR/cp310-cp310-linux_aarch64-aarch64-linux-gnu"
        echo "Cleaned cache directory for fresh build"
    fi
fi

if $LOCAL; then
    echo "Building locally"
    BUILD_CONFIG="$BUILD_DIR/x86_64-linux-gnu.python3.10.py-build-cmake.local.toml"
else
    echo "Building for aarch64-linux-gnu"
    BUILD_CONFIG="$BUILD_DIR/aarch64-linux-gnu.python3.10.py-build-cmake.cross.toml"
fi
run_cmd "build_extensions" "Building Python extensions" "$LOG_DIR/build_extensions.log"

echo -e "\033[32mBuild completed successfully, wheel located at $ROOT_DIR/dist/\033[0m"

if [ -z "$(ls -A "$LOG_DIR")" ]; then
    rmdir "$LOG_DIR"
fi
