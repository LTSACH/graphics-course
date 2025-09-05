#!/usr/bin/env python3
"""
Simple Triangle Demo - Basic PyOpenGL Triangle
A minimal example for testing PyOpenGL installation
"""

import glfw
import numpy as np
from OpenGL.GL import *
import sys

def main():
    # Initialize GLFW
    if not glfw.init():
        print("Failed to initialize GLFW")
        return
    
    # Create window with OpenGL 3.3 Core Profile (modern approach)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    
    window = glfw.create_window(800, 600, "Simple Triangle", None, None)
    if not window:
        print("Failed to create GLFW window")
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    
    # Triangle vertices (position only)
    vertices = np.array([
        -0.5, -0.5, 0.0,  # Left
         0.5, -0.5, 0.0,  # Right
         0.0,  0.5, 0.0   # Top
    ], dtype=np.float32)
    
    # Create simple shaders
    vertex_shader_source = """
    #version 330 core
    layout (location = 0) in vec3 position;
    
    void main()
    {
        gl_Position = vec4(position, 1.0);
    }
    """
    
    fragment_shader_source = """
    #version 330 core
    out vec4 FragColor;
    
    void main()
    {
        FragColor = vec4(1.0, 0.5, 0.2, 1.0); // Orange color
    }
    """
    
    # Compile and link shaders
    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex_shader, vertex_shader_source)
    glCompileShader(vertex_shader)
    
    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader, fragment_shader_source)
    glCompileShader(fragment_shader)
    
    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)
    
    # Clean up shaders
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)
    
    # Create and bind VAO
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)
    
    # Create and bind VBO
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    
    # Set vertex attributes
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, None)
    glEnableVertexAttribArray(0)
    
    # Unbind
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)
    
    print("Simple Triangle Demo is running!")
    print("Press ESC or close window to exit")
    
    # Render loop
    while not glfw.window_should_close(window):
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        
        # Use modern shader-based rendering
        glUseProgram(shader_program)
        glBindVertexArray(vao)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        
        glfw.swap_buffers(window)
        glfw.poll_events()
        
        # Handle ESC key
        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(window, True)
    
    # Cleanup
    glDeleteVertexArrays(1, [vao])
    glDeleteBuffers(1, [vbo])
    glDeleteProgram(shader_program)
    glfw.terminate()

if __name__ == "__main__":
    main()
