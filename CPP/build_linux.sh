#!/bin/bash
echo "Building Computer Graphics C++ project for Linux..."

# Check if CMake is installed
if ! command -v cmake &> /dev/null; then
    echo "❌ CMake is not installed. Please install CMake first."
    echo "Ubuntu/Debian: sudo apt install cmake"
    echo "CentOS/RHEL: sudo yum install cmake"
    exit 1
fi

# Check if required packages are installed
echo "Checking dependencies..."

# Check for GLFW
if ! pkg-config --exists glfw3; then
    echo "❌ GLFW3 is not installed. Please install GLFW3 first."
    echo "Ubuntu/Debian: sudo apt install libglfw3-dev"
    echo "CentOS/RHEL: sudo yum install glfw-devel"
    exit 1
fi

# Check for OpenGL
if ! pkg-config --exists gl; then
    echo "❌ OpenGL development libraries are not installed."
    echo "Ubuntu/Debian: sudo apt install libgl1-mesa-dev"
    echo "CentOS/RHEL: sudo yum install mesa-libGL-devel"
    exit 1
fi

echo "✅ All dependencies found!"

# Create build directory
mkdir -p build
cd build

# Configure with CMake
echo "Configuring with CMake..."
cmake ..
if [ $? -ne 0 ]; then
    echo "❌ CMake configuration failed!"
    exit 1
fi

# Build project
echo "Building project..."
make -j$(nproc)
if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi

echo ""
echo "✅ Build successful!"
echo ""
echo "To run the demos:"
echo "  cd build"
echo "  ./bin/simple_triangle"
echo "  ./bin/triangle_demo"
echo "  ./bin/phong_triangle"
echo ""
