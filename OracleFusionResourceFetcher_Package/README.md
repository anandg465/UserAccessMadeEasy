# Oracle Fusion Resource Fetcher
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
**Build Date**: 2025-08-18 19:38:59
**Compatible with**: Oracle Fusion Cloud
