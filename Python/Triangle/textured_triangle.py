#!/usr/bin/env python3
"""
Textured Triangle Demo
Demonstrates texture mapping with a rose texture.
"""

import numpy as np
import glfw
from OpenGL.GL import *
import math
from PIL import Image

class TexturedTriangleDemo:
    def __init__(self):
        self.window = None
        self.shader_program = None
        self.vao = None
        self.vbo = None
        self.texture = None
        
        # Triangle vertices with texture coordinates
        # Position (x, y, z), Texture coordinates (u, v)
        self.vertices = np.array([
            -0.5, -0.5, 0.0,  0.0, 0.0,  # Bottom left
             0.5, -0.5, 0.0,  1.0, 0.0,  # Bottom right
             0.0,  0.5, 0.0,  0.5, 1.0,  # Top center
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
        self.window = glfw.create_window(800, 600, "Textured Triangle Demo", None, None)
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
        # Vertex shader source
        vertex_shader_source = """
        #version 330 core
        layout (location = 0) in vec3 aPos;
        layout (location = 1) in vec2 aTexCoord;
        
        uniform mat4 mvp;
        
        out vec2 TexCoord;
        
        void main()
        {
            gl_Position = mvp * vec4(aPos, 1.0);
            TexCoord = aTexCoord;
        }
        """
        
        # Fragment shader source with texture sampling
        fragment_shader_source = """
        #version 330 core
        out vec4 FragColor;
        
        in vec2 TexCoord;
        
        uniform sampler2D ourTexture;
        uniform float time;
        
        void main()
        {
            // Sample the texture
            vec4 texColor = texture(ourTexture, TexCoord);
            
            // Add some animation effect
            float pulse = sin(time * 2.0) * 0.1 + 0.9;
            texColor.rgb *= pulse;
            
            FragColor = texColor;
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
        
    def load_texture(self, image_path):
        """Load texture from image file"""
        try:
            # Load image using PIL
            img = Image.open(image_path)
            
            # Convert to RGBA if not already
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Flip image vertically to match OpenGL coordinate system
            # (OpenGL has (0,0) at bottom-left, images have (0,0) at top-left)
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
            
            # Get image data
            img_data = np.array(img, dtype=np.uint8)
            width, height = img.size
            
            # Generate texture
            self.texture = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.texture)
            
            # Set texture parameters
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            
            # Upload texture data
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
            
            print(f"Texture loaded successfully: {width}x{height}")
            return True
            
        except Exception as e:
            print(f"Failed to load texture: {e}")
            return False
            
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
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        
        # Texture coordinate attribute (location = 1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * 4, ctypes.c_void_p(3 * 4))
        glEnableVertexAttribArray(1)
        
        # Unbind
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        
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
        """Render the textured triangle"""
        # Clear screen
        glClearColor(0.2, 0.3, 0.5, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Use shader program
        glUseProgram(self.shader_program)
        
        # Create and set MVP matrix
        mvp = self.create_mvp_matrix()
        mvp_loc = glGetUniformLocation(self.shader_program, "mvp")
        glUniformMatrix4fv(mvp_loc, 1, GL_FALSE, mvp)
        
        # Set time uniform for animation
        time_loc = glGetUniformLocation(self.shader_program, "time")
        glUniform1f(time_loc, self.time)
        
        # Bind texture
        if self.texture:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.texture)
            texture_loc = glGetUniformLocation(self.shader_program, "ourTexture")
            glUniform1i(texture_loc, 0)
        
        # Draw triangle
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, 3)
        
        # Swap buffers
        glfw.swap_buffers(self.window)
        
    def run(self):
        """Main render loop"""
        print("Textured Triangle Demo")
        print("Controls:")
        print("  ESC - Exit")
        print("  Window Resize - Automatically adjusts viewport")
        
        while not glfw.window_should_close(self.window):
            # Update time and rotation
            self.time = glfw.get_time()
            self.rotation_angle = self.time * 0.5  # Slow rotation
            
            # Handle input
            glfw.poll_events()
            
            # Check for key presses
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
        if self.texture:
            glDeleteTextures(1, [self.texture])
        if self.shader_program:
            glDeleteProgram(self.shader_program)
        glfw.terminate()

def main():
    """Main function"""
    try:
        demo = TexturedTriangleDemo()
        demo.init_glfw()
        demo.create_shaders()
        demo.setup_buffers()
        
        # Load texture
        if not demo.load_texture('rose.png'):
            print("Warning: Could not load rose.png, using fallback")
            # Create a simple colored triangle as fallback
            demo.vertices = np.array([
                -0.5, -0.5, 0.0,  0.0, 0.0,  # Bottom left
                 0.5, -0.5, 0.0,  1.0, 0.0,  # Bottom right
                 0.0,  0.5, 0.0,  0.5, 1.0,  # Top center
            ], dtype=np.float32)
        
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
