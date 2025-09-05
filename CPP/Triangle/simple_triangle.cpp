#include <iostream>
#include <vector>
#include <glad/glad.h>
#include <GLFW/glfw3.h>

class SimpleTriangleRenderer {
private:
    GLFWwindow* window;
    GLuint VAO, VBO;
    GLuint shaderProgram;
    
    // Simple vertex data (position only)
    std::vector<float> vertices = {
        -0.5f, -0.5f, 0.0f,  // Left
         0.5f, -0.5f, 0.0f,  // Right
         0.0f,  0.5f, 0.0f   // Top
    };
    
    // Simple shader sources
    const char* vertexShaderSource = R"(
    #version 330 core
    layout (location = 0) in vec3 position;
    
    void main()
    {
        gl_Position = vec4(position, 1.0);
    }
    )";
    
    const char* fragmentShaderSource = R"(
    #version 330 core
    out vec4 FragColor;
    
    void main()
    {
        FragColor = vec4(0.8f, 0.3f, 0.8f, 1.0f); // Purple color
    }
    )";

public:
    SimpleTriangleRenderer() : window(nullptr), VAO(0), VBO(0), shaderProgram(0) {}
    
    bool init() {
        // Initialize GLFW
        if (!glfwInit()) {
            std::cerr << "Failed to initialize GLFW" << std::endl;
            return false;
        }
        
        // Configure GLFW for OpenGL 3.3 Core Profile
        glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
        glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
        glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
        glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
        
        // Create window
        window = glfwCreateWindow(800, 600, "Simple Triangle (C++)", nullptr, nullptr);
        if (!window) {
            std::cerr << "Failed to create GLFW window" << std::endl;
            glfwTerminate();
            return false;
        }
        
        glfwMakeContextCurrent(window);
        glfwSetFramebufferSizeCallback(window, framebufferSizeCallback);
        
        // Load OpenGL function pointers
        if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress)) {
            std::cerr << "Failed to initialize GLAD" << std::endl;
            return false;
        }
        
        // Create shaders
        if (!createShaders()) {
            return false;
        }
        
        // Setup buffers
        setupBuffers();
        
        return true;
    }
    
    bool createShaders() {
        // Vertex shader
        GLuint vertexShader = glCreateShader(GL_VERTEX_SHADER);
        glShaderSource(vertexShader, 1, &vertexShaderSource, nullptr);
        glCompileShader(vertexShader);
        
        // Check compilation
        GLint success;
        glGetShaderiv(vertexShader, GL_COMPILE_STATUS, &success);
        if (!success) {
            GLchar infoLog[512];
            glGetShaderInfoLog(vertexShader, 512, nullptr, infoLog);
            std::cerr << "ERROR::SHADER::VERTEX::COMPILATION_FAILED\n" << infoLog << std::endl;
            return false;
        }
        
        // Fragment shader
        GLuint fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
        glShaderSource(fragmentShader, 1, &fragmentShaderSource, nullptr);
        glCompileShader(fragmentShader);
        
        // Check compilation
        glGetShaderiv(fragmentShader, GL_COMPILE_STATUS, &success);
        if (!success) {
            GLchar infoLog[512];
            glGetShaderInfoLog(fragmentShader, 512, nullptr, infoLog);
            std::cerr << "ERROR::SHADER::FRAGMENT::COMPILATION_FAILED\n" << infoLog << std::endl;
            return false;
        }
        
        // Create shader program
        shaderProgram = glCreateProgram();
        glAttachShader(shaderProgram, vertexShader);
        glAttachShader(shaderProgram, fragmentShader);
        glLinkProgram(shaderProgram);
        
        // Check linking
        glGetProgramiv(shaderProgram, GL_LINK_STATUS, &success);
        if (!success) {
            GLchar infoLog[512];
            glGetProgramInfoLog(shaderProgram, 512, nullptr, infoLog);
            std::cerr << "ERROR::PROGRAM::LINKING_FAILED\n" << infoLog << std::endl;
            return false;
        }
        
        // Clean up shaders
        glDeleteShader(vertexShader);
        glDeleteShader(fragmentShader);
        
        return true;
    }
    
    void setupBuffers() {
        // Create VAO
        glGenVertexArrays(1, &VAO);
        glBindVertexArray(VAO);
        
        // Create VBO
        glGenBuffers(1, &VBO);
        glBindBuffer(GL_ARRAY_BUFFER, VBO);
        glBufferData(GL_ARRAY_BUFFER, vertices.size() * sizeof(float), vertices.data(), GL_STATIC_DRAW);
        
        // Set vertex attributes
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
        glEnableVertexAttribArray(0);
        
        // Unbind
        glBindBuffer(GL_ARRAY_BUFFER, 0);
        glBindVertexArray(0);
    }
    
    void render() {
        glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);
        
        // Use shader program and draw triangle
        glUseProgram(shaderProgram);
        glBindVertexArray(VAO);
        glDrawArrays(GL_TRIANGLES, 0, 3);
        
        glfwSwapBuffers(window);
        glfwPollEvents();
    }
    
    void run() {
        std::cout << "Simple Triangle Demo is running!" << std::endl;
        std::cout << "Press ESC or close window to exit" << std::endl;
        
        while (!glfwWindowShouldClose(window)) {
            render();
            
            // Handle input
            if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS) {
                glfwSetWindowShouldClose(window, true);
            }
        }
    }
    
    void cleanup() {
        if (VAO) glDeleteVertexArrays(1, &VAO);
        if (VBO) glDeleteBuffers(1, &VBO);
        if (shaderProgram) glDeleteProgram(shaderProgram);
        if (window) glfwTerminate();
    }
    
    static void framebufferSizeCallback(GLFWwindow* window, int width, int height) {
        glViewport(0, 0, width, height);
    }
    
    ~SimpleTriangleRenderer() {
        cleanup();
    }
};

int main() {
    SimpleTriangleRenderer renderer;
    
    if (!renderer.init()) {
        std::cerr << "Failed to initialize renderer" << std::endl;
        return -1;
    }
    
    renderer.run();
    
    return 0;
}
