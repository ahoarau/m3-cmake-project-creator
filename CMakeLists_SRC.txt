cmake_minimum_required(VERSION 2.8)

project(controller_example) 

find_package(RTAI REQUIRED)
find_package(M3rt REQUIRED)
find_package(M3 REQUIRED toolbox chains robots hardware)
find_package(Boost REQUIRED)
find_package(Eigen3 3.2 REQUIRED)
find_package(Protobuf REQUIRED)
find_package(OROCOS-KDL REQUIRED)

# Start Protobuf
# Get all your protofiles
file(GLOB ProtoFiles "${M3ENS_PROTO_DIR}/m3ens/${PROJECT_NAME}/*.proto")
# Import external directories
SET(PROTOBUF_IMPORT_DIRS ${M3RT_INCLUDE_DIR} ${M3_INCLUDE_DIR})
# Generate the .pb.cc and .pb.h files
PROTOBUF_GENERATE_CPP(ProtoSources ProtoHeaders ${CMAKE_CURRENT_BINARY_DIR} ${ProtoFiles})
# Add a custom target to force the re-generation
add_custom_target(${PROJECT_NAME}_cpp_protobuf_output  ALL DEPENDS ${ProtoSources})
## Python protobufs
find_package(PythonLibs 2.7 REQUIRED)
find_package(PythonInterp REQUIRED) 
## Generate and copy the python protobuf
# Import external directories
SET(PROTOBUF_IMPORT_DIRS ${M3RT_INCLUDE_DIR} ${M3_INCLUDE_DIR})
# Generate the .pb.py files
PROTOBUF_GENERATE_PYTHON(PySources ${M3ENS_PYTHON_DIR}/m3ens/${PROJECT_NAME} ${ProtoFiles}) 
# Add a custom target to force the re-generation
add_custom_target(${PROJECT_NAME}_python_protobuf_output ALL DEPENDS ${PySources})
# End Protobuf 

# We assume that the M3 SDK was installed in /usr/local:
set(M3_PREFIX /usr/local)


# Include dirs to look for
include_directories(
    ${M3RT_INCLUDE_DIR}
    ${RTAI_INCLUDE_DIR}
    ${EIGEN3_INCLUDE_DIR}
    ${PROTOBUF_INCLUDE_DIR}
    ${M3_INCLUDE_DIR}
    ${KDL_INCLUDE_DIRS}
)


# Libraries to link against
SET(LIBS ${RTAI_LIBRARIES} pthread ${Boost_LIBRARIES} ${EIGEN3_LIBRARIES} ${PROTOBUF_LIBRARIES} m3hardware m3toolbox orocos-kdl m3robots m3chains)

# Set your srcs here
set( ALL_SRCS
factory_proxy.cpp
example.cpp
)

# Set your headers here
set( ALL_HDRS
example.h
)


# Add the proto-sources to the src list
list(APPEND ALL_SRCS ${ProtoSources})

# Add the proto-headers to the headers 
list(APPEND ALL_HDRS
${ProtoHeaders}
)


# Building
add_library(${PROJECT_NAME} SHARED ${ALL_SRCS})
# Linking
target_link_libraries(${PROJECT_NAME} ${LIBS})








