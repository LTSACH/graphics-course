# Computer Graphics C++ Demos

Cross-platform OpenGL demos using C++ with GLAD, GLM, GLFW, and STB Image.

## 🎯 Features

- **Cross-platform**: Windows, macOS, Linux
- **Modern OpenGL**: OpenGL 3.3 Core Profile
- **Triangle Demos**: Basic, Advanced, Phong Lighting, and Textured
- **Image Loading**: STB Image for PNG, JPG, BMP support
- **Official Libraries**: GLAD, GLM, GLFW, STB Image

## 📋 Prerequisites

### System Requirements
- **CMake** 3.10 or higher
- **C++ Compiler** (C++17 support)
- **OpenGL** 3.3 or higher

### Platform-specific Requirements

#### Windows
- **Visual Studio 2019** or later (with C++ workload)
- **vcpkg** (recommended) or manual GLFW installation

#### macOS
- **Xcode Command Line Tools**
- **Homebrew** (for package management)

#### Linux
- **Build tools**: `build-essential` (Ubuntu/Debian) or `Development Tools` (CentOS/RHEL)
- **OpenGL development libraries**

## 🚀 Quick Start

### Option 1: Automated Setup (macOS/Linux)

```bash
# Run automated setup
./setup_dependencies.sh

# Build the project
./build.sh
```

### Option 2: Manual Setup

#### Step 1: Install System Dependencies

**Windows:**
```cmd
# Install vcpkg
git clone https://github.com/Microsoft/vcpkg.git
cd vcpkg
.\bootstrap-vcpkg.bat
.\vcpkg install glfw3:x64-windows
```

**macOS:**
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install cmake glfw
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install build-essential cmake
sudo apt install libglfw3-dev libgl1-mesa-dev
sudo apt install pkg-config
```

**Linux (CentOS/RHEL):**
```bash
sudo yum groupinstall "Development Tools"
sudo yum install cmake
sudo yum install glfw-devel mesa-libGL-devel
sudo yum install pkgconfig
```

#### Step 2: Setup GLAD

1. Go to [GLAD Generator](https://glad.dav1d.de/)
2. Configure:
   - **Language**: C/C++
   - **Specification**: OpenGL
   - **gl**: 3.3
   - **Profile**: Core
   - **Extensions**: (leave empty)
   - **Options**: ✓ Generate a loader
3. Click **Generate**
4. Download the ZIP file
5. Extract to project directory:
   ```bash
   unzip glad.zip
   mkdir -p include
   cp -r glad/include/* include/
   cp glad/src/glad.c include/
   rm -rf glad glad.zip
   ```

#### Step 3: Setup GLM

```bash
git clone https://github.com/g-truc/glm.git include/glm
```

#### Step 4: Setup STB Image

```bash
# Download STB Image header
curl -o include/stb_image.h https://raw.githubusercontent.com/nothings/stb/master/stb_image.h
```

**Alternative method:**
```bash
# Clone STB repository
git clone https://github.com/nothings/stb.git
cp stb/stb_image.h include/
rm -rf stb
```

#### Step 5: Build the Project

**Windows:**
```cmd
build.bat
```

**macOS/Linux:**
```bash
./build.sh
```

**Linux (alternative):**
```bash
./build_linux.sh
```

## 🎮 Running the Demos

### Windows
```cmd
cd build
.\Release\simple_triangle.exe
.\Release\triangle_demo.exe
.\Release\phong_triangle.exe
.\Release\textured_triangle.exe
.\Release\rose_textured_triangle.exe
```

### macOS/Linux
```bash
cd build
./bin/simple_triangle
./bin/triangle_demo
./bin/phong_triangle
./bin/textured_triangle
./bin/rose_textured_triangle
```

## 🎮 Demo Controls

### Simple Triangle
- **ESC**: Exit

### Triangle Demo
- **ESC**: Exit
- **Mouse**: Rotate view

### Phong Triangle
- **ESC**: Exit
- **R**: Red color
- **G**: Green color
- **B**: Blue color
- **Y**: Yellow color

### Textured Triangle
- **ESC**: Exit
- **R**: Red tint
- **G**: Green tint
- **B**: Blue tint
- **W**: White (no tint)

### Rose Textured Triangle
- **ESC**: Exit
- **R**: Red tint
- **G**: Green tint
- **B**: Blue tint
- **W**: White (no tint)

## 📁 Project Structure

```
CPP/
├── include/
│   ├── glad/
│   │   └── glad.h          # GLAD header
│   ├── KHR/
│   │   └── khrplatform.h   # Khronos platform header
│   ├── glad.c              # GLAD implementation
│   ├── stb_image.h         # STB Image header
│   └── glm/                # GLM math library
├── Triangle/
│   ├── simple_triangle.cpp      # Basic triangle demo
│   ├── triangle_demo.cpp        # Advanced triangle demo
│   ├── phong_triangle.cpp       # Phong lighting demo
│   ├── textured_triangle.cpp    # Procedural texture demo
│   ├── rose_textured_triangle.cpp # Rose texture demo
│   ├── rose.png                 # Rose texture image
│   └── CMakeLists.txt           # Build configuration
├── build.sh               # macOS/Linux build script
├── build.bat              # Windows build script
├── build_linux.sh         # Linux-specific build script
├── setup_dependencies.sh  # Automated dependency setup
├── CMakeLists.txt         # Main CMake configuration
└── README.md              # This file
```

## 🔧 Manual Build (Advanced)

If you prefer to build manually:

```bash
# Create build directory
mkdir build
cd build

# Configure with CMake
cmake ..

# Build
make -j$(nproc)  # Linux/macOS
# or
cmake --build . --config Release  # Windows
```

## 🐛 Troubleshooting

### Common Issues

#### "CMake not found"
- **Windows**: Install CMake from https://cmake.org/download/
- **macOS**: `brew install cmake`
- **Linux**: `sudo apt install cmake` or `sudo yum install cmake`

#### "GLFW not found"
- **Windows**: Use vcpkg or download GLFW binaries
- **macOS**: `brew install glfw`
- **Linux**: `sudo apt install libglfw3-dev`

#### "OpenGL not found"
- **Windows**: Install graphics drivers
- **macOS**: Usually built-in
- **Linux**: `sudo apt install libgl1-mesa-dev`

#### "GLAD compilation failed"
- Ensure GLAD was generated for OpenGL 3.3 Core
- Check that `glad.c` and `glad.h` are in the correct locations

#### "GLM not found"
- Ensure GLM was cloned to `include/glm/`
- Check CMakeLists.txt includes the correct path

#### "STB Image not found"
- Ensure `stb_image.h` is in `include/` directory
- Check that `#define STB_IMAGE_IMPLEMENTATION` is included before `#include "stb_image.h"`

#### "Failed to load rose.png"
- Ensure `rose.png` is in the same directory as the executable
- Check file permissions and path

### Platform-specific Issues

#### Windows
- Use **Visual Studio 2019** or later
- Ensure **C++ workload** is installed
- Use **x64** configuration

#### macOS
- Install **Xcode Command Line Tools**: `xcode-select --install`
- Use **Homebrew** for package management

#### Linux
- Install **build-essential** or **Development Tools**
- Ensure **OpenGL drivers** are installed
- Use **pkg-config** for library detection

## 📚 Dependencies

| Library | Version | Purpose | License |
|---------|---------|---------|---------|
| **GLAD** | 0.1.36 | OpenGL function loading | MIT |
| **GLM** | Latest | Mathematics library | MIT |
| **GLFW** | 3.3+ | Window management | Zlib |
| **STB Image** | Latest | Image loading (PNG, JPG, BMP) | Public Domain |
| **OpenGL** | 3.3+ | Graphics API | - |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on multiple platforms
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **GLAD**: OpenGL Loader Generator by David Herberth
- **GLM**: OpenGL Mathematics by G-Truc Creation
- **GLFW**: Multi-platform library for OpenGL by Marcus Geelnard
- **STB Image**: Single header image loading library by Sean Barrett
- **OpenGL**: Graphics API by Khronos Group
