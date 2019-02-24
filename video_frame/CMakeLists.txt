cmake_minimum_required(VERSION 3.11)
project(videoFrame)

set(CMAKE_CXX_STANDARD 14)
set(PY_VERSION 3.7)


find_package(OpenCV REQUIRED)
find_package(PythonLibs ${PY_VERSION} REQUIRED)
find_package(Boost 1.69.0 REQUIRED COMPONENTS python3.7 system)
find_package(Python ${PY_VERSION})

include_directories( ${OpenCV_INCLUDE_DIRS} ${PYTHON_INCLUDE_DIRS} )
include_directories(${PROJECT_SOURCE_DIR}/src)
include_directories(${Boost_INCLUDE_DIRS})


add_library(video_frame MODULE src/video_frame.cpp src/videoFrame.h)
set_target_properties(video_frame PROPERTIES PREFIX "")
target_link_libraries(video_frame ${OpenCV_LIBS} ${Boost_LIBRARIES} ${PYTHON_LIBRARIES} ${PYTHON_EXECUTABLE})

configure_file(${PROJECT_SOURCE_DIR}/src/__init__.py __init__.py COPYONLY)

add_executable(Video src/video.cpp src/videoFrame.h)
target_link_libraries(Video ${OpenCV_LIBS})

