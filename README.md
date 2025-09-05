# Computer Graphics Course

This repository contains sample code and demos for Computer Graphics course.

## Structure

```
Python/
└── Triangle/
    ├── simple_triangle.py      # Basic triangle demo (minimal setup)
    ├── triangle_demo.py        # Triangle with interpolated colors
    └── triangle_pygame.py      # Triangle demo using Pygame
```

## Triangle Demos

Three different approaches to rendering triangles in Python:

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

## Requirements

- Python 3.6+
- PyOpenGL (for OpenGL demos)
- NumPy
- GLFW (for OpenGL demos)
- Pygame (for pygame demo)

## Installation

```bash
pip install PyOpenGL numpy glfw pygame
```

## Usage

```bash
cd Python/Triangle

# Run simple triangle demo
python simple_triangle.py

# Run triangle with interpolated colors
python triangle_demo.py

# Run triangle using Pygame
python triangle_pygame.py
```

## Controls

- **OpenGL demos**: ESC to exit, close window to exit
- **Pygame demo**: ESC to exit, close window to exit
