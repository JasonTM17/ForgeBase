cmake_minimum_required(VERSION 3.24)
project(ForgeBaseStarter C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

add_library(starter STATIC
    src/config.c
    src/log_severity.c
    src/logging.c
    src/greeter.c
)
target_include_directories(starter PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_compile_options(starter PRIVATE -Wall -Wextra -Werror)

add_executable(starter_cli app/main.c)
target_link_libraries(starter_cli PRIVATE starter)
target_compile_options(starter_cli PRIVATE -Wall -Wextra -Werror)
