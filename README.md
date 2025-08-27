# Oracle Fusion HCM User Management Tool

A comprehensive, modern web application for managing Oracle Fusion HCM users, roles, data security contexts, and areas of responsibility. Built with FastAPI backend and modern web technologies for a beautiful, responsive user experience.

## 🌟 Features

### Core Functionality
- **User Management**: Get comprehensive user details including roles and data security
- **Role Management**: Assign and remove roles from users with bulk operations
- **Data Security Contexts**: Manage data security contexts for users and roles
- **Areas of Responsibility (AOR)**: Assign and manage AORs for users
- **Password Management**: Reset and update user passwords
- **Search & Filtering**: Advanced search capabilities for users and AORs

### Bulk Operations
- **Excel Upload**: Upload Excel files for bulk operations
- **Bulk Role Assignment**: Process multiple role assignments at once
- **Bulk Data Security Assignment**: Assign data security contexts in bulk
- **Bulk AOR Assignment**: Assign areas of responsibility in bulk
- **Template Downloads**: Pre-built Excel templates for different operations

### User Experience
- **Modern UI**: Beautiful, responsive design with customizable theming
- **Client Branding**: Customizable colors, logos, and company branding
- **Cross-Platform**: Works on Windows, Mac, and Linux
- **Real-time Updates**: Live dashboard with auto-refresh capabilities
- **Activity Logs**: Track all operations and system activities

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Oracle Fusion HCM instance with API access
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/anand.gaurav@hotmail.com/UserAccessMadeEasy.git
   cd UserAccessMadeEasy
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the backend server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Open the application**
   - Navigate to `http://localhost:8000` in your browser
   - Or open `frontend/index.html` directly in your browser

## 📋 Configuration

### Oracle Fusion Connection
1. Enter your Oracle Fusion instance URL
2. Provide your API username and password
3. Click "Test Connection" to verify
4. Click "Connect" to establish the connection

### Application Settings
- **Theme**: Choose between Default, Dark, and Light themes
- **Auto Refresh**: Set automatic refresh interval for dashboard
- **Client Branding**: Customize colors, company name, and logo

## 🎯 Usage Guide

### Getting User Details
1. Navigate to "User Details" section
2. Enter the username
3. Click "Get Details" to view comprehensive user information
4. View assigned roles, areas of responsibility, and data security contexts

### Role Management
1. Go to "Role Management" section
2. Choose "Assign Role" or "Remove Role" tab
3. Enter username and role name
4. Submit the form to perform the operation

### Bulk Operations
1. Navigate to "Excel Upload" section
2. Download the appropriate template
3. Fill in the data according to the template format
4. Upload the Excel file
5. Select the operation type
6. Process the bulk operation

### Data Security Contexts
1. Go to "Data Security" section
2. Enter username, role name, security context, and value
3. Submit to assign the data security context

### Areas of Responsibility
1. Navigate to "Areas of Responsibility" section
2. Choose assign or remove operation
3. Enter the required details
4. Submit to perform the operation

## 📁 Project Structure

```
UserAccessMadeEasy/
├── app/                          # FastAPI backend
│   ├── __init__.py
│   ├── main.py                   # FastAPI application entry point
│   ├── api.py                    # API endpoints
│   ├── oracle_client.py          # Oracle Fusion API client
│   ├── schemas.py                # Pydantic data models
│   ├── models.py                 # Database models
│   ├── crud.py                   # Database operations
│   ├── database.py               # Database configuration
│   ├── deps.py                   # Dependencies
│   └── config.py                 # Application configuration
├── frontend/                     # Web frontend
│   ├── index.html                # Main HTML file
│   ├── styles.css                # CSS styles
│   └── app.js                    # JavaScript application
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── .gitignore                    # Git ignore rules
└── build_scripts/                # Build and packaging scripts
    ├── build_executable.py       # Create desktop executable
    ├── build_cross_platform.py   # Cross-platform build
    └── create_user_package.py    # User package creation
```

## 🔧 API Endpoints

### User Management
- `GET /users/` - Get all users
- `POST /users/details` - Get comprehensive user details
- `POST /users/roles/assign` - Assign role to user
- `POST /users/roles/remove` - Remove role from user
- `POST /users/roles/bulk-assign` - Bulk role assignment

### Data Security
- `POST /users/data-security/assign` - Assign data security context
- `POST /users/data-security/bulk-assign` - Bulk data security assignment

### Areas of Responsibility
- `GET /areas-of-responsibility/` - Get all AORs
- `POST /areas-of-responsibility/assign` - Assign AOR to user
- `POST /areas-of-responsibility/remove` - Remove AOR from user
- `POST /areas-of-responsibility/bulk-assign` - Bulk AOR assignment

### Password Management
- `POST /users/password/reset` - Reset user password
- `POST /users/password/update` - Update user password

### File Operations
- `POST /upload/excel` - Upload Excel file for bulk operations
- `GET /users/download` - Download users as Excel file

### Search
- `POST /users/search` - Search users with criteria
- `POST /areas-of-responsibility/search` - Search AORs

## 🛠️ Development

### Backend Development
```bash
# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
pytest

# Format code
black app/
```

### Frontend Development
```bash
# Open frontend/index.html in browser
# Or serve with a local server
python -m http.server 8080
```

### Building Executables
```bash
# Build for current platform
python build_scripts/build_executable.py

# Build cross-platform package
python build_scripts/build_cross_platform.py

# Create user package
python build_scripts/create_user_package.py
```

## 🔒 Security

- **API Authentication**: Uses Oracle Fusion API authentication
- **Password Security**: Passwords are not stored locally
- **HTTPS Support**: Configure for production use
- **Input Validation**: All inputs are validated and sanitized
- **Error Handling**: Comprehensive error handling without exposing sensitive data

## 🌐 Deployment

### Local Development
```bash
# Start backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Open frontend
open frontend/index.html
```

### Production Deployment
```bash
# Install production dependencies
pip install -r requirements.txt

# Start production server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4

# Serve frontend with nginx or similar
```

### Docker Deployment
```bash
# Build Docker image
docker build -t oracle-fusion-hcm .

# Run container
docker run -p 8000:8000 oracle-fusion-hcm
```

## 📊 Monitoring & Logging

- **Activity Logs**: Track all user operations
- **Error Logging**: Comprehensive error tracking
- **Performance Monitoring**: API response time tracking
- **User Analytics**: Usage statistics and metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the [Wiki](https://github.com/anand.gaurav@hotmail.com/UserAccessMadeEasy/wiki)
- **Issues**: Report bugs and request features via [GitHub Issues](https://github.com/anand.gaurav@hotmail.com/UserAccessMadeEasy/issues)
- **Discussions**: Join the [GitHub Discussions](https://github.com/anand.gaurav@hotmail.com/UserAccessMadeEasy/discussions)

## 🔄 Updates & Upgrades

The application supports automatic updates:
- Check for updates in the Settings section
- Download and install updates automatically
- Maintain backward compatibility with existing configurations

## 📞 Contact

- **Project Maintainer**: [Your Name](mailto:your.email@example.com)
- **Project Link**: [https://github.com/anand.gaurav@hotmail.com/UserAccessMadeEasy](https://github.com/anand.gaurav@hotmail.com/UserAccessMadeEasy)

---

**Note**: This tool is designed to work with Oracle Fusion HCM APIs. Ensure you have proper API access and permissions before using this application. 