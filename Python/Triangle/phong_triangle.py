#!/usr/bin/env python3
"""
Simple Phong Shading Triangle Demo
Very basic version to ensure triangle is visible.
"""

import numpy as np
import glfw
from OpenGL.GL import *
import math
import random

class PhongTriangle:
    def __init__(self):
        self.window = None
        self.shader_program = None
        self.vao = None
        self.vbo = None
        
        # Simple triangle vertices (3D positions + normals)
        self.vertices = np.array([
            # Position (x, y, z), Normal (nx, ny, nz)
            -0.5, -0.5, 0.0,  0.0, 0.0, 1.0,  # Bottom left
             0.5, -0.5, 0.0,  0.0, 0.0, 1.0,  # Bottom right
             0.0,  0.5, 0.0,  0.0, 0.0, 1.0,  # Top center
        ], dtype=np.float32)
        
        # Animation parameters
        self.rotation_angle = 0.0
        self.time = 0.0
        
    def init_glfw(self):
        """Initialize GLFW and create window"""
        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")
        
        # Set OpenGL version to 3.3 Core Profile
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
        
        # Create window
        self.window = glfw.create_window(800, 600, "Simple Phong Triangle", None, None)
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Failed to create GLFW window")
        
        glfw.make_context_current(self.window)
        glfw.set_window_size_callback(self.window, self.window_size_callback)
        
        # Enable depth testing
        glEnable(GL_DEPTH_TEST)
        
    def window_size_callback(self, window, width, height):
        """Handle window resize"""
        glViewport(0, 0, width, height)
        
    def create_shaders(self):
        """Create and compile shaders"""
        # Very simple vertex shader
        vertex_shader_source = """
        #version 330 core
        layout (location = 0) in vec3 aPos;
        layout (location = 1) in vec3 aNormal;
        
        uniform mat4 mvp;
        
        out vec3 Normal;
        out vec3 FragPos;
        
        void main()
        {
            FragPos = aPos;
            Normal = aNormal;
            gl_Position = mvp * vec4(aPos, 1.0);
        }
        """
        
        # Simple fragment shader with basic lighting
        fragment_shader_source = """
        #version 330 core
        out vec4 FragColor;
        
        in vec3 Normal;
        in vec3 FragPos;
        
        uniform vec3 lightPos;
        uniform vec3 lightColor;
        uniform vec3 objectColor;
        
        void main()
        {
            // Ambient lighting
            float ambient = 0.3;
            vec3 ambientColor = ambient * lightColor;
            
            // Diffuse lighting
            vec3 norm = normalize(Normal);
            vec3 lightDir = normalize(lightPos - FragPos);
            float diff = max(dot(norm, lightDir), 0.0);
            vec3 diffuseColor = diff * lightColor;
            
            // Combine lighting
            vec3 result = (ambientColor + diffuseColor) * objectColor;
            FragColor = vec4(result, 1.0);
        }
        """
        
        # Compile vertex shader
        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex_shader, vertex_shader_source)
        glCompileShader(vertex_shader)
        
        # Check vertex shader compilation
        success = glGetShaderiv(vertex_shader, GL_COMPILE_STATUS)
        if not success:
            info_log = glGetShaderInfoLog(vertex_shader)
            raise RuntimeError(f"Vertex shader compilation failed: {info_log}")
        
        # Compile fragment shader
        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment_shader, fragment_shader_source)
        glCompileShader(fragment_shader)
        
        # Check fragment shader compilation
        success = glGetShaderiv(fragment_shader, GL_COMPILE_STATUS)
        if not success:
            info_log = glGetShaderInfoLog(fragment_shader)
            raise RuntimeError(f"Fragment shader compilation failed: {info_log}")
        
        # Create shader program
        self.shader_program = glCreateProgram()
        glAttachShader(self.shader_program, vertex_shader)
        glAttachShader(self.shader_program, fragment_shader)
        glLinkProgram(self.shader_program)
        
        # Check program linking
        success = glGetProgramiv(self.shader_program, GL_LINK_STATUS)
        if not success:
            info_log = glGetProgramInfoLog(self.shader_program)
            raise RuntimeError(f"Shader program linking failed: {info_log}")
        
        # Clean up shaders
        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)
        
    def setup_buffers(self):
        """Setup VAO and VBO"""
        # Generate and bind VAO
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        
        # Generate and bind VBO
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        
        # Position attribute (location = 0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        
        # Normal attribute (location = 1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(3 * 4))
        glEnableVertexAttribArray(1)
        
        # Unbind
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        
    def generate_random_normals(self):
        """Generate random normals for demonstration"""
        print("Generating random normals...")
        
        # Generate random normals for each vertex
        for i in range(3):  # 3 vertices
            # Generate random normal vector
            nx = random.uniform(-1.0, 1.0)
            ny = random.uniform(-1.0, 1.0)
            nz = random.uniform(0.0, 1.0)  # Keep Z positive for visibility
            
            # Normalize the vector
            length = math.sqrt(nx*nx + ny*ny + nz*nz)
            nx /= length
            ny /= length
            nz /= length
            
            # Update the normal in vertices array (positions 3,4,5 for each vertex)
            vertex_offset = i * 6
            self.vertices[vertex_offset + 3] = nx
            self.vertices[vertex_offset + 4] = ny
            self.vertices[vertex_offset + 5] = nz
            
            print(f"Vertex {i}: Normal = ({nx:.3f}, {ny:.3f}, {nz:.3f})")
        
        # Update VBO with new normals
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferSubData(GL_ARRAY_BUFFER, 0, self.vertices.nbytes, self.vertices)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        
    def create_mvp_matrix(self):
        """Create Model-View-Projection matrix"""
        # Model matrix (rotation around Y axis)
        model = np.eye(4, dtype=np.float32)
        cos_angle = math.cos(self.rotation_angle)
        sin_angle = math.sin(self.rotation_angle)
        model[0, 0] = cos_angle
        model[0, 2] = sin_angle
        model[2, 0] = -sin_angle
        model[2, 2] = cos_angle
        
        # View matrix (camera looking at origin)
        view = np.eye(4, dtype=np.float32)
        view[2, 3] = -3.0  # Move camera back
        
        # Projection matrix (perspective)
        fov = 45.0
        aspect = 800.0 / 600.0
        near = 0.1
        far = 100.0
        
        projection = np.zeros((4, 4), dtype=np.float32)
        f = 1.0 / math.tan(math.radians(fov) / 2.0)
        projection[0, 0] = f / aspect
        projection[1, 1] = f
        projection[2, 2] = (far + near) / (near - far)
        projection[2, 3] = (2 * far * near) / (near - far)
        projection[3, 2] = -1.0
        
        # Combine matrices: MVP = Projection * View * Model
        mvp = np.dot(projection, np.dot(view, model))
        return mvp
        
    def render(self):
        """Render the triangle"""
        # Clear screen with a light blue color
        glClearColor(0.2, 0.3, 0.5, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Use shader program
        glUseProgram(self.shader_program)
        
        # Create and set MVP matrix
        mvp = self.create_mvp_matrix()
        mvp_loc = glGetUniformLocation(self.shader_program, "mvp")
        glUniformMatrix4fv(mvp_loc, 1, GL_FALSE, mvp)
        
        # Set lighting uniforms
        light_pos_loc = glGetUniformLocation(self.shader_program, "lightPos")
        light_color_loc = glGetUniformLocation(self.shader_program, "lightColor")
        object_color_loc = glGetUniformLocation(self.shader_program, "objectColor")
        
        glUniform3f(light_pos_loc, 1.0, 1.0, 2.0)  # Light position
        glUniform3f(light_color_loc, 1.0, 1.0, 1.0)  # White light
        glUniform3f(object_color_loc, 0.8, 0.2, 0.2)  # Red color
        
        # Draw triangle
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        
        # Swap buffers
        glfw.swap_buffers(self.window)
        
    def run(self):
        """Main render loop"""
        print("Simple Phong Triangle Demo")
        print("Controls:")
        print("  R - Generate new random normals")
        print("  ESC - Exit")
        
        while not glfw.window_should_close(self.window):
            # Update time and rotation
            self.time = glfw.get_time()
            self.rotation_angle = self.time * 0.5  # Slow rotation
            
            # Handle input
            glfw.poll_events()
            
            # Check for key presses
            if glfw.get_key(self.window, glfw.KEY_R) == glfw.PRESS:
                self.generate_random_normals()
                glfw.wait_events_timeout(0.1)  # Prevent multiple triggers
                
            if glfw.get_key(self.window, glfw.KEY_ESCAPE) == glfw.PRESS:
                glfw.set_window_should_close(self.window, True)
            
            # Render
            self.render()
            
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
        demo = PhongTriangle()
        demo.init_glfw()
        demo.create_shaders()
        demo.setup_buffers()
        demo.generate_random_normals()  # Start with random normals
        demo.run()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if 'demo' in locals():
            demo.cleanup()

if __name__ == "__main__":
    main()
