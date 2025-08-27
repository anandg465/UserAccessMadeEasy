#!/usr/bin/env python3
"""
Windows-Specific Build Script for Oracle Fusion Resource Fetcher
Run this script on a Windows machine to create a Windows executable
"""

import subprocess
import sys
import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def check_windows():
    """Check if running on Windows"""
    if os.name != 'nt':
        print("❌ This script is designed to run on Windows!")
        print("Current OS:", os.name)
        print("Please run this script on a Windows machine.")
        return False
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    dependencies = ["pyinstaller", "requests"]
    
    for dep in dependencies:
        try:
            print(f"Installing {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ {dep} installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing {dep}: {e}")
            return False
    
    return True

def build_windows_executable():
    """Build the Windows executable using PyInstaller"""
    print("🔨 Building Windows executable...")
    
    # Create spec file content for Windows
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
    
    # Write spec file
    with open('oracle_fusion_fetcher_windows.spec', 'w') as f:
        f.write(spec_content)
    
    # Build executable
    try:
        subprocess.check_call([sys.executable, "-m", "PyInstaller", "oracle_fusion_fetcher_windows.spec", "--clean"])
        print("✅ Windows executable built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error building executable: {e}")
        return False

def create_windows_package():
    """Create the Windows user package"""
    print("📦 Creating Windows user package...")
    
    # Check if executable exists
    exe_path = Path("dist/OracleFusionResourceFetcher.exe")
    if not exe_path.exists():
        print("❌ Error: Windows executable not found!")
        print("Expected path:", exe_path)
        return False
    
    # Create package directory
    package_dir = Path("OracleFusionResourceFetcher_Windows_Package")
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    # Copy executable
    shutil.copy2(exe_path, package_dir / "OracleFusionResourceFetcher.exe")
    
    # Create Windows-specific documentation
    create_windows_documentation(package_dir)
    create_windows_launchers(package_dir)
    create_zip_package(package_dir)
    
    return True

def create_windows_documentation(package_dir):
    """Create Windows-specific documentation"""
    
    # Main README
    readme_content = f'''# Oracle Fusion Resource Fetcher - Windows Edition
## Standalone Application Package

### 🎯 What is this?
This is a **standalone Windows application** that allows you to fetch and manage Oracle Fusion project resources. 
**No installation required** - just run the executable and start using it!

### ✨ Features
- 🔍 **Fetch Oracle Fusion Resources**: Retrieve all project resources from your Oracle Fusion instance
- 🔎 **Advanced Filtering**: Filter resources by name, email, role, manager, and more
- 📊 **Data Export**: Export filtered data to CSV format
- 🔄 **Update Person Info**: Update person information from HCM for selected resources
- 🌐 **Web Interface**: Modern, user-friendly web interface
- 🔒 **Secure**: Uses your existing Oracle Fusion credentials
- 🚀 **No Installation**: Runs directly without requiring Python or any dependencies

### 🖥️ System Requirements
- **Windows**: Windows 10/11 (64-bit)
- **Internet Connection**: Required to connect to Oracle Fusion
- **Oracle Fusion Account**: With appropriate permissions to access project resources

### 🚀 Quick Start
1. **Extract** this package to any folder on your computer
2. **Double-click** `OracleFusionResourceFetcher.exe` or run `Start_Application.bat`
3. **Wait** for the application to start (it will open in your default web browser)
4. **Enter** your Oracle Fusion credentials:
   - Base URL (e.g., https://your-instance.oraclecloud.com)
   - Username
   - Password
5. **Click** "Fetch Resources" to retrieve your project resources
6. **Use** the filters and export features as needed

### 📋 Detailed Instructions

#### Starting the Application
- **Option 1**: Double-click `OracleFusionResourceFetcher.exe`
- **Option 2**: Double-click `Start_Application.bat`
- **Option 3**: Right-click `OracleFusionResourceFetcher.exe` → "Run as administrator"

#### Using the Application
1. **Enter Credentials**:
   - Base URL: Your Oracle Fusion instance URL (e.g., https://your-instance.oraclecloud.com)
   - Username: Your Oracle Fusion username
   - Password: Your Oracle Fusion password

2. **Fetch Resources**:
   - Click "Fetch Resources" button
   - Wait for the data to load (this may take a few moments)
   - View your resources in the table

3. **Filter and Search**:
   - Use the filter section to search by name, email, role, etc.
   - Click column headers to sort data
   - Use the "Toggle Filters" button to show/hide filter options

4. **Export Data**:
   - Click "Export to CSV" to download filtered data
   - The file will be saved to your Downloads folder

5. **Update Person Information**:
   - Click "Update Person Info" button
   - Select resources you want to update
   - Click "Update Selected Resources"
   - View results and download error log if needed

### 🔧 Windows-Specific Troubleshooting

#### Application Won't Start
- **Error**: "Windows protected your PC"
  - **Solution**: Click "More info" → "Run anyway"
- **Error**: "Access denied"
  - **Solution**: Right-click → "Run as administrator"
- **Error**: "This app can't run on your PC"
  - **Solution**: Make sure you're using Windows 10/11 (64-bit)

#### Security Warnings
- **Windows Defender**: You may see a security warning. Click "More info" → "Run anyway"
- **SmartScreen**: If blocked, click "More info" → "Run anyway"
- **Antivirus**: Some antivirus software may flag the executable. Add it to exclusions if needed.

#### Connection Issues
- Check your internet connection
- Verify your Oracle Fusion base URL is correct
- Ensure your firewall allows the application to access the internet
- Check that your Oracle Fusion credentials are correct

#### Authentication Errors
- Verify your username and password
- Check that your account has permission to access project resources
- Ensure your Oracle Fusion instance is accessible

### 📞 Support
If you encounter any issues:
1. Check the troubleshooting guide in this package
2. Contact your system administrator
3. Contact the development team

### 🔒 Security Notes
- This application runs locally on your computer
- Your credentials are only sent to Oracle Fusion servers
- No data is stored permanently on your computer
- The application does not collect or transmit any personal information

### 📄 License
This application is provided as-is for internal use.

---
**Package Version**: 1.0
**Build Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Platform**: Windows
**Compatible with**: Oracle Fusion Cloud
'''
    
    with open(package_dir / "README.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    # Quick Start Guide
    quick_start_content = '''# Quick Start Guide - Windows
## Oracle Fusion Resource Fetcher

### ⚡ 5-Minute Setup

1. **Extract** this folder to your desktop or any location
2. **Double-click** `OracleFusionResourceFetcher.exe`
3. **Wait** for your browser to open automatically
4. **Enter** your Oracle Fusion details:
   - Base URL: `https://your-instance.oraclecloud.com`
   - Username: Your Oracle Fusion username
   - Password: Your Oracle Fusion password
5. **Click** "Fetch Resources"
6. **Done!** Your resources will appear in the table

### 🎯 Common Tasks

#### Export Data to Excel
1. Use filters to find the data you need
2. Click "Export to CSV"
3. Open the CSV file in Excel

#### Update Person Information
1. Click "Update Person Info"
2. Select the resources you want to update
3. Click "Update Selected Resources"
4. Check the results

### 🆘 Need Help?
- Check `TROUBLESHOOTING.md` for common issues
- Contact your IT support team
'''
    
    with open(package_dir / "QUICK_START.md", 'w', encoding='utf-8') as f:
        f.write(quick_start_content)
    
    # Troubleshooting Guide
    troubleshooting_content = '''# Troubleshooting Guide - Windows
## Oracle Fusion Resource Fetcher

### ❌ Application Won't Start

#### "Windows protected your PC"
- **Solution**: Click "More info" → "Run anyway"
- **Why**: Windows Defender blocks unsigned executables

#### "Access denied"
- **Solution**: Right-click → "Run as administrator"
- **Why**: Application needs elevated permissions

#### "This app can't run on your PC"
- **Solution**: Make sure you're using Windows 10/11 (64-bit)
- **Why**: Application requires 64-bit Windows

#### "SmartScreen blocked this app"
- **Solution**: Click "More info" → "Run anyway"
- **Why**: SmartScreen blocks unknown applications

### 🌐 Connection Issues

#### "Connection Error"
- Check your internet connection
- Verify your Oracle Fusion base URL
- Try accessing Oracle Fusion in your browser first

#### "Authentication Failed"
- Double-check your username and password
- Ensure your account is active
- Check if your password has expired

#### "Access Denied"
- Verify you have permission to access project resources
- Contact your Oracle Fusion administrator

### 📊 Data Issues

#### "No Resources Found"
- Check your Oracle Fusion permissions
- Verify the API endpoint is correct
- Try with a different account

#### "Export Failed"
- Check if you have write permissions to the Downloads folder
- Try saving to a different location
- Close any open Excel files

### 🔄 Update Issues

#### "Update Failed"
- Check the error log for specific details
- Verify you have update permissions
- Try updating fewer resources at once

### 📞 Getting Help

1. **Check this guide** for your specific error
2. **Note the exact error message**
3. **Contact your IT support** with:
   - Error message
   - Steps you followed
   - Your Windows version

### 🔧 Advanced Troubleshooting

#### Check Application Logs
- Look for any `.log` files in the application folder
- Check the browser's developer console (F12)

#### Test Oracle Fusion Access
- Try accessing Oracle Fusion directly in your browser
- Verify your credentials work there

#### Network Issues
- Check if you're behind a corporate firewall
- Verify proxy settings if applicable
- Try from a different network if possible

#### Windows-Specific Issues
- **Antivirus blocking**: Add the executable to antivirus exclusions
- **Firewall blocking**: Allow the application through Windows Firewall
- **UAC issues**: Run as administrator or disable UAC temporarily
'''
    
    with open(package_dir / "TROUBLESHOOTING.md", 'w', encoding='utf-8') as f:
        f.write(troubleshooting_content)
    
    # Version Info
    version_content = f'''Oracle Fusion Resource Fetcher - Windows Edition
Version: 1.0
Build Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Platform: Windows (64-bit)
Dependencies: None (Standalone)

Features:
- Fetch Oracle Fusion project resources
- Filter and search functionality
- Export to CSV
- Update person information from HCM
- Web-based interface
- No installation required

System Requirements:
- Windows 10/11 (64-bit)
- Internet connection
- Oracle Fusion account with appropriate permissions

For support, contact your system administrator.
'''
    
    with open(package_dir / "VERSION.txt", 'w') as f:
        f.write(version_content)
    
    print("✅ Windows documentation created")

def create_windows_launchers(package_dir):
    """Create Windows-specific launcher scripts"""
    
    # Windows batch launcher
    batch_content = '''@echo off
title Oracle Fusion Resource Fetcher - Windows Edition
color 0A

echo.
echo ========================================
echo   Oracle Fusion Resource Fetcher
echo   Windows Edition
echo ========================================
echo.
echo Starting application...
echo This will open in your default web browser.
echo.
echo If the application doesn't start automatically,
echo please double-click OracleFusionResourceFetcher.exe
echo.
echo Press any key to continue...
pause >nul

start OracleFusionResourceFetcher.exe

echo.
echo Application started!
echo Check your web browser for the interface.
echo.
echo Press any key to close this window...
pause >nul
'''
    
    with open(package_dir / "Start_Application.bat", 'w') as f:
        f.write(batch_content)
    
    # Create a PowerShell launcher as well
    powershell_content = '''# Oracle Fusion Resource Fetcher - PowerShell Launcher
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Oracle Fusion Resource Fetcher" -ForegroundColor Green
Write-Host "  Windows Edition" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Starting application..." -ForegroundColor Yellow
Write-Host "This will open in your default web browser." -ForegroundColor White
Write-Host ""
Write-Host "If the application doesn't start automatically," -ForegroundColor White
Write-Host "please double-click OracleFusionResourceFetcher.exe" -ForegroundColor White
Write-Host ""

# Start the application
Start-Process -FilePath "OracleFusionResourceFetcher.exe"

Write-Host ""
Write-Host "Application started!" -ForegroundColor Green
Write-Host "Check your web browser for the interface." -ForegroundColor White
Write-Host ""
'''
    
    with open(package_dir / "Start_Application.ps1", 'w') as f:
        f.write(powershell_content)
    
    print("✅ Windows launchers created")

def create_zip_package(package_dir):
    """Create a ZIP file of the Windows package"""
    zip_filename = f"{package_dir.name}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in package_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(package_dir)
                zipf.write(file_path, arcname)
    
    print(f"✅ Windows ZIP package created: {zip_filename}")

def cleanup():
    """Clean up build artifacts"""
    print("🧹 Cleaning up build artifacts...")
    
    # Remove spec file
    if os.path.exists("oracle_fusion_fetcher_windows.spec"):
        os.remove("oracle_fusion_fetcher_windows.spec")
    
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
    """Main function - Windows build and package"""
    print("🔧 Oracle Fusion Resource Fetcher - Windows Build & Package")
    print("=" * 70)
    print("This script will:")
    print("1. Install required dependencies")
    print("2. Build the Windows executable")
    print("3. Create a Windows user package")
    print("4. Generate a ZIP file for easy sharing")
    print("=" * 70)
    
    # Check if running on Windows
    if not check_windows():
        return
    
    # Check if we're in the right directory
    if not os.path.exists("simple_oracle_fetcher.py"):
        print("❌ Error: simple_oracle_fetcher.py not found!")
        print("Please run this script from the directory containing the server files.")
        return
    
    try:
        # Step 1: Install dependencies
        if not install_dependencies():
            print("❌ Failed to install dependencies")
            return
        
        # Step 2: Build Windows executable
        if not build_windows_executable():
            print("❌ Failed to build Windows executable")
            return
        
        # Step 3: Create Windows user package
        if not create_windows_package():
            print("❌ Failed to create Windows user package")
            return
        
        # Step 4: Cleanup
        cleanup()
        
        print("\n🎉 SUCCESS! Windows package completed successfully!")
        print("=" * 70)
        print("📦 Your Windows user package is ready:")
        print(f"   📁 Folder: OracleFusionResourceFetcher_Windows_Package/")
        print(f"   📦 ZIP: OracleFusionResourceFetcher_Windows_Package.zip")
        print("")
        print("🚀 You can now share this package with Windows users!")
        print("✅ Windows users can run it without installing Python or any dependencies")
        print("=" * 70)
        
    except KeyboardInterrupt:
        print("\n👋 Build cancelled by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main() 