#!/usr/bin/env python3
"""
Build Script for Oracle Fusion Resource Fetcher
Creates a standalone executable that can be shared with users who don't have Python installed
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path

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

def create_spec_file():
    """Create PyInstaller spec file"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

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
    hooksconfig={},
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
    name='OracleFusionResourceFetcher',
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
    
    with open('oracle_fusion_fetcher.spec', 'w') as f:
        f.write(spec_content)
    print("✅ Spec file created successfully!")

def build_executable():
    """Build the executable using PyInstaller"""
    print("🔨 Building executable...")
    try:
        # Use the spec file for more control
        subprocess.check_call([sys.executable, "-m", "PyInstaller", "oracle_fusion_fetcher.spec", "--clean"])
        print("✅ Executable built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error building executable: {e}")
        return False

def create_distribution_folder():
    """Create a distribution folder with the executable and documentation"""
    print("📁 Creating distribution folder...")
    
    # Create dist folder
    dist_folder = Path("dist/OracleFusionResourceFetcher")
    dist_folder.mkdir(parents=True, exist_ok=True)
    
    # Copy executable
    exe_path = Path("dist/OracleFusionResourceFetcher.exe")
    if exe_path.exists():
        shutil.copy2(exe_path, dist_folder / "OracleFusionResourceFetcher.exe")
        print("✅ Executable copied to distribution folder")
    else:
        print("❌ Executable not found!")
        return False
    
    # Create README
    readme_content = '''# Oracle Fusion Resource Fetcher

## What is this?
This is a standalone application that allows you to fetch and manage Oracle Fusion project resources without needing to install Python or any other dependencies.

## How to use:
1. Double-click `OracleFusionResourceFetcher.exe` to start the application
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
- ✅ Works on Windows, macOS, and Linux

## System Requirements:
- Windows 10/11, macOS 10.14+, or Linux
- Internet connection
- Oracle Fusion account with appropriate permissions

## Troubleshooting:
- If the application doesn't start, try running it as administrator
- Make sure your firewall allows the application to access the internet
- If you get a security warning, this is normal for unsigned executables

## Support:
If you encounter any issues, please contact your system administrator or the development team.

---
Generated on: {date}
'''.format(date=subprocess.check_output(['date']).decode().strip())
    
    with open(dist_folder / "README.txt", 'w') as f:
        f.write(readme_content)
    print("✅ README created")
    
    # Create batch file for Windows users
    batch_content = '''@echo off
echo Starting Oracle Fusion Resource Fetcher...
echo.
echo This will open the application in your default web browser.
echo.
pause
start OracleFusionResourceFetcher.exe
'''
    
    with open(dist_folder / "Start_Application.bat", 'w') as f:
        f.write(batch_content)
    print("✅ Batch file created")
    
    # Create shell script for macOS/Linux users
    shell_content = '''#!/bin/bash
echo "Starting Oracle Fusion Resource Fetcher..."
echo ""
echo "This will open the application in your default web browser."
echo ""
read -p "Press Enter to continue..."
./OracleFusionResourceFetcher
'''
    
    with open(dist_folder / "start_application.sh", 'w') as f:
        f.write(shell_content)
    
    # Make shell script executable
    os.chmod(dist_folder / "start_application.sh", 0o755)
    print("✅ Shell script created")
    
    return True

def cleanup():
    """Clean up build artifacts"""
    print("🧹 Cleaning up build artifacts...")
    
    # Remove spec file
    if os.path.exists("oracle_fusion_fetcher.spec"):
        os.remove("oracle_fusion_fetcher.spec")
    
    # Remove build folder
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    # Remove __pycache__ folders
    for root, dirs, files in os.walk("."):
        for dir in dirs:
            if dir == "__pycache__":
                shutil.rmtree(os.path.join(root, dir))
    
    print("✅ Cleanup completed")

def main():
    """Main build process"""
    print("🔧 Oracle Fusion Resource Fetcher - Build Script")
    print("=" * 60)
    print("This script will create a standalone executable that can be")
    print("shared with users who don't have Python installed.")
    print("=" * 60)
    
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
    
    # Create spec file
    create_spec_file()
    
    # Build executable
    if not build_executable():
        return
    
    # Create distribution folder
    if not create_distribution_folder():
        return
    
    # Cleanup
    cleanup()
    
    print("\n🎉 Build completed successfully!")
    print("=" * 60)
    print("📁 Your executable is ready in: dist/OracleFusionResourceFetcher/")
    print("📦 You can now share this folder with other users.")
    print("🚀 Users just need to run OracleFusionResourceFetcher.exe")
    print("=" * 60)

if __name__ == "__main__":
    main() 