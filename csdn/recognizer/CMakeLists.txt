cmake_minimum_required(VERSION 2.8)
project(recognizer)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
find_package(OpenCV REQUIRED)
aux_source_directory(./ SOURCE_DIR)
add_executable(recognizer ${SOURCE_DIR})
target_link_libraries(recognizer ${OpenCV_LIBS})
