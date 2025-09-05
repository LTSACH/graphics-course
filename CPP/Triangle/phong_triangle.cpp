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
layout (location = 1) in vec3 normal;

out vec3 FragPos;
out vec3 Normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main() {
    FragPos = vec3(model * vec4(position, 1.0));
    Normal = mat3(transpose(inverse(model))) * normal;
    
    gl_Position = projection * view * vec4(FragPos, 1.0);
}
)";

const char* fragmentShaderSource = R"(
#version 330 core
out vec4 FragColor;

in vec3 FragPos;
in vec3 Normal;

uniform vec3 lightPos;
uniform vec3 viewPos;
uniform vec3 lightColor;
uniform vec3 objectColor;

void main() {
    // Ambient
    float ambientStrength = 0.1;
    vec3 ambient = ambientStrength * lightColor;
    
    // Diffuse
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(lightPos - FragPos);
    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diff * lightColor;
    
    // Specular
    float specularStrength = 0.5;
    vec3 viewDir = normalize(viewPos - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 32);
    vec3 specular = specularStrength * spec * lightColor;
    
    vec3 result = (ambient + diffuse + specular) * objectColor;
    FragColor = vec4(result, 1.0);
}
)";

class PhongTriangleRenderer {
private:
    GLFWwindow* window;
    GLuint VAO, VBO;
    GLuint shaderProgram;
    int width, height;
    
    // Lighting parameters
    glm::vec3 lightPos;
    glm::vec3 lightColor;
    glm::vec3 objectColor;
    glm::vec3 viewPos;
    
    // Matrices
    glm::mat4 model;
    glm::mat4 view;
    glm::mat4 projection;
    
    float rotationAngle;

public:
    PhongTriangleRenderer() : width(800), height(600), rotationAngle(0.0f) {
        // Initialize lighting
        lightPos = glm::vec3(2.0f, 2.0f, 2.0f);
        lightColor = glm::vec3(1.0f, 1.0f, 1.0f);
        objectColor = glm::vec3(0.3f, 0.7f, 0.9f);
        viewPos = glm::vec3(0.0f, 0.0f, 3.0f);
        
        // Initialize matrices
        model = glm::mat4(1.0f);
        view = glm::lookAt(viewPos, glm::vec3(0.0f, 0.0f, 0.0f), glm::vec3(0.0f, 1.0f, 0.0f));
        projection = glm::perspective(glm::radians(45.0f), (float)width / (float)height, 0.1f, 100.0f);
    }
    
    ~PhongTriangleRenderer() {
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
        window = glfwCreateWindow(width, height, "Phong Triangle Demo", nullptr, nullptr);
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
        
        // Enable depth testing
        glEnable(GL_DEPTH_TEST);
        
        return true;
    }
    
    void setupBuffers() {
        // Triangle vertices with positions and normals
        float vertices[] = {
            // positions          // normals
             0.0f,  0.5f, 0.0f,   0.0f, 0.0f, 1.0f,  // top
            -0.5f, -0.5f, 0.0f,   0.0f, 0.0f, 1.0f,  // bottom left
             0.5f, -0.5f, 0.0f,   0.0f, 0.0f, 1.0f   // bottom right
        };
        
        glGenVertexArrays(1, &VAO);
        glGenBuffers(1, &VBO);
        
        glBindVertexArray(VAO);
        
        glBindBuffer(GL_ARRAY_BUFFER, VBO);
        glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
        
        // Position attribute
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)0);
        glEnableVertexAttribArray(0);
        
        // Normal attribute
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(float), (void*)(3 * sizeof(float)));
        glEnableVertexAttribArray(1);
        
        glBindVertexArray(0);
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
        glClearColor(0.1f, 0.1f, 0.1f, 1.0f);
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
        GLint lightPosLoc = glGetUniformLocation(shaderProgram, "lightPos");
        GLint lightColorLoc = glGetUniformLocation(shaderProgram, "lightColor");
        GLint objectColorLoc = glGetUniformLocation(shaderProgram, "objectColor");
        GLint viewPosLoc = glGetUniformLocation(shaderProgram, "viewPos");
        
        glUniformMatrix4fv(modelLoc, 1, GL_FALSE, &model[0][0]);
        glUniformMatrix4fv(viewLoc, 1, GL_FALSE, &view[0][0]);
        glUniformMatrix4fv(projLoc, 1, GL_FALSE, &projection[0][0]);
        glUniform3fv(lightPosLoc, 1, &lightPos[0]);
        glUniform3fv(lightColorLoc, 1, &lightColor[0]);
        glUniform3fv(objectColorLoc, 1, &objectColor[0]);
        glUniform3fv(viewPosLoc, 1, &viewPos[0]);
        
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
            objectColor = glm::vec3(0.9f, 0.3f, 0.3f); // Red
        }
        if (glfwGetKey(window, GLFW_KEY_G) == GLFW_PRESS) {
            objectColor = glm::vec3(0.3f, 0.9f, 0.3f); // Green
        }
        if (glfwGetKey(window, GLFW_KEY_B) == GLFW_PRESS) {
            objectColor = glm::vec3(0.3f, 0.3f, 0.9f); // Blue
        }
        if (glfwGetKey(window, GLFW_KEY_Y) == GLFW_PRESS) {
            objectColor = glm::vec3(0.9f, 0.9f, 0.3f); // Yellow
        }
    }
    
    void cleanup() {
        glDeleteVertexArrays(1, &VAO);
        glDeleteBuffers(1, &VBO);
        glDeleteProgram(shaderProgram);
        glfwTerminate();
    }
    
    static void framebufferSizeCallback(GLFWwindow* window, int width, int height) {
        glViewport(0, 0, width, height);
    }
};

int main() {
    PhongTriangleRenderer renderer;
    
    if (!renderer.init()) {
        std::cerr << "Failed to initialize renderer" << std::endl;
        return -1;
    }
    
    std::cout << "Phong Triangle Demo" << std::endl;
    std::cout << "Controls:" << std::endl;
    std::cout << "  R - Red color" << std::endl;
    std::cout << "  G - Green color" << std::endl;
    std::cout << "  B - Blue color" << std::endl;
    std::cout << "  Y - Yellow color" << std::endl;
    std::cout << "  ESC - Exit" << std::endl;
    
    renderer.run();
    
    return 0;
}
