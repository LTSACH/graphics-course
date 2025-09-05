# Triangle Demo CMakeLists.txt

# Add GLAD source
add_library(glad STATIC ${CMAKE_SOURCE_DIR}/include/glad.c)

# Create executable
add_executable(triangle_demo triangle_demo.cpp)
add_executable(simple_triangle simple_triangle.cpp)
add_executable(phong_triangle phong_triangle.cpp)
add_executable(textured_triangle textured_triangle.cpp)
add_executable(rose_textured_triangle rose_textured_triangle.cpp)

# Include directories
target_include_directories(triangle_demo PRIVATE ${CMAKE_SOURCE_DIR}/include)
target_include_directories(simple_triangle PRIVATE ${CMAKE_SOURCE_DIR}/include)
target_include_directories(phong_triangle PRIVATE ${CMAKE_SOURCE_DIR}/include ${CMAKE_SOURCE_DIR}/include/glm)
target_include_directories(textured_triangle PRIVATE ${CMAKE_SOURCE_DIR}/include ${CMAKE_SOURCE_DIR}/include/glm)
target_include_directories(rose_textured_triangle PRIVATE ${CMAKE_SOURCE_DIR}/include ${CMAKE_SOURCE_DIR}/include/glm)

# Link libraries
target_link_libraries(triangle_demo glad glfw OpenGL::GL)
target_link_libraries(simple_triangle glad glfw OpenGL::GL)
target_link_libraries(phong_triangle glad glfw OpenGL::GL)
target_link_libraries(textured_triangle glad glfw OpenGL::GL)
target_link_libraries(rose_textured_triangle glad glfw OpenGL::GL)

# Set properties
set_target_properties(triangle_demo PROPERTIES
    OUTPUT_NAME "triangle_demo"
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
)

set_target_properties(simple_triangle PROPERTIES
    OUTPUT_NAME "simple_triangle"
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
)

set_target_properties(phong_triangle PROPERTIES
    OUTPUT_NAME "phong_triangle"
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
)

set_target_properties(textured_triangle PROPERTIES
    OUTPUT_NAME "textured_triangle"
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
)

set_target_properties(rose_textured_triangle PROPERTIES
    OUTPUT_NAME "rose_textured_triangle"
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin
)
