#!/usr/bin/env python3
"""
Triangle Demo - Computer Graphics with PyOpenGL
A simple demonstration of rendering a triangle using modern shader-based approach
"""

import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL import shaders
import sys
import ctypes

class TriangleRenderer:
    def __init__(self):
        self.window = None
        self.shader_program = None
        self.vao = None
        self.vbo = None
        
        # Vertex data for triangle (position + color)
        self.vertices = np.array([
            # Position (x, y, z)   # Color (r, g, b)
            -0.5, -0.5, 0.0,       1.0, 0.0, 0.0,  # Red
             0.5, -0.5, 0.0,       0.0, 1.0, 0.0,  # Green
             0.0,  0.5, 0.0,       0.0, 0.0, 1.0,  # Blue
        ], dtype=np.float32)
        
        # Vertex shader source code
        self.vertex_shader_source = """
        #version 330 core
        layout (location = 0) in vec3 position;
        layout (location = 1) in vec3 color;
        
        out vec3 fragmentColor;
        
        void main()
        {
            gl_Position = vec4(position, 1.0);
            fragmentColor = color;
        }
        """
        
        # Fragment shader source code
        self.fragment_shader_source = """
        #version 330 core
        in vec3 fragmentColor;
        out vec4 FragColor;
        
        void main()
        {
            FragColor = vec4(fragmentColor, 1.0);
        }
        """
    
    def init_glfw(self):
        """Initialize GLFW and create window"""
        if not glfw.init():
            print("Failed to initialize GLFW")
            sys.exit(-1)
        
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        
        self.window = glfw.create_window(800, 600, "Triangle Demo - Computer Graphics", None, None)
        if not self.window:
            print("Failed to create GLFW window")
            glfw.terminate()
            sys.exit(-1)
        
        glfw.make_context_current(self.window)
        glfw.set_framebuffer_size_callback(self.window, self.framebuffer_size_callback)
    
    def framebuffer_size_callback(self, window, width, height):
        """Callback for window resize"""
        glViewport(0, 0, width, height)
    
    def create_shaders(self):
        """Create and compile shaders"""
        try:
            # Compile vertex shader
            vertex_shader = glCreateShader(GL_VERTEX_SHADER)
            glShaderSource(vertex_shader, self.vertex_shader_source)
            glCompileShader(vertex_shader)
            
            # Check vertex shader compilation
            if not glGetShaderiv(vertex_shader, GL_COMPILE_STATUS):
                error = glGetShaderInfoLog(vertex_shader)
                print(f"Vertex shader compilation error: {error}")
                return False
            
            # Compile fragment shader
            fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
            glShaderSource(fragment_shader, self.fragment_shader_source)
            glCompileShader(fragment_shader)
            
            # Check fragment shader compilation
            if not glGetShaderiv(fragment_shader, GL_COMPILE_STATUS):
                error = glGetShaderInfoLog(fragment_shader)
                print(f"Fragment shader compilation error: {error}")
                return False
            
            # Create shader program
            self.shader_program = glCreateProgram()
            glAttachShader(self.shader_program, vertex_shader)
            glAttachShader(self.shader_program, fragment_shader)
            glLinkProgram(self.shader_program)
            
            # Check program linking
            if not glGetProgramiv(self.shader_program, GL_LINK_STATUS):
                error = glGetProgramInfoLog(self.shader_program)
                print(f"Shader program linking error: {error}")
                return False
            
            # Clean up shaders
            glDeleteShader(vertex_shader)
            glDeleteShader(fragment_shader)
            
            return True
            
        except Exception as e:
            print(f"Error creating shaders: {e}")
            return False
    
    def setup_buffers(self):
        """Setup vertex buffer and vertex array objects"""
        # Create VAO
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        
        # Create VBO
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        
        # Position attribute (location = 0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * 4, None)
        glEnableVertexAttribArray(0)
        
        # Color attribute (location = 1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(3 * 4))
        glEnableVertexAttribArray(1)
        
        # Unbind
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
    
    def render(self):
        """Render the triangle"""
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        
        glUseProgram(self.shader_program)
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        
        glfw.swap_buffers(self.window)
        glfw.poll_events()
    
    def run(self):
        """Main render loop"""
        self.init_glfw()
        
        if not self.create_shaders():
            print("Failed to create shaders")
            return
        
        self.setup_buffers()
        
        print("Triangle Demo is running!")
        print("Press ESC or close window to exit")
        
        while not glfw.window_should_close(self.window):
            self.render()
            
            # Handle input
            if glfw.get_key(self.window, glfw.KEY_ESCAPE) == glfw.PRESS:
                glfw.set_window_should_close(self.window, True)
        
        self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        if self.vao:
            glDeleteVertexArrays(1, [self.vao])
        if self.vbo:
            glDeleteBuffers(1, [self.vbo])
        if self.shader_program:
            glDeleteProgram(self.shader_program)
        
        glfw.terminate()

def main():
    """Main function"""
    try:
        renderer = TriangleRenderer()
        renderer.run()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(-1)

if __name__ == "__main__":
    main()
