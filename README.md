# Computer Graphics Course

This repository contains sample code and demos for Computer Graphics course in both Python and C++.

## Structure

```
Python/
└── Triangle/
    ├── simple_triangle.py              # Basic triangle demo (minimal setup)
    ├── triangle_demo.py                # Triangle with interpolated colors
    ├── triangle_pygame.py              # Triangle demo using Pygame
    ├── phong_triangle.py               # Triangle with Phong lighting
    ├── advanced_phong_triangle.py      # Advanced Phong lighting with multiple lights
    ├── textured_triangle.py            # Triangle with texture mapping
    └── advanced_textured_triangle.py   # Advanced textured triangle with effects

CPP/
├── include/                            # Libraries (GLAD, GLM, STB Image)
├── Triangle/                           # C++ Triangle demos
│   ├── simple_triangle.cpp             # Basic triangle demo
│   ├── triangle_demo.cpp               # Advanced triangle demo
│   ├── phong_triangle.cpp              # Phong lighting demo
│   ├── textured_triangle.cpp           # Procedural texture demo
│   ├── rose_textured_triangle.cpp      # Rose texture demo
│   └── rose.png                        # Rose texture image
├── build.sh                            # macOS/Linux build script
├── build.bat                           # Windows build script
├── setup_dependencies.sh               # Automated dependency setup
└── README.md                           # C++ specific documentation
```

## Triangle Demos

### Python Demos

Seven different approaches to rendering triangles in Python:

### 1. Simple Triangle (`simple_triangle.py`)
- Basic triangle rendering with minimal setup
- Single color triangle
- Good for understanding fundamentals

### 2. Triangle Demo (`triangle_demo.py`)
- Triangle with interpolated colors (red, green, blue vertices)
- Modern OpenGL Core Profile (3.3+)
- Vertex and Fragment Shaders
- VAO/VBO setup
- GLFW window management

### 3. Triangle Pygame (`triangle_pygame.py`)
- Triangle rendering using Pygame
- Alternative approach for beginners
- Simpler setup than OpenGL

### 4. Phong Triangle (`phong_triangle.py`)
- Triangle with Phong lighting model
- Demonstrates lighting calculations
- Normal vectors and material properties
- Interactive lighting controls

### 5. Advanced Phong Triangle (`advanced_phong_triangle.py`)
- Multiple light sources (directional, point, spot)
- Advanced Phong lighting calculations
- Interactive light positioning
- Material property controls

### 6. Textured Triangle (`textured_triangle.py`)
- Triangle with texture mapping
- Rose texture with animation effects
- Texture coordinate mapping
- Rotation and pulsing effects

### 7. Advanced Textured Triangle (`advanced_textured_triangle.py`)
- Multiple triangles with different effects
- Wave, pulse, and rotation animations
- Interactive effect switching
- Advanced texture mapping techniques

### C++ Demos

Five different approaches to rendering triangles in C++:

### 1. Simple Triangle (`simple_triangle.cpp`)
- Basic triangle rendering with minimal setup
- Single color triangle
- Cross-platform OpenGL setup

### 2. Triangle Demo (`triangle_demo.cpp`)
- Triangle with interpolated colors
- Modern OpenGL Core Profile (3.3+)
- GLAD for OpenGL function loading
- GLM for mathematics

### 3. Phong Triangle (`phong_triangle.cpp`)
- Triangle with Phong lighting model
- Demonstrates lighting calculations
- Normal vectors and material properties
- Interactive lighting controls

### 4. Textured Triangle (`textured_triangle.cpp`)
- Triangle with procedural checkerboard texture
- Texture coordinate mapping
- Rotation and color tinting effects

### 5. Rose Textured Triangle (`rose_textured_triangle.cpp`)
- Triangle with external image texture (rose.png)
- STB Image for image loading
- Texture flipping for correct orientation
- Interactive color tinting

## Requirements

### Python Requirements

- Python 3.6+
- PyOpenGL (for OpenGL demos)
- NumPy
- GLFW (for OpenGL demos)
- Pygame (for pygame demo)
- Pillow (for texture loading)

### C++ Requirements

- **CMake** 3.10 or higher
- **C++ Compiler** (C++17 support)
- **OpenGL** 3.3 or higher
- **GLFW** (window management)
- **GLAD** (OpenGL function loading)
- **GLM** (mathematics library)
- **STB Image** (image loading)

## Installation

### Python Installation

```bash
pip install PyOpenGL numpy glfw pygame pillow
```

### C++ Installation

#### Automated Setup (macOS/Linux)
```bash
cd CPP
./setup_dependencies.sh
./build.sh
```

#### Manual Setup
See [CPP/README.md](CPP/README.md) for detailed instructions.

## Usage

### Python Demos

```bash
cd Python/Triangle

# Basic demos
python simple_triangle.py
python triangle_demo.py
python triangle_pygame.py

# Advanced demos
python phong_triangle.py
python advanced_phong_triangle.py
python textured_triangle.py
python advanced_textured_triangle.py
```

### C++ Demos

```bash
cd CPP/build

# macOS/Linux
./bin/simple_triangle
./bin/triangle_demo
./bin/phong_triangle
./bin/textured_triangle
./bin/rose_textured_triangle

# Windows
.\Release\simple_triangle.exe
.\Release\triangle_demo.exe
.\Release\phong_triangle.exe
.\Release\textured_triangle.exe
.\Release\rose_textured_triangle.exe
```

## Controls

### Python Demos
- **OpenGL demos**: ESC to exit, close window to exit
- **Pygame demo**: ESC to exit, close window to exit
- **Phong Triangle**: WASD to move light, R to reset
- **Advanced Phong**: WASD to move lights, 1-3 to switch light types, R to reset
- **Advanced Textured**: 1-3 to switch effects, WASD to move camera

### C++ Demos
- **All demos**: ESC to exit
- **Triangle Demo**: Mouse to rotate view
- **Phong Triangle**: R/G/B/Y for colors
- **Textured Triangle**: R/G/B/W for color tinting
- **Rose Textured Triangle**: R/G/B/W for color tinting

## Comparison

| Feature | Python | C++ |
|---------|--------|-----|
| **Setup** | Simple pip install | CMake + dependencies |
| **Performance** | Slower | Faster |
| **Cross-platform** | ✅ | ✅ |
| **Dependencies** | Many | Few |
| **Learning curve** | Easy | Moderate |
| **Production use** | Prototyping | Production |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test on multiple platforms
5. Submit a pull request

## License

This project is licensed under the MIT License.
