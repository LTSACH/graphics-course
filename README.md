# Computer Graphics Course

This repository contains sample code and demos for Computer Graphics course.

## Structure

```
Python/
└── Triangle/
    ├── simple_triangle.py              # Basic triangle demo (minimal setup)
    ├── triangle_demo.py                # Triangle with interpolated colors
    ├── triangle_pygame.py              # Triangle demo using Pygame
    ├── phong_triangle.py               # Triangle with Phong lighting
    ├── textured_triangle.py            # Triangle with texture mapping
    └── advanced_textured_triangle.py   # Advanced textured triangle with effects
```

## Triangle Demos

Six different approaches to rendering triangles in Python:

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

### 5. Textured Triangle (`textured_triangle.py`)
- Triangle with texture mapping
- Rose texture with animation effects
- Texture coordinate mapping
- Rotation and pulsing effects

### 6. Advanced Textured Triangle (`advanced_textured_triangle.py`)
- Multiple triangles with different effects
- Wave, pulse, and rotation animations
- Interactive effect switching
- Advanced texture mapping techniques

## Requirements

- Python 3.6+
- PyOpenGL (for OpenGL demos)
- NumPy
- GLFW (for OpenGL demos)
- Pygame (for pygame demo)
- Pillow (for texture loading)

## Installation

```bash
pip install PyOpenGL numpy glfw pygame pillow
```

## Usage

```bash
cd Python/Triangle

# Basic demos
python simple_triangle.py
python triangle_demo.py
python triangle_pygame.py

# Advanced demos
python phong_triangle.py
python textured_triangle.py
python advanced_textured_triangle.py
```

## Controls

- **OpenGL demos**: ESC to exit, close window to exit
- **Pygame demo**: ESC to exit, close window to exit
- **Phong Triangle**: WASD to move light, R to reset
- **Advanced Textured**: 1-3 to switch effects, WASD to move camera
