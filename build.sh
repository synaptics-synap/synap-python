#!/bin/bash

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.

set -e

PYTHON_DEV_URL="https://github.com/tttapa/python-dev/releases/download/0.0.7/python-dev-3.10.15-aarch64-rpi3-linux-gnu.tar.gz"
TOOLCHAIN_URL="https://developer.arm.com/-/media/Files/downloads/gnu/11.3.rel1/binrel/arm-gnu-toolchain-11.3.rel1-x86_64-aarch64-none-linux-gnu.tar.xz"

ROOT_DIR="$PWD"
BUILD_DIR="$ROOT_DIR/build"
CACHE_DIR="$ROOT_DIR/.py-build-cmake_cache"

VERBOSE=false
CLEAN=false
x86_64=false


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
        --x86_64)
            x86_64=true
            shift
            ;;
        *)
            echo "Usage: $0 [--clean] [--verbose]"
            exit 1
            ;;
    esac
done

TARGET_ARCH="aarch64"
HOST_ARCH=$(uname -m)

if [[ "$HOST_ARCH" != "x86_64" && "$HOST_ARCH" != "aarch64" ]]; then
    echo "Error: Unsupported architecture '$HOST_ARCH'."
    exit 1
fi

if [[ "$x86_64" == true && "$HOST_ARCH" != "x86_64" ]]; then
    echo "Error: Cannot build for x86_64 on arch $HOST_ARCH"
    exit 1
fi

if [[ "$HOST_ARCH" != "$TARGET_ARCH" && "$x86_64" != true ]]; then
    CROSSCOMPILE=true
    TOOLCHAIN_DIR="$BUILD_DIR/toolchain"
    PYTHON_DEV_DIR="$BUILD_DIR/python-dev"
else
    CROSSCOMPILE=false
    TOOLCHAIN_DIR=
    PYTHON_DEV_DIR=
fi

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
    if $CROSSCOMPILE; then
        python -m build -w . -C "cross=$BUILD_CONFIG"
    else
        python -m build -w . -C "local=$BUILD_CONFIG"
    fi
}

generate_stubs() {
    bash "$ROOT_DIR/stubs.sh"
}

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
LOG_DIR="$ROOT_DIR/logs/$TIMESTAMP"
mkdir -p "$LOG_DIR"

run_cmd "git submodule update --init --recursive" "Updating submodules" "$LOG_DIR/submodule_update.log"

if $CROSSCOMPILE; then
    echo "Cross-compiling for aarch64-linux-gnu, toolchain: $TOOLCHAIN_DIR, python-dev: $PYTHON_DEV_DIR"
    run_cmd "setup_toolchain" "Setting up toolchain" "$LOG_DIR/toolchain_setup.log"
    export TOOLCHAIN_DIR
    export PYTHON_DEV_DIR
fi

run_cmd "setup_venv" "Setting up virtual environment" "$LOG_DIR/venv_activation.log"

if $CLEAN; then
    if $x86_64; then
        rm -rf "$CACHE_DIR/cp310-cp310-linux_x86_64-x86_64-linux-gnu"
    else
        rm -rf "$CACHE_DIR/cp310-cp310-linux_aarch64-aarch64-linux-gnu"
    fi
    echo "Cleaned cache directory for fresh build"
fi

if $x86_64; then
    echo "Building for x86_64"
    BUILD_CONFIG="$BUILD_DIR/x86_64-linux-gnu.python3.10.py-build-cmake.local.toml"
else
    echo "Building for aarch64-linux-gnu"
    if $CROSSCOMPILE; then
        BUILD_CONFIG="$BUILD_DIR/aarch64-linux-gnu.python3.10.py-build-cmake.cross.toml"
    else
        BUILD_CONFIG="$BUILD_DIR/aarch64-linux-gnu.python3.10.py-build-cmake.local.toml"
    fi
fi
run_cmd "build_extensions" "Building Python extensions" "$LOG_DIR/build_extensions.log"

if $CROSSCOMPILE; then
    echo "Skipping stubs generation for cross-compilation"
else
    run_cmd "generate_stubs" "Generating stubs" "$LOG_DIR/stubgen.log"
fi

echo -e "\033[32mBuild completed successfully, wheel located at $ROOT_DIR/dist/\033[0m"

if [ -z "$(ls -A "$LOG_DIR")" ]; then
    rmdir "$LOG_DIR"
fi
