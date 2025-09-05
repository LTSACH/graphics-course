cmake_minimum_required(VERSION 3.16)
project(ComputerGraphics)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find required packages
find_package(OpenGL REQUIRED)
find_package(glfw3 REQUIRED)

# Include directories
include_directories(${CMAKE_SOURCE_DIR})
include_directories(${CMAKE_SOURCE_DIR}/include)

# Add subdirectories
add_subdirectory(Triangle)

# Set compiler flags
if(APPLE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -framework OpenGL -framework Cocoa -framework IOKit -framework CoreVideo")
endif()

if(UNIX AND NOT APPLE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -lGL -lGLU -lX11 -lXxf86vm -lXrandr -lpthread -lXi -ldl")
endif()

if(WIN32)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -lopengl32 -lglu32")
endif()
