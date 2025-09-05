@echo off
echo Building Computer Graphics C++ project for Windows...

REM Check if CMake is installed
cmake --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ CMake is not installed. Please install CMake first.
    echo Download from: https://cmake.org/download/
    pause
    exit /b 1
)

REM Create build directory
if not exist build mkdir build
cd build

REM Configure with CMake (Visual Studio 2019)
echo Configuring with CMake...
cmake .. -G "Visual Studio 16 2019" -A x64
if %errorlevel% neq 0 (
    echo ❌ CMake configuration failed!
    pause
    exit /b 1
)

REM Build project
echo Building project...
cmake --build . --config Release
if %errorlevel% neq 0 (
    echo ❌ Build failed!
    pause
    exit /b 1
)

echo.
echo ✅ Build successful!
echo.
echo To run the demos:
echo   cd build
echo   .\Release\simple_triangle.exe
echo   .\Release\triangle_demo.exe
echo   .\Release\phong_triangle.exe
echo.
pause
