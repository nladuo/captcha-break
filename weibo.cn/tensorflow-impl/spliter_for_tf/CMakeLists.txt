cmake_minimum_required(VERSION 2.8)
project(spliter_for_tf)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
find_package(OpenCV REQUIRED)
aux_source_directory(./ SOURCE_DIR)
add_executable(spliter_for_tf ${SOURCE_DIR})
target_link_libraries(spliter_for_tf ${OpenCV_LIBS})
