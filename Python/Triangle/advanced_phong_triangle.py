#!/usr/bin/env python3
"""
Advanced Phong Shading Triangle Demo
Interactive demo with lighting controls, multiple triangles, and real-time parameter adjustment.
"""

import numpy as np
import glfw
from OpenGL.GL import *
import math
import random

class AdvancedPhongTriangleDemo:
    def __init__(self):
        self.window = None
        self.shader_program = None
        self.vao = None
        self.vbo = None
        
        # Multiple triangles for comparison
        self.triangles = []
        self.generate_triangles()
        
        # Lighting parameters
        self.light_pos = np.array([2.0, 2.0, 2.0], dtype=np.float32)
        self.view_pos = np.array([0.0, 0.0, 5.0], dtype=np.float32)
        
        # Material properties
        self.materials = [
            {"color": [0.8, 0.2, 0.2], "ambient": 0.3, "specular": 0.8, "shininess": 32},  # Red
            {"color": [0.2, 0.8, 0.2], "ambient": 0.2, "specular": 0.9, "shininess": 64},  # Green
            {"color": [0.2, 0.2, 0.8], "ambient": 0.4, "specular": 0.6, "shininess": 16},  # Blue
        ]
        
        # Animation parameters
        self.rotation_angle = 0.0
        self.time = 0.0
        
        # Interactive parameters
        self.current_material = 0
        self.show_normals = False
        self.light_intensity = 1.0
        
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
        self.window = glfw.create_window(1000, 800, "Advanced Phong Shading Demo", None, None)
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
            if key == glfw.KEY_R:
                self.generate_triangles()
                print("Generated new random normals for all triangles")
            elif key == glfw.KEY_M:
                self.current_material = (self.current_material + 1) % len(self.materials)
                print(f"Switched to material {self.current_material + 1}")
            elif key == glfw.KEY_N:
                self.show_normals = not self.show_normals
                print(f"Normal visualization: {'ON' if self.show_normals else 'OFF'}")
            elif key == glfw.KEY_UP:
                self.light_intensity = min(2.0, self.light_intensity + 0.1)
                print(f"Light intensity: {self.light_intensity:.1f}")
            elif key == glfw.KEY_DOWN:
                self.light_intensity = max(0.1, self.light_intensity - 0.1)
                print(f"Light intensity: {self.light_intensity:.1f}")
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
        """Generate multiple triangles with different normal configurations"""
        self.triangles = []
        
        # Triangle 1: Random normals (educational)
        triangle1 = np.array([
            # Position (x, y, z), Normal (nx, ny, nz)
            -1.0, -0.5, 0.0,  0.0, 0.0, 1.0,  # Bottom left
             0.0, -0.5, 0.0,  0.0, 0.0, 1.0,  # Bottom right
            -0.5,  0.5, 0.0,  0.0, 0.0, 1.0,  # Top center
        ], dtype=np.float32)
        
        # Generate random normals
        for i in range(3):
            nx = random.uniform(-1.0, 1.0)
            ny = random.uniform(-1.0, 1.0)
            nz = random.uniform(0.0, 1.0)
            length = math.sqrt(nx*nx + ny*ny + nz*nz)
            triangle1[i*6 + 3] = nx / length
            triangle1[i*6 + 4] = ny / length
            triangle1[i*6 + 5] = nz / length
        
        # Triangle 2: Smooth normals (realistic)
        triangle2 = np.array([
            # Position (x, y, z), Normal (nx, ny, nz)
             0.0, -0.5, 0.0,  0.0, 0.0, 1.0,  # Bottom left
             1.0, -0.5, 0.0,  0.0, 0.0, 1.0,  # Bottom right
             0.5,  0.5, 0.0,  0.0, 0.0, 1.0,  # Top center
        ], dtype=np.float32)
        
        # Triangle 3: Varied normals (artistic)
        triangle3 = np.array([
            # Position (x, y, z), Normal (nx, ny, nz)
            -0.5,  0.0, 0.0,  0.0, 0.0, 1.0,  # Left
             0.5,  0.0, 0.0,  0.0, 0.0, 1.0,  # Right
             0.0,  1.0, 0.0,  0.0, 0.0, 1.0,  # Top
        ], dtype=np.float32)
        
        # Generate varied normals for triangle 3
        for i in range(3):
            angle = i * 2 * math.pi / 3
            nx = math.cos(angle) * 0.5
            ny = math.sin(angle) * 0.5
            nz = 0.8
            length = math.sqrt(nx*nx + ny*ny + nz*nz)
            triangle3[i*6 + 3] = nx / length
            triangle3[i*6 + 4] = ny / length
            triangle3[i*6 + 5] = nz / length
        
        self.triangles = [triangle1, triangle2, triangle3]
        
    def create_shaders(self):
        """Create and compile shaders"""
        # Vertex shader source
        vertex_shader_source = """
        #version 330 core
        layout (location = 0) in vec3 aPos;
        layout (location = 1) in vec3 aNormal;
        
        uniform mat4 mvp;
        
        out vec3 FragPos;
        out vec3 Normal;
        
        void main()
        {
            FragPos = aPos;
            Normal = aNormal;
            gl_Position = mvp * vec4(aPos, 1.0);
        }
        """
        
        # Fragment shader source with enhanced Phong lighting
        fragment_shader_source = """
        #version 330 core
        out vec4 FragColor;
        
        in vec3 FragPos;
        in vec3 Normal;
        
        uniform vec3 lightPos;
        uniform vec3 viewPos;
        uniform vec3 objectColor;
        uniform vec3 lightColor;
        uniform float ambientStrength;
        uniform float specularStrength;
        uniform int shininess;
        uniform float lightIntensity;
        
        void main()
        {
            // Ambient lighting
            vec3 ambient = ambientStrength * lightColor * lightIntensity;
            
            // Diffuse lighting
            vec3 norm = normalize(Normal);
            vec3 lightDir = normalize(lightPos - FragPos);
            float diff = max(dot(norm, lightDir), 0.0);
            vec3 diffuse = diff * lightColor * lightIntensity;
            
            // Specular lighting
            vec3 viewDir = normalize(viewPos - FragPos);
            vec3 reflectDir = reflect(-lightDir, norm);
            float spec = pow(max(dot(viewDir, reflectDir), 0.0), shininess);
            vec3 specular = specularStrength * spec * lightColor * lightIntensity;
            
            // Combine all lighting components
            vec3 result = (ambient + diffuse + specular) * objectColor;
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
        
        # Position attribute (location = 0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        
        # Normal attribute (location = 1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * 4, ctypes.c_void_p(3 * 4))
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
        """Render the triangles"""
        # Clear screen
        glClearColor(0.1, 0.1, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Use shader program
        glUseProgram(self.shader_program)
        
        # Create and set MVP matrix
        mvp = self.create_mvp_matrix()
        mvp_loc = glGetUniformLocation(self.shader_program, "mvp")
        glUniformMatrix4fv(mvp_loc, 1, GL_FALSE, mvp)
        
        # Set lighting uniforms
        light_pos_loc = glGetUniformLocation(self.shader_program, "lightPos")
        view_pos_loc = glGetUniformLocation(self.shader_program, "viewPos")
        object_color_loc = glGetUniformLocation(self.shader_program, "objectColor")
        light_color_loc = glGetUniformLocation(self.shader_program, "lightColor")
        ambient_str_loc = glGetUniformLocation(self.shader_program, "ambientStrength")
        specular_str_loc = glGetUniformLocation(self.shader_program, "specularStrength")
        shininess_loc = glGetUniformLocation(self.shader_program, "shininess")
        light_intensity_loc = glGetUniformLocation(self.shader_program, "lightIntensity")
        
        glUniform3f(light_pos_loc, 1.0, 1.0, 2.0)  # Light position
        glUniform3f(view_pos_loc, 0.0, 0.0, 3.0)  # View position
        glUniform3f(light_color_loc, 1.0, 1.0, 1.0)  # White light
        glUniform1f(light_intensity_loc, self.light_intensity)
        
        # Render each triangle
        for i, triangle in enumerate(self.triangles):
            # Set material properties
            material = self.materials[i]
            glUniform3fv(object_color_loc, 1, material["color"])
            glUniform1f(ambient_str_loc, material["ambient"])
            glUniform1f(specular_str_loc, material["specular"])
            glUniform1i(shininess_loc, material["shininess"])
            
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
        print("Advanced Phong Shading Triangle Demo")
        print("Controls:")
        print("  R - Generate new random normals")
        print("  M - Switch material")
        print("  N - Toggle normal visualization")
        print("  UP/DOWN - Adjust light intensity")
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
        if self.shader_program:
            glDeleteProgram(self.shader_program)
        glfw.terminate()

def main():
    """Main function"""
    try:
        demo = AdvancedPhongTriangleDemo()
        demo.init_glfw()
        demo.create_shaders()
        demo.setup_buffers()
        demo.generate_triangles()
        demo.run()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'demo' in locals():
            demo.cleanup()

if __name__ == "__main__":
    main()
