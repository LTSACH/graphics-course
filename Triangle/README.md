# Triangle Demos - WebGL

This directory contains WebGL demonstrations of rendering triangles using modern shader-based approach.

## Available Demos

### 1. `triangle_demo.html` - Full Shader Demo
**Complete demonstration with modern WebGL features**

**Features:**
- WebGL 1.0 with modern shader pipeline
- Vertex and Fragment Shaders (GLSL ES)
- VBO and VAO with color attributes
- Colored triangle (red, green, and blue vertices)
- Responsive design with window resize handling
- Error handling and WebGL context validation

**Technical Details:**
- Uses `gl.createShader()` and `gl.createProgram()`
- Vertex Buffer Objects for efficient data storage
- Vertex Array Objects for attribute configuration
- Modern shader-based rendering pipeline
- Cross-browser compatibility with fallbacks

**Best for:** Learning complete WebGL pipeline, understanding shader compilation

---

### 2. `simple_triangle.html` - Basic Demo
**Simplified WebGL example for beginners**

**Features:**
- WebGL 1.0 with basic shader pipeline
- Simple Vertex and Fragment Shaders
- VBO and VAO setup
- Single color triangle (orange)
- Minimal code for learning purposes
- Clean, well-commented code

**Technical Details:**
- Basic shader setup without complex features
- Uniform color in fragment shader
- Essential WebGL concepts only
- Easy to understand and modify

**Best for:** WebGL beginners, understanding basic concepts

---

### 3. `interactive_triangle.html` - Interactive Demo
**Advanced demonstration with user interaction**

**Features:**
- Mouse interaction (triangle follows mouse movement)
- Real-time animation (continuous rotation and scaling)
- Dynamic color (HSV color space manipulation)
- Interactive controls (sliders for parameter adjustment)
- WebGL shaders with uniforms
- Advanced shader programming

**Technical Details:**
- Uniform variables for real-time parameter changes
- HSV to RGB color space conversion in shaders
- Matrix transformations in vertex shader
- Event handling for mouse and keyboard input
- Animation loop with `requestAnimationFrame()`

**Best for:** Learning interactive graphics, understanding uniforms, advanced shader programming

---

### 4. `textured_triangle.html` - Procedural Texture Demo
**Triangle with procedural texture generation**

**Features:**
- Procedural texture generation in fragment shader
- Multiple texture types (checkerboard, gradient, noise)
- Real-time texture switching
- Interactive controls for rotation, scale, and color tinting
- Advanced fragment shader programming
- Texture coordinate mapping

**Technical Details:**
- Procedural texture algorithms in GLSL
- Uniform variables for texture type selection
- UV coordinate mapping
- Color tinting with RGB multiplication
- Matrix transformations for rotation and scaling

**Best for:** Learning procedural graphics, understanding texture coordinates, advanced fragment shaders

---

### 5. `rose_textured_triangle.html` - Image Texture Demo
**Triangle with rose image texture**

**Features:**
- Real rose image texture (rose.png)
- Texture effects (normal, invert, grayscale)
- Interactive controls for rotation, scale, and color tinting
- Real-time texture effect switching
- Advanced texture manipulation
- Fallback procedural texture if image fails to load

**Technical Details:**
- Image texture loading with HTML5 Image API
- Texture effect shaders (invert, grayscale)
- Texture coordinate mapping
- Color tinting and blending
- Matrix transformations
- CORS handling for image loading

**Best for:** Learning image texture loading, understanding texture effects, advanced texture manipulation

## How to Run

### Quick Start
```bash
# Open any demo directly in browser
open triangle_demo.html        # macOS
start triangle_demo.html       # Windows
xdg-open triangle_demo.html    # Linux

# Or open texture demos
open textured_triangle.html
open rose_textured_triangle.html
```

### With Local Server (Recommended)
```bash
# From HTML directory
python -m http.server 8000
# Then open: 
# http://localhost:8000/Triangle/triangle_demo.html
# http://localhost:8000/Triangle/textured_triangle.html
# http://localhost:8000/Triangle/rose_textured_triangle.html
```

## Learning Path

### For Beginners:
1. Start with `simple_triangle.html` - understand basic concepts
2. Move to `triangle_demo.html` - learn complete pipeline
3. Try `interactive_triangle.html` - explore advanced features
4. Experiment with `textured_triangle.html` - learn procedural textures
5. Explore `rose_textured_triangle.html` - understand texture effects

### For Experienced Developers:
1. Examine `triangle_demo.html` - see best practices
2. Study `interactive_triangle.html` - learn advanced techniques
3. Analyze `textured_triangle.html` - understand procedural generation
4. Review `rose_textured_triangle.html` - learn texture manipulation
5. Use as templates for your own projects

## Code Structure

Each demo follows this structure:
```
├── HTML Structure (canvas, controls, info)
├── CSS Styling (responsive design, themes)
├── JavaScript Class (TriangleRenderer)
│   ├── Constructor (setup, shader sources)
│   ├── init() (WebGL context, shaders, buffers)
│   ├── createShaders() (compile and link)
│   ├── setupBuffers() (VBO, attributes)
│   ├── loadTexture() (image loading for rose demo)
│   ├── render() (drawing loop)
│   ├── setupEventListeners() (interaction)
│   └── cleanup() (resource management)
└── Initialization (window load event)
```

## File Structure

```
HTML/Triangle/
├── simple_triangle.html           # Basic triangle
├── triangle_demo.html             # Colored triangle
├── interactive_triangle.html      # Interactive triangle
├── textured_triangle.html         # Procedural textures
├── rose_textured_triangle.html    # Rose image texture
├── rose.png                       # Rose texture image
└── README.md                      # This documentation
```

## Key WebGL Concepts Demonstrated

### 1. **Context Creation**
```javascript
const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
```

### 2. **Shader Compilation**
```javascript
const vertexShader = gl.createShader(gl.VERTEX_SHADER);
gl.shaderSource(vertexShader, vertexShaderSource);
gl.compileShader(vertexShader);
```

### 3. **Program Linking**
```javascript
const program = gl.createProgram();
gl.attachShader(program, vertexShader);
gl.attachShader(program, fragmentShader);
gl.linkProgram(program);
```

### 4. **Buffer Management**
```javascript
const vbo = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, vbo);
gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);
```

### 5. **Attribute Setup**
```javascript
const positionLocation = gl.getAttribLocation(program, 'position');
gl.enableVertexAttribArray(positionLocation);
gl.vertexAttribPointer(positionLocation, 3, gl.FLOAT, false, 6 * 4, 0);
```

### 6. **Rendering Loop**
```javascript
const animate = () => {
    render();
    requestAnimationFrame(animate);
};
```

## Browser Compatibility

- ✅ **Chrome** (recommended)
- ✅ **Firefox**
- ✅ **Safari**
- ✅ **Edge**
- ✅ **Mobile browsers** (iOS Safari, Chrome Mobile)

## Troubleshooting

### Common Issues:

1. **Black screen**
   - Check browser console for errors
   - Ensure WebGL is supported
   - Try different browser

2. **Shader compilation errors**
   - Check GLSL ES syntax
   - Verify precision qualifiers
   - Test in Chrome DevTools

3. **Performance issues**
   - Close other browser tabs
   - Check GPU acceleration
   - Monitor frame rate

## Next Steps

After mastering these triangle demos, consider exploring:

- **3D Models**: Loading and rendering 3D objects
- **Advanced Textures**: Normal maps, specular maps, environment mapping
- **Lighting**: Implementing Phong, Blinn-Phong shading
- **Animation**: Keyframe and procedural animation
- **Post-processing**: Bloom, blur, color grading effects
- **Physics**: Integration with physics engines
- **Procedural Generation**: Noise functions, fractals, cellular automata

## Resources

- [WebGL Fundamentals](https://webglfundamentals.org/)
- [MDN WebGL Guide](https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API)
- [WebGL Academy](http://www.webglacademy.com/)
- [Three.js](https://threejs.org/) - Popular WebGL library
