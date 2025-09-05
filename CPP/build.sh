#!/bin/bash

# Build script for Computer Graphics C++ project

echo "Building Computer Graphics C++ project..."

# Create build directory
mkdir -p build
cd build

# Configure with CMake
echo "Configuring with CMake..."
cmake ..

# Build
echo "Building project..."
make

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo ""
    echo "To run the demos:"
    echo "  ./bin/triangle_demo"
    echo "  ./bin/simple_triangle"
else
    echo "❌ Build failed!"
    exit 1
fi
