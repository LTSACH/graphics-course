#include <iostream>
#include <vector>
#include <string>
#include <glad/glad.h>
#include <GLFW/glfw3.h>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <glm/gtc/type_ptr.hpp>
#include <cmath>

// Shader sources
const char* vertexShaderSource = R"(
#version 330 core
layout (location = 0) in vec3 position;
layout (location = 1) in vec2 texCoord;

out vec2 TexCoord;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main() {
    gl_Position = projection * view * model * vec4(position, 1.0);
    TexCoord = texCoord;
}
)";

const char* fragmentShaderSource = R"(
#version 330 core
out vec4 FragColor;

in vec2 TexCoord;

uniform sampler2D texture1;
uniform vec3 objectColor;

void main() {
    vec4 texColor = texture(texture1, TexCoord);
    FragColor = texColor * vec4(objectColor, 1.0);
}
)";

class TexturedTriangleRenderer {
private:
    GLFWwindow* window;
    GLuint VAO, VBO;
    GLuint shaderProgram;
    GLuint texture;
    int width, height;
    
    // Color parameters
    glm::vec3 objectColor;
    
    // Matrices
    glm::mat4 model;
    glm::mat4 view;
    glm::mat4 projection;
    
    float rotationAngle;

public:
    TexturedTriangleRenderer() : width(800), height(600), rotationAngle(0.0f) {
        // Initialize color
        objectColor = glm::vec3(1.0f, 1.0f, 1.0f); // White (no color tint)
        
        // Initialize matrices
        model = glm::mat4(1.0f);
        view = glm::lookAt(glm::vec3(0.0f, 0.0f, 3.0f), glm::vec3(0.0f, 0.0f, 0.0f), glm::vec3(0.0f, 1.0f, 0.0f));
        projection = glm::perspective(glm::radians(45.0f), (float)width / (float)height, 0.1f, 100.0f);
    }
    
    ~TexturedTriangleRenderer() {
        cleanup();
    }
    
    bool init() {
        // Initialize GLFW
        if (!glfwInit()) {
            std::cerr << "Failed to initialize GLFW" << std::endl;
            return false;
        }
        
        // Configure GLFW
        glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
        glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
        glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
        
        // Create window
        window = glfwCreateWindow(width, height, "Textured Triangle Demo", nullptr, nullptr);
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
        
        // Load texture
        if (!loadTexture()) {
            return false;
        }
        
        // Enable depth testing
        glEnable(GL_DEPTH_TEST);
        
        return true;
    }
    
    void setupBuffers() {
        // Triangle vertices with positions and texture coordinates
        float vertices[] = {
            // positions          // texture coords
             0.0f,  0.5f, 0.0f,   0.5f, 1.0f,  // top
            -0.5f, -0.5f, 0.0f,   0.0f, 0.0f,  // bottom left
             0.5f, -0.5f, 0.0f,   1.0f, 0.0f   // bottom right
        };
        
        glGenVertexArrays(1, &VAO);
        glGenBuffers(1, &VBO);
        
        glBindVertexArray(VAO);
        
        glBindBuffer(GL_ARRAY_BUFFER, VBO);
        glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
        
        // Position attribute
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void*)0);
        glEnableVertexAttribArray(0);
        
        // Texture coordinate attribute
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5 * sizeof(float), (void*)(3 * sizeof(float)));
        glEnableVertexAttribArray(1);
        
        glBindVertexArray(0);
    }
    
    bool loadTexture() {
        // Create a simple procedural texture (checkerboard pattern)
        const int textureWidth = 64;
        const int textureHeight = 64;
        unsigned char textureData[textureWidth * textureHeight * 3];
        
        for (int y = 0; y < textureHeight; y++) {
            for (int x = 0; x < textureWidth; x++) {
                int index = (y * textureWidth + x) * 3;
                
                // Create a checkerboard pattern
                bool isEven = ((x / 8) + (y / 8)) % 2 == 0;
                
                if (isEven) {
                    // White squares
                    textureData[index] = 255;     // R
                    textureData[index + 1] = 255; // G
                    textureData[index + 2] = 255; // B
                } else {
                    // Red squares
                    textureData[index] = 255;     // R
                    textureData[index + 1] = 100; // G
                    textureData[index + 2] = 100; // B
                }
            }
        }
        
        // Generate texture
        glGenTextures(1, &texture);
        glBindTexture(GL_TEXTURE_2D, texture);
        
        // Set texture parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
        
        // Upload texture data
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, textureWidth, textureHeight, 0, GL_RGB, GL_UNSIGNED_BYTE, textureData);
        glGenerateMipmap(GL_TEXTURE_2D);
        
        return true;
    }
    
    bool createShaders() {
        // Vertex shader
        GLuint vertexShader = glCreateShader(GL_VERTEX_SHADER);
        glShaderSource(vertexShader, 1, &vertexShaderSource, nullptr);
        glCompileShader(vertexShader);
        
        // Check vertex shader compilation
        GLint success;
        glGetShaderiv(vertexShader, GL_COMPILE_STATUS, &success);
        if (!success) {
            GLchar infoLog[512];
            glGetShaderInfoLog(vertexShader, 512, nullptr, infoLog);
            std::cerr << "Vertex shader compilation failed: " << infoLog << std::endl;
            return false;
        }
        
        // Fragment shader
        GLuint fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
        glShaderSource(fragmentShader, 1, &fragmentShaderSource, nullptr);
        glCompileShader(fragmentShader);
        
        // Check fragment shader compilation
        glGetShaderiv(fragmentShader, GL_COMPILE_STATUS, &success);
        if (!success) {
            GLchar infoLog[512];
            glGetShaderInfoLog(fragmentShader, 512, nullptr, infoLog);
            std::cerr << "Fragment shader compilation failed: " << infoLog << std::endl;
            return false;
        }
        
        // Shader program
        shaderProgram = glCreateProgram();
        glAttachShader(shaderProgram, vertexShader);
        glAttachShader(shaderProgram, fragmentShader);
        glLinkProgram(shaderProgram);
        
        // Check program linking
        glGetProgramiv(shaderProgram, GL_LINK_STATUS, &success);
        if (!success) {
            GLchar infoLog[512];
            glGetProgramInfoLog(shaderProgram, 512, nullptr, infoLog);
            std::cerr << "Shader program linking failed: " << infoLog << std::endl;
            return false;
        }
        
        // Clean up shaders
        glDeleteShader(vertexShader);
        glDeleteShader(fragmentShader);
        
        return true;
    }
    
    void render() {
        // Clear screen
        glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        
        // Use shader program
        glUseProgram(shaderProgram);
        
        // Update rotation
        rotationAngle += 0.01f;
        model = glm::rotate(glm::mat4(1.0f), rotationAngle, glm::vec3(0.0f, 1.0f, 0.0f));
        
        // Set uniforms
        GLint modelLoc = glGetUniformLocation(shaderProgram, "model");
        GLint viewLoc = glGetUniformLocation(shaderProgram, "view");
        GLint projLoc = glGetUniformLocation(shaderProgram, "projection");
        GLint objectColorLoc = glGetUniformLocation(shaderProgram, "objectColor");
        
        glUniformMatrix4fv(modelLoc, 1, GL_FALSE, &model[0][0]);
        glUniformMatrix4fv(viewLoc, 1, GL_FALSE, &view[0][0]);
        glUniformMatrix4fv(projLoc, 1, GL_FALSE, &projection[0][0]);
        glUniform3fv(objectColorLoc, 1, &objectColor[0]);
        
        // Bind texture
        glActiveTexture(GL_TEXTURE0);
        glBindTexture(GL_TEXTURE_2D, texture);
        
        // Draw triangle
        glBindVertexArray(VAO);
        glDrawArrays(GL_TRIANGLES, 0, 3);
        glBindVertexArray(0);
    }
    
    void run() {
        while (!glfwWindowShouldClose(window)) {
            // Handle input
            processInput();
            
            // Render
            render();
            
            // Swap buffers and poll events
            glfwSwapBuffers(window);
            glfwPollEvents();
        }
    }
    
    void processInput() {
        if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS) {
            glfwSetWindowShouldClose(window, true);
        }
        
        // Change colors with keys
        if (glfwGetKey(window, GLFW_KEY_R) == GLFW_PRESS) {
            objectColor = glm::vec3(1.0f, 0.3f, 0.3f); // Red tint
        }
        if (glfwGetKey(window, GLFW_KEY_G) == GLFW_PRESS) {
            objectColor = glm::vec3(0.3f, 1.0f, 0.3f); // Green tint
        }
        if (glfwGetKey(window, GLFW_KEY_B) == GLFW_PRESS) {
            objectColor = glm::vec3(0.3f, 0.3f, 1.0f); // Blue tint
        }
        if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS) {
            objectColor = glm::vec3(1.0f, 1.0f, 1.0f); // White (no tint)
        }
    }
    
    void cleanup() {
        glDeleteVertexArrays(1, &VAO);
        glDeleteBuffers(1, &VBO);
        glDeleteProgram(shaderProgram);
        glDeleteTextures(1, &texture);
        glfwTerminate();
    }
    
    static void framebufferSizeCallback(GLFWwindow* window, int width, int height) {
        glViewport(0, 0, width, height);
    }
};

int main() {
    TexturedTriangleRenderer renderer;
    
    if (!renderer.init()) {
        std::cerr << "Failed to initialize renderer" << std::endl;
        return -1;
    }
    
    std::cout << "Textured Triangle Demo" << std::endl;
    std::cout << "Controls:" << std::endl;
    std::cout << "  R - Red tint" << std::endl;
    std::cout << "  G - Green tint" << std::endl;
    std::cout << "  B - Blue tint" << std::endl;
    std::cout << "  W - White (no tint)" << std::endl;
    std::cout << "  ESC - Exit" << std::endl;
    
    renderer.run();
    
    return 0;
}
