cmake_minimum_required(VERSION 3.11)
project(Vision)

set(CMAKE_CXX_STANDARD 14)

add_executable(Vision imageProcessing.cpp)

find_package(OpenCV REQUIRED)
include_directories( ${OpenCV_INCLUDE_DIRS} )
target_link_libraries( Vision ${OpenCV_LIBS} )