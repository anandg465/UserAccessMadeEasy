# 🚀 Quick Start Guide - Oracle Fusion HCM User Management Tool

## ⚡ Get Started in 5 Minutes

### Prerequisites
- Python 3.8 or higher
- Git
- Oracle Fusion HCM API access

### Step 1: Clone the Repository
```bash
git clone https://github.com/anandg465/UserAccessMadeEasy.git
cd UserAccessMadeEasy
```

### Step 2: Set Up Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Start the Application
```bash
# Start the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 4: Access the Application
1. **API Documentation**: Open http://localhost:8000/docs in your browser
2. **Web Interface**: Open `frontend/index.html` in your browser
3. **Backend API**: http://localhost:8000

## 🎯 Key Features

### User Management
- ✅ Get comprehensive user details (username, person number, roles)
- ✅ View assigned roles and data security contexts
- ✅ Search users with advanced filters

### Role Management
- ✅ Assign roles to users
- ✅ Remove roles from users
- ✅ Bulk role assignment via Excel upload

### Areas of Responsibility (AOR)
- ✅ Assign AORs to users
- ✅ Remove AORs from users
- ✅ Bulk AOR assignment

### Data Security
- ✅ Assign data security contexts
- ✅ Bulk data security assignment
- ✅ View current data security settings

### Bulk Operations
- ✅ Excel file upload for bulk operations
- ✅ Template downloads for different operations
- ✅ Progress tracking and error reporting

## 🔧 Configuration

### Oracle Fusion Connection
1. Open the web interface
2. Enter your Oracle Fusion instance URL
3. Provide your API username and password
4. Click "Test Connection" to verify
5. Click "Connect" to establish connection

### Application Settings
- **Theme**: Choose between Default, Dark, and Light themes
- **Auto Refresh**: Set automatic refresh interval
- **Client Branding**: Customize colors, company name, and logo

## 📋 Usage Examples

### Get User Details
1. Navigate to "User Details" section
2. Enter username (e.g., "john.doe")
3. Click "Get Details"
4. View comprehensive user information

### Assign Role to User
1. Go to "Role Management" → "Assign Role"
2. Enter username and role name
3. Click "Assign Role"
4. Verify the assignment

### Bulk Role Assignment
1. Download the role assignment template
2. Fill in the Excel file with usernames and roles
3. Upload the file in "Bulk Upload" section
4. Select "Role Assignment" operation type
5. Process the bulk operation

## 🛠️ Development

### Running Tests
```bash
# Run all tests
PYTHONPATH=. pytest tests/ -v

# Run with coverage
PYTHONPATH=. pytest tests/ -v --cov=app --cov-report=html
```

### Code Quality
```bash
# Format code
black app/

# Run linting
flake8 app/

# Security scan
bandit -r app/
```

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/your-feature

# Make changes and test
# ...

# Commit and push
git add .
git commit -m "Add your feature"
git push origin feature/your-feature

# Create Pull Request on GitHub
```

## 🔍 Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>
```

#### Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Oracle Connection Issues
- Verify your Oracle Fusion API credentials
- Check network connectivity
- Ensure you have proper API permissions

### Getting Help
- **Documentation**: Check [README.md](README.md) for detailed information
- **Issues**: Report bugs via [GitHub Issues](https://github.com/anandg465/UserAccessMadeEasy/issues)
- **Discussions**: Join [GitHub Discussions](https://github.com/anandg465/UserAccessMadeEasy/discussions)

## 📞 Support

- **Repository**: https://github.com/anandg465/UserAccessMadeEasy
- **Maintainer**: anandg465
- **Email**: anand.gaurav@hotmail.com

---

**Happy Coding! 🎉**
