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

if(MSVC)
    set(STARTER_WARNING_FLAGS /W4 /WX)
else()
    set(STARTER_WARNING_FLAGS -Wall -Wextra -Werror)
endif()

target_compile_options(starter PRIVATE ${STARTER_WARNING_FLAGS})

add_executable(starter_cli app/main.c)
target_link_libraries(starter_cli PRIVATE starter)
target_compile_options(starter_cli PRIVATE ${STARTER_WARNING_FLAGS})

enable_testing()
add_executable(test_starter tests/test_starter.c)
target_link_libraries(test_starter PRIVATE starter)
target_compile_options(test_starter PRIVATE ${STARTER_WARNING_FLAGS})
add_test(NAME starter_tests COMMAND test_starter)
