cmake_minimum_required(VERSION 3.22)
project(doc_lab1)

set(CMAKE_CXX_STANDARD 20)
find_package(OpenMP REQUIRED)

add_executable(doc_lab1 main.cpp)

target_link_libraries(doc_lab1
        PRIVATE
        OpenMP::OpenMP_CXX)