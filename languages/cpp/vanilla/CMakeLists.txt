cmake_minimum_required(VERSION 3.24)
project(ForgeBaseStarter CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(starter STATIC
    src/config.cpp
    src/log_severity.cpp
    src/logging.cpp
    src/greeter.cpp
)
target_include_directories(starter PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_compile_options(starter PRIVATE -Wall -Wextra -Werror)

add_executable(starter_cli app/main.cpp)
target_link_libraries(starter_cli PRIVATE starter)
target_compile_options(starter_cli PRIVATE -Wall -Wextra -Werror)
