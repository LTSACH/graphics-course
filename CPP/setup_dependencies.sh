#!/bin/bash
echo "Setting up dependencies for Computer Graphics C++ project..."

# Function to detect OS
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command -v apt &> /dev/null; then
            echo "ubuntu"
        elif command -v yum &> /dev/null; then
            echo "centos"
        else
            echo "linux"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    else
        echo "unknown"
    fi
}

OS=$(detect_os)
echo "Detected OS: $OS"

# Install system dependencies
case $OS in
    "ubuntu")
        echo "Installing dependencies for Ubuntu/Debian..."
        sudo apt update
        sudo apt install -y build-essential cmake
        sudo apt install -y libglfw3-dev libgl1-mesa-dev
        sudo apt install -y pkg-config
        ;;
    "centos")
        echo "Installing dependencies for CentOS/RHEL..."
        sudo yum groupinstall -y "Development Tools"
        sudo yum install -y cmake
        sudo yum install -y glfw-devel mesa-libGL-devel
        sudo yum install -y pkgconfig
        ;;
    "macos")
        echo "Installing dependencies for macOS..."
        if ! command -v brew &> /dev/null; then
            echo "Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew install cmake glfw
        ;;
    *)
        echo "❌ Unsupported OS: $OSTYPE"
        echo "Please install the following manually:"
        echo "  - CMake"
        echo "  - GLFW3"
        echo "  - OpenGL development libraries"
        exit 1
        ;;
esac

echo "✅ System dependencies installed!"

# Setup GLAD
echo "Setting up GLAD..."
if [ ! -d "include/glad" ]; then
    echo "Downloading GLAD..."
    curl -o glad.zip "https://glad.dav1d.de/generated/tmp/glad.zip"
    if [ $? -ne 0 ]; then
        echo "❌ Failed to download GLAD. Please download manually from:"
        echo "   https://glad.dav1d.de/"
        echo "   Configuration: OpenGL 3.3 Core, C/C++, glfwGetProcAddress"
        exit 1
    fi
    
    unzip -q glad.zip
    if [ $? -ne 0 ]; then
        echo "❌ Failed to extract GLAD. Please extract manually."
        exit 1
    fi
    
    # Move GLAD files to include directory
    mkdir -p include
    cp -r glad/include/* include/
    cp glad/src/glad.c include/
    
    # Clean up
    rm -rf glad glad.zip
    
    echo "✅ GLAD setup complete!"
else
    echo "✅ GLAD already exists!"
fi

# Setup GLM
echo "Setting up GLM..."
if [ ! -d "include/glm" ]; then
    echo "Cloning GLM..."
    git clone https://github.com/g-truc/glm.git include/glm
    if [ $? -ne 0 ]; then
        echo "❌ Failed to clone GLM. Please clone manually:"
        echo "   git clone https://github.com/g-truc/glm.git include/glm"
        exit 1
    fi
    echo "✅ GLM setup complete!"
else
    echo "✅ GLM already exists!"
fi

# Setup STB Image
echo "Setting up STB Image..."
if [ ! -f "include/stb_image.h" ]; then
    echo "Downloading STB Image..."
    curl -o include/stb_image.h https://raw.githubusercontent.com/nothings/stb/master/stb_image.h
    if [ $? -ne 0 ]; then
        echo "❌ Failed to download STB Image. Please download manually:"
        echo "   curl -o include/stb_image.h https://raw.githubusercontent.com/nothings/stb/master/stb_image.h"
        exit 1
    fi
    echo "✅ STB Image setup complete!"
else
    echo "✅ STB Image already exists!"
fi

echo ""
echo "🎉 All dependencies setup complete!"
echo ""
echo "Next steps:"
echo "  macOS/Linux: ./build.sh"
echo "  Windows: build.bat"
echo ""
