# This file incorporates code from toolchains (https://github.com/tttapa/toolchains),
# which is licensed under the MIT License and copyright (c) 2022 Pieter P

include("${CMAKE_CURRENT_LIST_DIR}/aarch64-linux-gnu.toolchain.cmake")

# Logic for locating Python
# ------------------------------------------------------------------------------

if (NOT DEFINED TOOLCHAIN_GNU_TRIPLE)
    message(FATAL_ERROR "This toolchain file is not intended to be used directly")
endif()

# User options
set(TOOLCHAIN_PYTHON_VERSION "3" CACHE STRING "Python version to locate")
option(TOOLCHAIN_NO_FIND_PYTHON "Do not set the FindPython hints" Off)
option(TOOLCHAIN_NO_FIND_PYTHON3 "Do not set the FindPython3 hints" Off)

# Inform CMake about these options (for try_compile etc.)
list(APPEND CMAKE_TRY_COMPILE_PLATFORM_VARIABLES
    TOOLCHAIN_PYTHON_VERSION TOOLCHAIN_NO_FIND_PYTHON TOOLCHAIN_NO_FIND_PYTHON3)

# Internal variables
set(TOOLCHAIN_PYTHON_ROOT "$ENV{PYTHON_DEV_DIR}")
list(APPEND CMAKE_FIND_ROOT_PATH "${TOOLCHAIN_PYTHON_ROOT}")

# Determine the paths and other properties of the Python installation
function(toolchain_locate_python)
    # Locate the python-config script
    set(_TOOLCHAIN_PYTHON_CONFIG_VERSION ${TOOLCHAIN_PYTHON_VERSION})
    if (_TOOLCHAIN_PYTHON_CONFIG_VERSION MATCHES "^([0-9]+\\.[0-9]+)")
        set(_TOOLCHAIN_PYTHON_CONFIG_VERSION ${CMAKE_MATCH_1})
    endif()
    file(GLOB _TOOLCHAIN_PYTHON_CONFIG_LIST LIST_DIRECTORIES false
        "${TOOLCHAIN_PYTHON_ROOT}/usr/local/bin/python${_TOOLCHAIN_PYTHON_CONFIG_VERSION}-config")
    message("${TOOLCHAIN_PYTHON_ROOT}/usr/local/bin/python${_TOOLCHAIN_PYTHON_CONFIG_VERSION}-config")
    if (NOT _TOOLCHAIN_PYTHON_CONFIG_LIST)
        message(FATAL_ERROR "Failed to locate python${_TOOLCHAIN_PYTHON_CONFIG_VERSION}-config")
    endif()
    list(GET _TOOLCHAIN_PYTHON_CONFIG_LIST 0 _TOOLCHAIN_PYTHON_CONFIG)
    message(STATUS "Found target Python${TOOLCHAIN_PYTHON_VERSION} config: ${_TOOLCHAIN_PYTHON_CONFIG}")

    # Determine the ABI flags
    execute_process(COMMAND ${_TOOLCHAIN_PYTHON_CONFIG} --abiflags
        OUTPUT_VARIABLE _TOOLCHAIN_PYTHON_ABI OUTPUT_STRIP_TRAILING_WHITESPACE
        RESULT_VARIABLE result)
    if (NOT result EQUAL 0)
        message(FATAL_ERROR "Unable to determine Python ABI flags: ${_TOOLCHAIN_PYTHON_ABI}")
    endif()
    message(STATUS "Found target Python${TOOLCHAIN_PYTHON_VERSION} ABI: ${_TOOLCHAIN_PYTHON_ABI}")

    # Determine the full version and ABI from the include directories
    execute_process(COMMAND ${_TOOLCHAIN_PYTHON_CONFIG} --includes
        OUTPUT_VARIABLE _TOOLCHAIN_PYTHON_INCLUDES OUTPUT_STRIP_TRAILING_WHITESPACE
        RESULT_VARIABLE result)
    if (NOT result EQUAL 0 OR NOT _TOOLCHAIN_PYTHON_INCLUDES)
        message(FATAL_ERROR "Unable to determine Python includes: ${_TOOLCHAIN_PYTHON_INCLUDES}")
    endif()
    if (NOT _TOOLCHAIN_PYTHON_INCLUDES MATCHES "/include/python(${_TOOLCHAIN_PYTHON_CONFIG_VERSION}[.0-9]*${_TOOLCHAIN_PYTHON_ABI})")
        message(FATAL_ERROR "Unable to determine Python include directory: ${_TOOLCHAIN_PYTHON_INCLUDES}")
    endif()
    set(_TOOLCHAIN_PYTHON_VERSIONABI ${CMAKE_MATCH_1})

    # Determine the extension suffix:
    execute_process(COMMAND ${_TOOLCHAIN_PYTHON_CONFIG} --extension-suffix
        OUTPUT_VARIABLE _TOOLCHAIN_PYTHON_EXTSUFFIX
        OUTPUT_STRIP_TRAILING_WHITESPACE
        RESULT_VARIABLE result)
    if (NOT result EQUAL 0 OR NOT _TOOLCHAIN_PYTHON_EXTSUFFIX)
        message(FATAL_ERROR "Unable to determine extension suffix: ${_TOOLCHAIN_PYTHON_EXTSUFFIX}")
    endif()
    message(STATUS "Found target Python${TOOLCHAIN_PYTHON_VERSION} extension suffix: ${_TOOLCHAIN_PYTHON_EXTSUFFIX}")

    # Set the SOABI
    if (_TOOLCHAIN_PYTHON_EXTSUFFIX MATCHES "^(${CMAKE_SHARED_LIBRARY_SUFFIX}|\\.so|\\.pyd)$")
        set(_TOOLCHAIN_PYTHON_SOABI "")
    else()
        string(REGEX REPLACE "^[.-](.+)(${CMAKE_SHARED_LIBRARY_SUFFIX}|\\.(so|pyd))$" "\\1"
               _TOOLCHAIN_PYTHON_SOABI "${_TOOLCHAIN_PYTHON_EXTSUFFIX}")
    endif()
    message(STATUS "Found target Python${TOOLCHAIN_PYTHON_VERSION} SOABI: ${_TOOLCHAIN_PYTHON_SOABI}")

    # Set the SOSABI (stable ABI)
    if (CMAKE_SYSTEM_NAME STREQUAL "Windows" OR CMAKE_SYSTEM_NAME MATCHES "MSYS|CYGWIN")
        set(_TOOLCHAIN_PYTHON_SOSABI "")
    else()
        set(_TOOLCHAIN_PYTHON_SOSABI "abi3")
    endif()
    message(STATUS "Found target Python${TOOLCHAIN_PYTHON_VERSION} SOSABI: ${_TOOLCHAIN_PYTHON_SOSABI}")

    # Set result variables (cached)
    set(TOOLCHAIN_PYTHON_ABI "${_TOOLCHAIN_PYTHON_ABI}" CACHE STRING "" FORCE)
    set(TOOLCHAIN_PYTHON_EXTSUFFIX "${_TOOLCHAIN_PYTHON_EXTSUFFIX}" CACHE STRING "" FORCE)
    set(TOOLCHAIN_PYTHON_SOABI "${_TOOLCHAIN_PYTHON_SOABI}" CACHE STRING "" FORCE)
    set(TOOLCHAIN_PYTHON_SOSABI "${_TOOLCHAIN_PYTHON_SOSABI}" CACHE STRING "" FORCE)
    set(TOOLCHAIN_PYTHON_ROOT_DIR "${TOOLCHAIN_PYTHON_ROOT}/usr/local" CACHE PATH "" FORCE)
    set(TOOLCHAIN_PYTHON_LIBRARY "${TOOLCHAIN_PYTHON_ROOT_DIR}/lib/libpython${_TOOLCHAIN_PYTHON_VERSIONABI}.so" CACHE FILEPATH "" FORCE)
    set(TOOLCHAIN_PYTHON_INCLUDE_DIR "${TOOLCHAIN_PYTHON_ROOT_DIR}/include/python${_TOOLCHAIN_PYTHON_VERSIONABI}" CACHE PATH "" FORCE)

    message(STATUS "Target Python${TOOLCHAIN_PYTHON_VERSION} root dir: ${TOOLCHAIN_PYTHON_ROOT_DIR}")
    message(STATUS "Target Python${TOOLCHAIN_PYTHON_VERSION} library: ${TOOLCHAIN_PYTHON_LIBRARY}")
    message(STATUS "Target Python${TOOLCHAIN_PYTHON_VERSION} include dir: ${TOOLCHAIN_PYTHON_INCLUDE_DIR}")
endfunction()

if (NOT TOOLCHAIN_NO_FIND_PYTHON OR NOT TOOLCHAIN_NO_FIND_PYTHON3)
    # Determine Python location and properties if not already cached
    if (NOT DEFINED TOOLCHAIN_PYTHON_ABI
     OR NOT DEFINED TOOLCHAIN_PYTHON_EXTSUFFIX
     OR NOT DEFINED TOOLCHAIN_PYTHON_SOABI
     OR NOT DEFINED TOOLCHAIN_PYTHON_SOSABI
     OR NOT DEFINED TOOLCHAIN_PYTHON_ROOT_DIR
     OR NOT DEFINED TOOLCHAIN_PYTHON_LIBRARY
     OR NOT DEFINED TOOLCHAIN_PYTHON_INCLUDE_DIR
     OR NOT TOOLCHAIN_PYTHON_VERSION STREQUAL "${_TOOLCHAIN_PYTHON_VERSION_PREVIOUS}")
        toolchain_locate_python()
        set(_TOOLCHAIN_PYTHON_VERSION_PREVIOUS "${TOOLCHAIN_PYTHON_VERSION}" CACHE INTERNAL "")
    endif()
    # Set FindPython hints and artifacts
    if (NOT TOOLCHAIN_NO_FIND_PYTHON)
        set(Python_ROOT_DIR ${TOOLCHAIN_PYTHON_ROOT_DIR} CACHE PATH "" FORCE)
        set(Python_LIBRARY ${TOOLCHAIN_PYTHON_LIBRARY} CACHE FILEPATH "" FORCE)
        set(Python_INCLUDE_DIR ${TOOLCHAIN_PYTHON_INCLUDE_DIR} CACHE PATH "" FORCE)
        set(Python_SOABI ${TOOLCHAIN_PYTHON_SOABI} CACHE STRING "" FORCE)
        set(Python_SOSABI ${TOOLCHAIN_PYTHON_SOSABI} CACHE STRING "" FORCE)
        set(Python_INTERPRETER_ID "Python" CACHE STRING "" FORCE)
    endif()
    # Set FindPytho3 hints and artifacts
    if (NOT TOOLCHAIN_NO_FIND_PYTHON3)
        set(Python3_ROOT_DIR ${TOOLCHAIN_PYTHON_ROOT_DIR} CACHE PATH "" FORCE)
        set(Python3_LIBRARY ${TOOLCHAIN_PYTHON_LIBRARY} CACHE FILEPATH "" FORCE)
        set(Python3_INCLUDE_DIR ${TOOLCHAIN_PYTHON_INCLUDE_DIR} CACHE PATH "" FORCE)
        set(Python3_SOABI ${TOOLCHAIN_PYTHON_SOABI} CACHE STRING "" FORCE)
        set(Python3_SOSABI ${TOOLCHAIN_PYTHON_SOSABI} CACHE STRING "" FORCE)
        set(Python3_INTERPRETER_ID "Python" CACHE STRING "" FORCE)
    endif()
    # Set pybind11 hints
    get_filename_component(PYTHON_MODULE_DEBUG_POSTFIX ${TOOLCHAIN_PYTHON_EXTSUFFIX} NAME_WE)
    get_filename_component(PYTHON_MODULE_EXTENSION ${TOOLCHAIN_PYTHON_EXTSUFFIX} EXT)
    if (TOOLCHAIN_PYTHON_ABI MATCHES "d")
        set(PYTHON_IS_DEBUG TRUE)
    else()
        set(PYTHON_IS_DEBUG FALSE)
    endif()
    set(PYTHON_MODULE_DEBUG_POSTFIX ${PYTHON_MODULE_DEBUG_POSTFIX} CACHE INTERNAL "")
    set(PYTHON_MODULE_EXTENSION ${PYTHON_MODULE_EXTENSION} CACHE INTERNAL "")
    set(PYTHON_IS_DEBUG ${PYTHON_IS_DEBUG} CACHE INTERNAL "")
endif()
