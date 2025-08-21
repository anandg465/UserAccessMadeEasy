# Troubleshooting Guide
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
