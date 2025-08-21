#!/usr/bin/env python3
"""
Cross-Platform Build Script for Oracle Fusion Resource Fetcher
Creates standalone executables for Windows, macOS, and Linux
"""

import subprocess
import sys
import os
import shutil
import platform
from pathlib import Path

def get_platform_info():
    """Get current platform information"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "windows":
        return "windows"
    elif system == "darwin":
        return "macos"
    elif system == "linux":
        return "linux"
    else:
        return "unknown"

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    print("📦 Installing PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing PyInstaller: {e}")
        return False

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        print("✅ Packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def create_spec_file(platform_name):
    """Create PyInstaller spec file for specific platform"""
    exe_name = "OracleFusionResourceFetcher"
    if platform_name == "windows":
        exe_name += ".exe"
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['simple_oracle_fetcher.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'http.server',
        'socketserver',
        'json',
        'requests',
        'base64',
        'os',
        'socket',
        'urllib.parse',
        'datetime',
        'threading'
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{exe_name}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None
)
'''
    
    spec_filename = f'oracle_fusion_fetcher_{platform_name}.spec'
    with open(spec_filename, 'w') as f:
        f.write(spec_content)
    print(f"✅ Spec file created for {platform_name}: {spec_filename}")
    return spec_filename

def build_executable(spec_filename):
    """Build the executable using PyInstaller"""
    print(f"🔨 Building executable using {spec_filename}...")
    try:
        subprocess.check_call([sys.executable, "-m", "PyInstaller", spec_filename, "--clean"])
        print("✅ Executable built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error building executable: {e}")
        return False

def create_distribution_folder(platform_name):
    """Create a distribution folder with the executable and documentation"""
    print(f"📁 Creating distribution folder for {platform_name}...")
    
    # Create dist folder
    dist_folder = Path(f"dist/OracleFusionResourceFetcher_{platform_name}")
    dist_folder.mkdir(parents=True, exist_ok=True)
    
    # Copy executable
    exe_name = "OracleFusionResourceFetcher"
    if platform_name == "windows":
        exe_name += ".exe"
    
    exe_path = Path(f"dist/{exe_name}")
    if exe_path.exists():
        shutil.copy2(exe_path, dist_folder / exe_name)
        print(f"✅ Executable copied to distribution folder: {exe_name}")
    else:
        print(f"❌ Executable not found: {exe_path}")
        return False
    
    # Create README
    readme_content = f'''# Oracle Fusion Resource Fetcher - {platform_name.title()}

## What is this?
This is a standalone application that allows you to fetch and manage Oracle Fusion project resources without needing to install Python or any other dependencies.

## How to use:
1. Double-click `{exe_name}` to start the application
2. The application will open in your default web browser automatically
3. Enter your Oracle Fusion credentials and base URL
4. Click "Fetch Resources" to retrieve your project resources
5. Use the filters and export features as needed

## Features:
- ✅ Fetch Oracle Fusion project resources
- ✅ Filter and search resources
- ✅ Export data to CSV
- ✅ Update person information from HCM
- ✅ No installation required - just run the executable
- ✅ Cross-platform support (Windows, macOS, Linux)

## System Requirements:
- {platform_name.title()}: {get_platform_requirements(platform_name)}
- Internet connection
- Oracle Fusion account with appropriate permissions

## Troubleshooting:
- If the application doesn't start, try running it as administrator (Windows) or with sudo (macOS/Linux)
- Make sure your firewall allows the application to access the internet
- If you get a security warning, this is normal for unsigned executables

## Support:
If you encounter any issues, please contact your system administrator or the development team.

---
Generated on: {platform_name.title()}
Build Date: {subprocess.check_output(['date']).decode().strip()}
'''
    
    with open(dist_folder / "README.txt", 'w') as f:
        f.write(readme_content)
    print("✅ README created")
    
    # Create platform-specific launcher scripts
    if platform_name == "windows":
        create_windows_launcher(dist_folder, exe_name)
    elif platform_name == "macos":
        create_macos_launcher(dist_folder, exe_name)
    elif platform_name == "linux":
        create_linux_launcher(dist_folder, exe_name)
    
    return True

def get_platform_requirements(platform_name):
    """Get system requirements for specific platform"""
    requirements = {
        "windows": "Windows 10/11 (64-bit)",
        "macos": "macOS 10.14+ (Intel or Apple Silicon)",
        "linux": "Linux with glibc 2.17+ (Ubuntu 18.04+, CentOS 7+, etc.)"
    }
    return requirements.get(platform_name, "Compatible operating system")

def create_windows_launcher(dist_folder, exe_name):
    """Create Windows batch launcher"""
    batch_content = f'''@echo off
echo Starting Oracle Fusion Resource Fetcher...
echo.
echo This will open the application in your default web browser.
echo.
pause
start {exe_name}
'''
    
    with open(dist_folder / "Start_Application.bat", 'w') as f:
        f.write(batch_content)
    print("✅ Windows batch launcher created")

def create_macos_launcher(dist_folder, exe_name):
    """Create macOS shell launcher"""
    shell_content = f'''#!/bin/bash
echo "Starting Oracle Fusion Resource Fetcher..."
echo ""
echo "This will open the application in your default web browser."
echo ""
read -p "Press Enter to continue..."
./{exe_name}
'''
    
    with open(dist_folder / "start_application.sh", 'w') as f:
        f.write(shell_content)
    
    # Make shell script executable
    os.chmod(dist_folder / "start_application.sh", 0o755)
    print("✅ macOS shell launcher created")

def create_linux_launcher(dist_folder, exe_name):
    """Create Linux shell launcher"""
    shell_content = f'''#!/bin/bash
echo "Starting Oracle Fusion Resource Fetcher..."
echo ""
echo "This will open the application in your default web browser."
echo ""
read -p "Press Enter to continue..."
./{exe_name}
'''
    
    with open(dist_folder / "start_application.sh", 'w') as f:
        f.write(shell_content)
    
    # Make shell script executable
    os.chmod(dist_folder / "start_application.sh", 0o755)
    print("✅ Linux shell launcher created")

def cleanup(spec_filename):
    """Clean up build artifacts"""
    print("🧹 Cleaning up build artifacts...")
    
    # Remove spec file
    if os.path.exists(spec_filename):
        os.remove(spec_filename)
    
    # Remove build folder
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    # Remove __pycache__ folders
    for root, dirs, files in os.walk("."):
        for dir in dirs:
            if dir == "__pycache__":
                shutil.rmtree(os.path.join(root, dir))
    
    print("✅ Cleanup completed")

def build_for_platform(platform_name):
    """Build executable for specific platform"""
    print(f"\n🔧 Building for {platform_name.title()}...")
    print("=" * 50)
    
    # Create spec file
    spec_filename = create_spec_file(platform_name)
    
    # Build executable
    if not build_executable(spec_filename):
        return False
    
    # Create distribution folder
    if not create_distribution_folder(platform_name):
        return False
    
    # Cleanup
    cleanup(spec_filename)
    
    print(f"✅ {platform_name.title()} build completed successfully!")
    return True

def main():
    """Main build process"""
    print("🔧 Oracle Fusion Resource Fetcher - Cross-Platform Build Script")
    print("=" * 70)
    print("This script will create standalone executables for multiple platforms.")
    print("=" * 70)
    
    # Check if we're in the right directory
    if not os.path.exists("simple_oracle_fetcher.py"):
        print("❌ Error: simple_oracle_fetcher.py not found!")
        print("Please run this script from the directory containing the server files.")
        return
    
    # Install requirements
    if not install_requirements():
        return
    
    # Install PyInstaller
    if not install_pyinstaller():
        return
    
    # Get current platform
    current_platform = get_platform_info()
    print(f"🖥️  Current platform: {current_platform.title()}")
    
    # Ask user which platforms to build for
    print("\n📋 Which platforms would you like to build for?")
    print("1. Current platform only ({})".format(current_platform.title()))
    print("2. All platforms (Windows, macOS, Linux)")
    print("3. Custom selection")
    
    try:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        platforms_to_build = []
        
        if choice == "1":
            platforms_to_build = [current_platform]
        elif choice == "2":
            platforms_to_build = ["windows", "macos", "linux"]
        elif choice == "3":
            print("\nSelect platforms to build:")
            print("1. Windows")
            print("2. macOS") 
            print("3. Linux")
            print("4. All")
            
            custom_choice = input("Enter your choices (comma-separated, e.g., 1,3): ").strip()
            
            platform_map = {"1": "windows", "2": "macos", "3": "linux"}
            if "4" in custom_choice:
                platforms_to_build = ["windows", "macos", "linux"]
            else:
                for num in custom_choice.split(","):
                    num = num.strip()
                    if num in platform_map:
                        platforms_to_build.append(platform_map[num])
        else:
            print("❌ Invalid choice. Building for current platform only.")
            platforms_to_build = [current_platform]
        
        if not platforms_to_build:
            print("❌ No platforms selected. Exiting.")
            return
        
        print(f"\n🎯 Building for: {', '.join([p.title() for p in platforms_to_build])}")
        
        # Build for each platform
        successful_builds = []
        for platform_name in platforms_to_build:
            if build_for_platform(platform_name):
                successful_builds.append(platform_name)
        
        # Summary
        print("\n🎉 Build Summary:")
        print("=" * 50)
        for platform_name in successful_builds:
            dist_folder = f"dist/OracleFusionResourceFetcher_{platform_name}"
            print(f"✅ {platform_name.title()}: {dist_folder}/")
        
        if successful_builds:
            print(f"\n📦 Successfully built {len(successful_builds)} platform(s)")
            print("🚀 You can now share these folders with users on different platforms.")
        else:
            print("❌ No builds were successful.")
        
    except KeyboardInterrupt:
        print("\n👋 Build cancelled by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main() 