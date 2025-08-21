#!/usr/bin/env python3
"""
Create User-Friendly Package for Oracle Fusion Resource Fetcher
Creates a complete package that can be easily shared with end users
"""

import subprocess
import sys
import os
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def create_user_package():
    """Create a complete user-friendly package"""
    print("📦 Creating User-Friendly Package for Oracle Fusion Resource Fetcher")
    print("=" * 70)
    
    # Check if executable exists
    exe_path = Path("dist/OracleFusionResourceFetcher.exe")
    if not exe_path.exists():
        print("❌ Error: Executable not found!")
        print("Please run build_executable.py or build_cross_platform.py first.")
        return False
    
    # Create package directory
    package_dir = Path("OracleFusionResourceFetcher_Package")
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    print(f"📁 Creating package in: {package_dir}")
    
    # Copy executable
    shutil.copy2(exe_path, package_dir / "OracleFusionResourceFetcher.exe")
    print("✅ Executable copied")
    
    # Create comprehensive README
    create_comprehensive_readme(package_dir)
    
    # Create quick start guide
    create_quick_start_guide(package_dir)
    
    # Create troubleshooting guide
    create_troubleshooting_guide(package_dir)
    
    # Create batch launcher
    create_batch_launcher(package_dir)
    
    # Create shell launcher for macOS/Linux
    create_shell_launcher(package_dir)
    
    # Create version info
    create_version_info(package_dir)
    
    # Create ZIP file
    create_zip_package(package_dir)
    
    print("\n🎉 Package created successfully!")
    print("=" * 50)
    print(f"📦 Package location: {package_dir}")
    print(f"📦 ZIP file: {package_dir}.zip")
    print("🚀 You can now share this package with users!")
    print("=" * 50)
    
    return True

def create_comprehensive_readme(package_dir):
    """Create a comprehensive README file"""
    readme_content = '''# Oracle Fusion Resource Fetcher
## Standalone Application Package

### 🎯 What is this?
This is a **standalone application** that allows you to fetch and manage Oracle Fusion project resources. 
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
- **macOS**: macOS 10.14+ (Intel or Apple Silicon)
- **Linux**: Linux with glibc 2.17+ (Ubuntu 18.04+, CentOS 7+, etc.)
- **Internet Connection**: Required to connect to Oracle Fusion
- **Oracle Fusion Account**: With appropriate permissions to access project resources

### 🚀 Quick Start
1. **Extract** this package to any folder on your computer
2. **Double-click** `OracleFusionResourceFetcher.exe` (Windows) or run `./OracleFusionResourceFetcher` (macOS/Linux)
3. **Wait** for the application to start (it will open in your default web browser)
4. **Enter** your Oracle Fusion credentials:
   - Base URL (e.g., https://your-instance.oraclecloud.com)
   - Username
   - Password
5. **Click** "Fetch Resources" to retrieve your project resources
6. **Use** the filters and export features as needed

### 📋 Detailed Instructions

#### Starting the Application
- **Windows**: Double-click `OracleFusionResourceFetcher.exe` or run `Start_Application.bat`
- **macOS/Linux**: Run `./start_application.sh` or `./OracleFusionResourceFetcher`

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

### 🔧 Troubleshooting

#### Application Won't Start
- **Windows**: Try running as administrator (right-click → "Run as administrator")
- **macOS**: Try running from Terminal: `./OracleFusionResourceFetcher`
- **Linux**: Try running with sudo: `sudo ./OracleFusionResourceFetcher`

#### Security Warnings
- **Windows**: You may see a "Windows protected your PC" message. Click "More info" → "Run anyway"
- **macOS**: You may see a "macOS cannot verify the developer" message. Go to System Preferences → Security & Privacy → Allow

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
**Build Date**: {build_date}
**Compatible with**: Oracle Fusion Cloud
'''.format(build_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    with open(package_dir / "README.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("✅ Comprehensive README created")

def create_quick_start_guide(package_dir):
    """Create a quick start guide"""
    quick_start_content = '''# Quick Start Guide
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
    print("✅ Quick start guide created")

def create_troubleshooting_guide(package_dir):
    """Create a troubleshooting guide"""
    troubleshooting_content = '''# Troubleshooting Guide
## Oracle Fusion Resource Fetcher

### ❌ Application Won't Start

#### Windows
- **Error**: "Windows protected your PC"
  - **Solution**: Click "More info" → "Run anyway"
- **Error**: "Access denied"
  - **Solution**: Right-click → "Run as administrator"

#### macOS
- **Error**: "macOS cannot verify the developer"
  - **Solution**: System Preferences → Security & Privacy → Allow
- **Error**: "Permission denied"
  - **Solution**: Run in Terminal: `chmod +x OracleFusionResourceFetcher && ./OracleFusionResourceFetcher`

#### Linux
- **Error**: "Permission denied"
  - **Solution**: Run `chmod +x OracleFusionResourceFetcher && ./OracleFusionResourceFetcher`
- **Error**: "Command not found"
  - **Solution**: Make sure you're in the correct directory

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
   - Your operating system

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
'''
    
    with open(package_dir / "TROUBLESHOOTING.md", 'w', encoding='utf-8') as f:
        f.write(troubleshooting_content)
    print("✅ Troubleshooting guide created")

def create_batch_launcher(package_dir):
    """Create Windows batch launcher"""
    batch_content = '''@echo off
title Oracle Fusion Resource Fetcher
color 0A

echo.
echo ========================================
echo   Oracle Fusion Resource Fetcher
echo ========================================
echo.
echo Starting application...
echo This will open in your default web browser.
echo.
echo If the application doesn't start automatically,
echo please double-click OracleFusionResourceFetcher.exe
echo.
pause

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
    print("✅ Windows batch launcher created")

def create_shell_launcher(package_dir):
    """Create shell launcher for macOS/Linux"""
    shell_content = '''#!/bin/bash

# Colors for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
NC='\\033[0m' # No Color

echo ""
echo -e "${GREEN}========================================"
echo -e "  Oracle Fusion Resource Fetcher"
echo -e "========================================${NC}"
echo ""
echo -e "${YELLOW}Starting application...${NC}"
echo "This will open in your default web browser."
echo ""
echo "If the application doesn't start automatically,"
echo "please run: ./OracleFusionResourceFetcher"
echo ""

# Make executable if needed
if [ ! -x "./OracleFusionResourceFetcher" ]; then
    echo -e "${YELLOW}Making executable...${NC}"
    chmod +x ./OracleFusionResourceFetcher
fi

# Start the application
./OracleFusionResourceFetcher

echo ""
echo -e "${GREEN}Application started!${NC}"
echo "Check your web browser for the interface."
echo ""
'''
    
    with open(package_dir / "start_application.sh", 'w') as f:
        f.write(shell_content)
    
    # Make shell script executable
    os.chmod(package_dir / "start_application.sh", 0o755)
    print("✅ Shell launcher created")

def create_version_info(package_dir):
    """Create version information file"""
    version_content = f'''Oracle Fusion Resource Fetcher
Version: 1.0
Build Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Platform: Cross-Platform (Windows, macOS, Linux)
Dependencies: None (Standalone)

Features:
- Fetch Oracle Fusion project resources
- Filter and search functionality
- Export to CSV
- Update person information from HCM
- Web-based interface
- No installation required

System Requirements:
- Windows 10/11, macOS 10.14+, or Linux
- Internet connection
- Oracle Fusion account with appropriate permissions

For support, contact your system administrator.
'''
    
    with open(package_dir / "VERSION.txt", 'w') as f:
        f.write(version_content)
    print("✅ Version info created")

def create_zip_package(package_dir):
    """Create a ZIP file of the package"""
    zip_filename = f"{package_dir.name}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in package_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(package_dir)
                zipf.write(file_path, arcname)
    
    print(f"✅ ZIP package created: {zip_filename}")

def main():
    """Main function"""
    print("🔧 Oracle Fusion Resource Fetcher - User Package Creator")
    print("=" * 70)
    
    # Check if executable exists
    if not Path("dist/OracleFusionResourceFetcher.exe").exists():
        print("❌ Error: Executable not found!")
        print("Please run one of these first:")
        print("  - python build_executable.py")
        print("  - python build_cross_platform.py")
        return
    
    # Create the package
    if create_user_package():
        print("\n🎉 Success! Your user package is ready.")
        print("📦 Share the ZIP file or folder with your users.")
        print("🚀 Users can run it without installing anything!")
    else:
        print("❌ Failed to create package.")

if __name__ == "__main__":
    main() 