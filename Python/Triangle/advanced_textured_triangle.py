#!/usr/bin/env python3
"""
Advanced Textured Triangle Demo
Multiple triangles with different textures and effects.
"""

import numpy as np
import glfw
from OpenGL.GL import *
import math
from PIL import Image

class AdvancedTexturedTriangleDemo:
    def __init__(self):
        self.window = None
        self.shader_program = None
        self.vao = None
        self.vbo = None
        self.textures = []
        
        # Multiple triangles with different textures
        self.triangles = []
        self.generate_triangles()
        
        # Animation parameters
        self.rotation_angle = 0.0
        self.time = 0.0
        
        # Interactive parameters
        self.current_effect = 0
        self.texture_scale = 1.0
        self.brightness = 1.0
        
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
        self.window = glfw.create_window(1000, 800, "Advanced Textured Triangle Demo", None, None)
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Failed to create GLFW window")
        
        glfw.make_context_current(self.window)
        glfw.set_window_size_callback(self.window, self.window_size_callback)
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.set_cursor_pos_callback(self.window, self.cursor_callback)
        glfw.set_scroll_callback(self.window, self.scroll_callback)
        
        # Enable depth testing
        glEnable(GL_DEPTH_TEST)
        
        # Mouse state
        self.mouse_x = 0.0
        self.mouse_y = 0.0
        self.camera_angle_x = 0.0
        self.camera_angle_y = 0.0
        self.zoom = 1.0
        
    def window_size_callback(self, window, width, height):
        """Handle window resize"""
        glViewport(0, 0, width, height)
        
    def key_callback(self, window, key, scancode, action, mods):
        """Handle keyboard input"""
        if action == glfw.PRESS or action == glfw.REPEAT:
            if key == glfw.KEY_E:
                self.current_effect = (self.current_effect + 1) % 4
                print(f"Effect: {['Normal', 'Wave', 'Pulse', 'Rainbow'][self.current_effect]}")
            elif key == glfw.KEY_UP:
                self.brightness = min(2.0, self.brightness + 0.1)
                print(f"Brightness: {self.brightness:.1f}")
            elif key == glfw.KEY_DOWN:
                self.brightness = max(0.1, self.brightness - 0.1)
                print(f"Brightness: {self.brightness:.1f}")
            elif key == glfw.KEY_ESCAPE:
                glfw.set_window_should_close(window, True)
                
    def cursor_callback(self, window, xpos, ypos):
        """Handle mouse movement for camera control"""
        if glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS:
            dx = xpos - self.mouse_x
            dy = ypos - self.mouse_y
            self.camera_angle_y += dx * 0.01
            self.camera_angle_x += dy * 0.01
            self.camera_angle_x = max(-math.pi/2, min(math.pi/2, self.camera_angle_x))
        
        self.mouse_x = xpos
        self.mouse_y = ypos
        
    def scroll_callback(self, window, xoffset, yoffset):
        """Handle mouse scroll for zoom"""
        self.zoom *= (1.0 + yoffset * 0.1)
        self.zoom = max(0.1, min(5.0, self.zoom))
        
    def generate_triangles(self):
        """Generate multiple triangles with different textures"""
        # Triangle 1: Rose texture
        triangle1 = np.array([
            # Position (x, y, z), Texture coordinates (u, v)
            -1.0, -0.5, 0.0,  0.0, 0.0,  # Bottom left
             0.0, -0.5, 0.0,  1.0, 0.0,  # Bottom right
            -0.5,  0.5, 0.0,  0.5, 1.0,  # Top center
        ], dtype=np.float32)
        
        # Triangle 2: Rose texture (mirrored)
        triangle2 = np.array([
            # Position (x, y, z), Texture coordinates (u, v)
             0.0, -0.5, 0.0,  1.0, 0.0,  # Bottom left
             1.0, -0.5, 0.0,  0.0, 0.0,  # Bottom right
             0.5,  0.5, 0.0,  0.5, 1.0,  # Top center
        ], dtype=np.float32)
        
        # Triangle 3: Rose texture (rotated)
        triangle3 = np.array([
            # Position (x, y, z), Texture coordinates (u, v)
            -0.5,  0.0, 0.0,  0.0, 1.0,  # Left
             0.5,  0.0, 0.0,  1.0, 1.0,  # Right
             0.0,  1.0, 0.0,  0.5, 0.0,  # Top
        ], dtype=np.float32)
        
        self.triangles = [triangle1, triangle2, triangle3]
        
    def create_shaders(self):
        """Create and compile shaders"""
        # Vertex shader source
        vertex_shader_source = """
        #version 330 core
        layout (location = 0) in vec3 aPos;
        layout (location = 1) in vec2 aTexCoord;
        
        uniform mat4 mvp;
        uniform float time;
        uniform int effect;
        
        out vec2 TexCoord;
        out float VertexTime;
        
        void main()
        {
            vec3 pos = aPos;
            
            // Apply effects
            if (effect == 1) { // Wave effect
                pos.y += sin(pos.x * 3.0 + time * 2.0) * 0.1;
            } else if (effect == 2) { // Pulse effect
                float scale = 1.0 + sin(time * 3.0) * 0.2;
                pos *= scale;
            }
            
            gl_Position = mvp * vec4(pos, 1.0);
            TexCoord = aTexCoord;
            VertexTime = time;
        }
        """
        
        # Fragment shader source with multiple effects
        fragment_shader_source = """
        #version 330 core
        out vec4 FragColor;
        
        in vec2 TexCoord;
        in float VertexTime;
        
        uniform sampler2D ourTexture;
        uniform float brightness;
        uniform float time;
        uniform int effect;
        
        void main()
        {
            vec2 texCoord = TexCoord;
            
            // Apply texture coordinate effects
            if (effect == 1) { // Wave effect
                texCoord.x += sin(texCoord.y * 5.0 + time * 2.0) * 0.1;
            } else if (effect == 2) { // Pulse effect
                float scale = 1.0 + sin(time * 3.0) * 0.3;
                texCoord = (texCoord - 0.5) * scale + 0.5;
            }
            
            // Sample the texture
            vec4 texColor = texture(ourTexture, texCoord);
            
            // Apply brightness
            texColor.rgb *= brightness;
            
            // Apply color effects
            if (effect == 3) { // Rainbow effect
                float hue = time * 0.5 + TexCoord.x + TexCoord.y;
                vec3 rainbow = vec3(
                    sin(hue) * 0.5 + 0.5,
                    sin(hue + 2.094) * 0.5 + 0.5,
                    sin(hue + 4.188) * 0.5 + 0.5
                );
                texColor.rgb = mix(texColor.rgb, rainbow, 0.3);
            }
            
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
            texture = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture)
            
            # Set texture parameters
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            
            # Upload texture data
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
            
            self.textures.append(texture)
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
        
        # View matrix with mouse control
        view = np.eye(4, dtype=np.float32)
        
        # Apply camera rotation
        cos_x = math.cos(self.camera_angle_x)
        sin_x = math.sin(self.camera_angle_x)
        cos_y = math.cos(self.camera_angle_y)
        sin_y = math.sin(self.camera_angle_y)
        
        # Rotation around X axis
        view[1, 1] = cos_x
        view[1, 2] = sin_x
        view[2, 1] = -sin_x
        view[2, 2] = cos_x
        
        # Rotation around Y axis
        temp = view.copy()
        view[0, 0] = cos_y
        view[0, 2] = -sin_y
        view[2, 0] = sin_y
        view[2, 2] = cos_y
        view = np.dot(view, temp)
        
        # Apply zoom and translation
        view[2, 3] = -5.0 / self.zoom
        
        # Projection matrix (perspective)
        fov = 45.0
        aspect = 1000.0 / 800.0
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
        """Render the textured triangles"""
        # Clear screen
        glClearColor(0.1, 0.1, 0.2, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Use shader program
        glUseProgram(self.shader_program)
        
        # Create and set MVP matrix
        mvp = self.create_mvp_matrix()
        mvp_loc = glGetUniformLocation(self.shader_program, "mvp")
        glUniformMatrix4fv(mvp_loc, 1, GL_FALSE, mvp)
        
        # Set uniforms
        time_loc = glGetUniformLocation(self.shader_program, "time")
        effect_loc = glGetUniformLocation(self.shader_program, "effect")
        brightness_loc = glGetUniformLocation(self.shader_program, "brightness")
        
        glUniform1f(time_loc, self.time)
        glUniform1i(effect_loc, self.current_effect)
        glUniform1f(brightness_loc, self.brightness)
        
        # Bind texture
        if self.textures:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.textures[0])  # Use first texture for all triangles
            texture_loc = glGetUniformLocation(self.shader_program, "ourTexture")
            glUniform1i(texture_loc, 0)
        
        # Render each triangle
        for triangle in self.triangles:
            # Update VBO with current triangle data
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
            glBufferData(GL_ARRAY_BUFFER, triangle.nbytes, triangle, GL_DYNAMIC_DRAW)
            
            # Draw triangle
            glBindVertexArray(self.vao)
            glDrawArrays(GL_TRIANGLES, 0, 3)
        
        # Swap buffers
        glfw.swap_buffers(self.window)
        
    def run(self):
        """Main render loop"""
        print("Advanced Textured Triangle Demo")
        print("Controls:")
        print("  E - Switch effects (Normal, Wave, Pulse, Rainbow)")
        print("  UP/DOWN - Adjust brightness")
        print("  Mouse drag - Rotate camera")
        print("  Mouse scroll - Zoom")
        print("  ESC - Exit")
        
        while not glfw.window_should_close(self.window):
            # Update time and rotation
            self.time = glfw.get_time()
            self.rotation_angle = self.time * 0.3  # Slow rotation
            
            # Handle input
            glfw.poll_events()
            
            # Render
            self.render()
            
    def cleanup(self):
        """Clean up resources"""
        if self.vao:
            glDeleteVertexArrays(1, [self.vao])
        if self.vbo:
            glDeleteBuffers(1, [self.vbo])
        if self.textures:
            glDeleteTextures(len(self.textures), self.textures)
        if self.shader_program:
            glDeleteProgram(self.shader_program)
        glfw.terminate()

def main():
    """Main function"""
    try:
        demo = AdvancedTexturedTriangleDemo()
        demo.init_glfw()
        demo.create_shaders()
        demo.setup_buffers()
        
        # Load texture
        if not demo.load_texture('rose.png'):
            print("Warning: Could not load rose.png")
        
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
