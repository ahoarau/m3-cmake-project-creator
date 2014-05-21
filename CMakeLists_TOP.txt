cmake_minimum_required(VERSION 2.8)
project(m3ens)

# Set the M3ENS_ROOT variable
set(M3ENS_ROOT ${PROJECT_SOURCE_DIR})
# Set where to find the FindXXX.cmake
set(CMAKE_MODULE_PATH "${M3ENS_ROOT}/../meka-cmake-modules/Modules/" ${CMAKE_MODULE_PATH})

# Set all bunch of usefull variables
set(M3ENS_INCLUDE_DIR ${M3ENS_ROOT}/include)

set(M3ENS_PROTO_DIR ${M3ENS_ROOT}/proto)

set(M3ENS_SRC_DIR ${M3ENS_ROOT}/src)

set(M3ENS_INSTALL_BIN ${M3ENS_ROOT}/bin)

set(M3ENS_BINARY_OUTPUT_DIRECTORY ${M3ENS_ROOT}/bin)

set(M3ENS_INSTALL_LIB ${M3ENS_ROOT}/lib)

set(M3ENS_LIBRARY_OUTPUT_DIRECTORY ${M3ENS_ROOT}/lib)

set(M3ENS_PYTHON_DIR ${M3ENS_ROOT}/python)

# Forcing the generation dirs to be local
set(CMAKE_BINARY_OUTPUT_DIRECTORY  ${M3ENS_BINARY_OUTPUT_DIRECTORY})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${M3ENS_LIBRARY_OUTPUT_DIRECTORY})

include_directories(
    ${M3ENS_INCLUDE_DIR}
    ${CMAKE_BINARY_DIR}/src # Include this directory for the generated protobufs headers
)


# Add the main project src dir that contains all the others
add_subdirectory(src/m3ens)
