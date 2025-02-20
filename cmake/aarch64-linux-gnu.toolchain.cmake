# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.

include(CMakeDependentOption)
set(TOOLCHAIN_GNU_TRIPLE "aarch64-linux-gnu" CACHE STRING "The GNU triple of the toolchain to use" FORCE)

set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR arm)
set(CMAKE_LIBRARY_ARCHITECTURE $TOOLCHAIN_GNU_TRIPLE)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

set(TOOLCHAIN_DIR $ENV{TOOLCHAIN_DIR})
set(TOOLCHAIN_PREFIX aarch64-none-linux-gnu-)

set(CMAKE_C_COMPILER ${TOOLCHAIN_DIR}/bin/${TOOLCHAIN_PREFIX}gcc)
set(CMAKE_CXX_COMPILER ${TOOLCHAIN_DIR}/bin/${TOOLCHAIN_PREFIX}g++)

set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -pie -Wl,--no-undefined -Wl,--no-allow-shlib-undefined")
# uncomment for static linking
# set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -static-libgcc -static-libstdc++")
# set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -static-libgcc -static-libstdc++")

# search for programs in the build host directories
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)

# for libraries and headers in the target directories
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)

# To avoid warnings about C++ ABI changes since gcc-7.1
add_compile_options(-Wno-psabi)
