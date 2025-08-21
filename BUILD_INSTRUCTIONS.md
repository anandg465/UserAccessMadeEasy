# Oracle Fusion Resource Fetcher - Build Instructions

## Overview
This guide explains how to create standalone executables and user-friendly packages for the Oracle Fusion Resource Fetcher application.

## 🎯 What You'll Create
- **Standalone Executable**: A single file that users can run without installing Python
- **User Package**: A complete package with documentation and launchers
- **Cross-Platform Support**: Works on Windows, macOS, and Linux

## 🚀 Quick Start (Recommended)

### Option 1: One-Command Build (Easiest)
```bash
python build_and_package.py
```

This single command will:
1. Install required dependencies (PyInstaller, requests)
2. Build the standalone executable
3. Create a user-friendly package
4. Generate a ZIP file for easy sharing

**Result**: You'll get `OracleFusionResourceFetcher_Package.zip` ready to share with users!

### Option 2: Step-by-Step Build

#### Step 1: Build Executable
```bash
python build_executable.py
```

#### Step 2: Create User Package
```bash
python create_user_package.py
```

### Option 3: Cross-Platform Build
```bash
python build_cross_platform.py
```

This allows you to build for multiple platforms (Windows, macOS, Linux).

## 📦 What Gets Created

### Executable Files
- `dist/OracleFusionResourceFetcher.exe` (Windows)
- `dist/OracleFusionResourceFetcher` (macOS/Linux)

### User Package Contents
```
OracleFusionResourceFetcher_Package/
├── OracleFusionResourceFetcher.exe    # Main executable
├── README.md                          # Comprehensive documentation
├── QUICK_START.md                     # 5-minute setup guide
├── TROUBLESHOOTING.md                 # Common issues and solutions
├── VERSION.txt                        # Version information
├── Start_Application.bat              # Windows launcher
├── start_application.sh               # macOS/Linux launcher
└── OracleFusionResourceFetcher_Package.zip  # Complete package
```

## 🖥️ System Requirements for Building

### Windows
- Python 3.7+ installed
- Internet connection (to download dependencies)

### macOS
- Python 3.7+ installed
- Xcode Command Line Tools (for some dependencies)
- Internet connection

### Linux
- Python 3.7+ installed
- Build tools (gcc, make)
- Internet connection

## 🔧 Detailed Build Process

### 1. Install Dependencies
The build scripts automatically install:
- **PyInstaller**: Creates standalone executables
- **requests**: HTTP library for API calls

### 2. Create Executable
PyInstaller bundles your Python application with all dependencies into a single executable file.

### 3. Package for Distribution
Creates a user-friendly package with:
- Executable file
- Documentation
- Launcher scripts
- ZIP file for easy sharing

## 📋 Build Scripts Explained

### `build_and_package.py` (Recommended)
- **Purpose**: Complete build and package in one command
- **Best for**: Most users, quick setup
- **Output**: Ready-to-share ZIP file

### `build_executable.py`
- **Purpose**: Build executable only
- **Best for**: Developers who want just the executable
- **Output**: Executable in `dist/` folder

### `build_cross_platform.py`
- **Purpose**: Build for multiple platforms
- **Best for**: Distributing to users on different operating systems
- **Output**: Platform-specific packages

### `create_user_package.py`
- **Purpose**: Create user package from existing executable
- **Best for**: When you already have an executable
- **Output**: Complete user package

## 🎯 Sharing with Users

### What Users Get
1. **No Installation Required**: Users don't need Python or any dependencies
2. **Cross-Platform**: Works on Windows, macOS, and Linux
3. **Self-Contained**: Everything needed is in the package
4. **Documentation**: Complete guides and troubleshooting

### How Users Use It
1. Extract the ZIP file
2. Double-click the executable (or use launcher scripts)
3. Application opens in their web browser
4. Enter Oracle Fusion credentials
5. Start using the application

## 🔧 Troubleshooting Build Issues

### Common Issues

#### "PyInstaller not found"
```bash
pip install pyinstaller
```

#### "Permission denied" (macOS/Linux)
```bash
chmod +x build_and_package.py
python build_and_package.py
```

#### "Executable not found"
Make sure you're running the script from the directory containing `simple_oracle_fetcher.py`

#### "Build failed"
- Check your internet connection
- Ensure you have sufficient disk space
- Try running as administrator (Windows) or with sudo (macOS/Linux)

### Advanced Troubleshooting

#### Clean Build
```bash
# Remove previous builds
rm -rf dist/ build/ __pycache__/
rm -f *.spec

# Rebuild
python build_and_package.py
```

#### Debug Build
```bash
# Build with debug information
pyinstaller --debug=all simple_oracle_fetcher.py
```

## 📊 File Sizes

Typical file sizes:
- **Executable**: 15-25 MB
- **User Package**: 20-30 MB
- **ZIP File**: 15-25 MB

## 🔒 Security Considerations

### For Builders
- The executable contains your application code
- No sensitive data is embedded
- Users' credentials are only sent to Oracle Fusion servers

### For Users
- Application runs locally on their computer
- No data is stored permanently
- No personal information is collected or transmitted

## 📞 Support

### For Build Issues
1. Check this guide
2. Verify system requirements
3. Try clean build process
4. Contact development team

### For User Issues
1. Check troubleshooting guide in the package
2. Verify Oracle Fusion credentials
3. Check network connectivity
4. Contact system administrator

## 🚀 Next Steps

After building:
1. Test the executable on a clean system
2. Share the ZIP file with users
3. Provide support documentation
4. Collect feedback for improvements

---

**Build Date**: Generated automatically
**Version**: 1.0
**Compatible with**: Oracle Fusion Cloud 