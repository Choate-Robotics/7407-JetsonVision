cmake_minimum_required(VERSION 3.5)
project(videoFrame)

set(CMAKE_CXX_STANDARD 14)
set(PY_VERSION 3.7)
#set(COMPILE_FLAGS -fno-stack-protector)
set(CMAKE_MODULE_PATH  /usr/local/lib)

find_package(OpenCV REQUIRED)
find_package(PythonLibs ${PY_VERSION} REQUIRED)
find_package(Python ${PY_VERSION})
find_package(Boost 1.69.0 REQUIRED COMPONENTS python37 system)

include_directories( ${OpenCV_INCLUDE_DIRS} ${PYTHON_INCLUDE_DIRS} )
include_directories(${PROJECT_SOURCE_DIR}/src)
include_directories(${Boost_INCLUDE_DIRS})


add_library(video_frame MODULE src/video_frame.cpp src/videoFrame.h)
set_target_properties(video_frame PROPERTIES PREFIX "")
target_link_libraries(video_frame ${OpenCV_LIBS} ${Boost_LIBRARIES} ${PYTHON_LIBRARIES} )

configure_file(${PROJECT_SOURCE_DIR}/src/__init__.py __init__.py COPYONLY)

add_executable(Video src/video.cpp src/videoFrame.h)
target_link_libraries(Video ${OpenCV_LIBS})

