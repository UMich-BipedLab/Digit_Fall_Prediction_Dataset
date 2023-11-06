# Specify the minimum version.
cmake_minimum_required(VERSION 3.9)

# Specify the project info.
project(digit_data VERSION 1.0 DESCRIPTION "digit kinematics and dynamics calculation library")

set(C_KIN ${CMAKE_CURRENT_SOURCE_DIR}/c_kin)

file(GLOB DIGIT_C_KIN_SRC ${C_KIN}/*.c)
file(GLOB DIGIT_C_KIN_HEADER ${C_KIN}/*.h)

foreach(digit_c_kin_src ${DIGIT_C_KIN_SRC})
    get_filename_component(basename ${digit_c_kin_src} NAME_WE)
    message(STATUS ${basename})

    add_library(${basename} SHARED ${digit_c_kin_src})
    target_include_directories(${basename} PRIVATE C_KIN)
    set_target_properties(${basename} PROPERTIES VERSION ${PROJECT_VERSION})
    set_target_properties(${basename} PROPERTIES SOVERSION ${PROJECT_VERSION_MAJOR})
endforeach()
