#!/usr/bin/env python3
"""
Triangle Demo with Pygame - Alternative to GLFW
A simple demonstration of rendering a triangle using PyOpenGL with Pygame
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import sys

class TriangleRenderer:
    def __init__(self):
        self.display = None
        self.vertices = None
        
        # Triangle vertices (position only)
        self.vertices = np.array([
            -0.5, -0.5, 0.0,  # Left
             0.5, -0.5, 0.0,  # Right
             0.0,  0.5, 0.0   # Top
        ], dtype=np.float32)
    
    def init_pygame(self):
        """Initialize Pygame and OpenGL context"""
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        
        # Set up OpenGL
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glEnable(GL_DEPTH_TEST)
        
        self.display = display
        print("Triangle Demo with Pygame is running!")
        print("Press ESC or close window to exit")
    
    def render(self):
        """Render the triangle"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Draw triangle using immediate mode (for simplicity)
        glBegin(GL_TRIANGLES)
        glColor3f(1.0, 0.0, 0.0)  # Red
        glVertex3f(-0.5, -0.5, 0.0)
        
        glColor3f(0.0, 1.0, 0.0)  # Green
        glVertex3f(0.5, -0.5, 0.0)
        
        glColor3f(0.0, 0.0, 1.0)  # Blue
        glVertex3f(0.0, 0.5, 0.0)
        glEnd()
        
        pygame.display.flip()
    
    def run(self):
        """Main render loop"""
        self.init_pygame()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
            
            self.render()
            pygame.time.wait(10)  # Small delay to prevent excessive CPU usage

def main():
    """Main function"""
    try:
        renderer = TriangleRenderer()
        renderer.run()
    except Exception as e:
        print(f"Error: {e}")
        pygame.quit()
        sys.exit(-1)

if __name__ == "__main__":
    main()
