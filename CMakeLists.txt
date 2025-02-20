# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright © 2019 Synaptics Incorporated.

cmake_minimum_required(VERSION 3.19)
project(synap-python)

if (NOT CMAKE_BUILD_TYPE)
    message(FATAL_ERROR "Build type not provided, set with -DCMAKE_BUILD_TYPE")
endif()
set(FRAMEWORK_DIR ${CMAKE_SOURCE_DIR}/extern/framework)

list(APPEND CMAKE_MODULE_PATH ${FRAMEWORK_DIR}/cmake/modules)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_C_STANDARD 11)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
if(NOT CMAKE_CROSSCOMPILING)
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -pie  -Wl,--no-undefined -Wl,--no-allow-shlib-undefined")
endif()

message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")

if (CMAKE_CXX_COMPILER_ID STREQUAL "GNU" AND CMAKE_CXX_COMPILER_VERSION VERSION_LESS 9.0)
    message("Old GCC version detected, disabling C++-17 standard filesystem library")
    set(ENABLE_CXX_STD_FILESYSTEM OFF)
else()
    set(ENABLE_CXX_STD_FILESYSTEM ON)
endif()

add_subdirectory(${FRAMEWORK_DIR}/lib)

set(TARGET_NAME _synap)
set(EXPORT_SRC
    src/export_preprocessor.cpp
    src/export_postprocessor.cpp
    src/export_tensor.cpp
    src/export_types.cpp
    src/export.cpp
)

include(cmake/FindPybind11.cmake)
find_pybind11_python_first()
pybind11_add_module(${TARGET_NAME} ${EXPORT_SRC})

# add debug identifiers
set_target_properties(${TARGET_NAME} PROPERTIES
    DEBUG_POSTFIX "${CMAKE_DEBUG_POSTFIX}${PYTHON_MODULE_DEBUG_POSTFIX}")
target_compile_definitions(${TARGET_NAME} PRIVATE
    MODULE_NAME=$<TARGET_FILE_BASE_NAME:${TARGET_NAME}>
    VERSION_INFO="${PY_FULL_VERSION}"
)

# expose only exported symbols to reduce shared library size
set_target_properties(${TARGET_NAME} PROPERTIES
    CXX_VISIBILITY_PRESET "hidden"
    VISIBILITY_INLINES_HIDDEN true)
if (CMAKE_SYSTEM_NAME MATCHES "Linux")
    target_link_options(${TARGET_NAME} PRIVATE "LINKER:--exclude-libs,ALL")
endif()

target_link_libraries(${TARGET_NAME} PRIVATE
    synapnb
    synap_base
    synap_preprocess
    synap_postprocess
)

install(TARGETS ${TARGET_NAME}
    EXCLUDE_FROM_ALL
    COMPONENT python_modules
    DESTINATION ${PY_BUILD_CMAKE_IMPORT_NAME}
)
