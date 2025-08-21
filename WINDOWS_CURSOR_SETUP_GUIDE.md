# 🚀 Windows + Cursor Setup Guide
## Oracle Fusion Resource Fetcher

## 🎯 **Complete Setup Process**

### **Option 1: Using Complete Project Package** (Recommended)

#### **Step 1: Transfer Project to Windows**
1. **Copy** `OracleFusion_Complete_Project.zip` to Windows machine
2. **Extract** to your desired location:
   ```
   C:\Projects\user-access-backend\
   ```

#### **Step 2: Install Cursor on Windows**
1. **Download Cursor** from [cursor.sh](https://cursor.sh/)
2. **Run installer** and follow setup wizard
3. **Launch Cursor** after installation

#### **Step 3: Open Project in Cursor**
1. **In Cursor**: File → Open Folder
2. **Navigate** to: `C:\Projects\user-access-backend\`
3. **Select** the folder and click "Select Folder"
4. **Wait** for Cursor to load the project

---

### **Option 2: Using Git Repository** (For Version Control)

#### **Step 1: Clone Repository on Windows**
```cmd
# Open Command Prompt or PowerShell
cd C:\Projects
git clone <your-repository-url> user-access-backend
cd user-access-backend
```

#### **Step 2: Install Cursor and Open Project**
1. **Install Cursor** from [cursor.sh](https://cursor.sh/)
2. **Open Cursor** and go to File → Open Folder
3. **Select** `C:\Projects\user-access-backend\`

---

## 🐍 **Python Setup on Windows**

### **Step 1: Install Python**
1. **Download Python** from [python.org](https://www.python.org/downloads/)
2. **Choose Python 3.8+** (recommended: Python 3.11 or 3.12)
3. **During installation**:
   - ✅ **Check "Add Python to PATH"**
   - ✅ **Check "Install pip"**
   - ✅ **Check "Install for all users"** (if admin)

### **Step 2: Verify Python Installation**
Open Command Prompt and run:
```cmd
python --version
pip --version
```

### **Step 3: Install Project Dependencies**
```cmd
cd C:\Projects\user-access-backend
pip install -r requirements.txt
```

---

## 🔧 **Cursor Configuration**

### **Step 1: Install Python Extension**
1. **In Cursor**: Extensions → Search "Python"
2. **Install** "Python" extension by Microsoft
3. **Reload** Cursor if prompted

### **Step 2: Select Python Interpreter**
1. **In Cursor**: Ctrl+Shift+P
2. **Type**: "Python: Select Interpreter"
3. **Choose** your Python installation

### **Step 3: Configure Terminal**
1. **In Cursor**: Terminal → New Terminal
2. **Verify** Python is available:
   ```cmd
   python --version
   ```

---

## 📁 **Project Structure in Cursor**

After opening the project, you should see:

```
user-access-backend/
├── app/                           # FastAPI application
│   ├── __init__.py
│   ├── api.py
│   ├── config.py
│   ├── crud.py
│   ├── database.py
│   ├── deps.py
│   ├── main.py
│   ├── models.py
│   ├── oracle_client.py
│   └── schemas.py
├── simple_oracle_fetcher.py       # Main application
├── build_windows_package.py       # Windows build script
├── build_and_package.py           # Complete build script
├── requirements.txt               # Dependencies
├── README.md                      # Project documentation
├── BUILD_INSTRUCTIONS.md          # Build instructions
├── PROJECT_TRANSFER_GUIDE.md      # Transfer guide
├── WINDOWS_COMPATIBILITY_GUIDE.md # Windows guide
└── [Other build and documentation files]
```

---

## 🚀 **Running the Project**

### **Method 1: Run Simple Server**
```cmd
# In Cursor terminal
python simple_oracle_fetcher.py
```

### **Method 2: Run FastAPI Application**
```cmd
# In Cursor terminal
cd app
python main.py
```

### **Method 3: Run with uvicorn**
```cmd
# In Cursor terminal
pip install uvicorn
uvicorn app.main:app --reload
```

---

## 🔨 **Building Windows Executable**

### **Step 1: Run Build Script**
```cmd
# In Cursor terminal
python build_windows_package.py
```

### **Step 2: Check Output**
```cmd
# After build completes
dir
# Should see OracleFusionResourceFetcher_Windows_Package.zip
```

---

## ⚙️ **Cursor Features for Development**

### **Code Intelligence**
- **Auto-completion**: Python functions and variables
- **Error detection**: Real-time syntax checking
- **Refactoring**: Rename variables, extract functions
- **Go to definition**: Ctrl+Click on functions

### **Debugging**
1. **Set breakpoints**: Click left margin in code
2. **Start debugging**: F5 or Debug → Start Debugging
3. **Step through code**: F10 (step over), F11 (step into)

### **Terminal Integration**
- **Integrated terminal**: Ctrl+` (backtick)
- **Multiple terminals**: Split terminal view
- **Python environment**: Automatic activation

### **Git Integration**
- **Source control**: View changes in sidebar
- **Commit changes**: Ctrl+Shift+G
- **Push/Pull**: Sync with remote repository

---

## 🎯 **Development Workflow**

### **1. Make Changes**
- **Edit files** in Cursor
- **Save changes**: Ctrl+S
- **See real-time errors** and warnings

### **2. Test Changes**
```cmd
# Run the application
python simple_oracle_fetcher.py

# Or run tests (if available)
python -m pytest
```

### **3. Build Package**
```cmd
# Build Windows executable
python build_windows_package.py

# Or build complete package
python build_and_package.py
```

### **4. Commit Changes**
```cmd
# In Cursor terminal
git add .
git commit -m "Description of changes"
git push
```

---

## 🔧 **Troubleshooting**

### **Issue 1: Python Not Found**
**Solution**: Install Python and add to PATH
```cmd
# Verify Python installation
python --version
# If not found, reinstall Python with "Add to PATH" checked
```

### **Issue 2: Dependencies Missing**
**Solution**: Install requirements
```cmd
pip install -r requirements.txt
```

### **Issue 3: Cursor Not Recognizing Python**
**Solution**: Select Python interpreter
1. **Ctrl+Shift+P** → "Python: Select Interpreter"
2. **Choose** your Python installation

### **Issue 4: Terminal Issues**
**Solution**: Configure terminal
1. **Terminal** → New Terminal
2. **Verify** Python is available in terminal

### **Issue 5: Build Script Fails**
**Solution**: Check prerequisites
```cmd
# Install PyInstaller
pip install pyinstaller

# Install requests
pip install requests

# Run build script
python build_windows_package.py
```

---

## 📋 **Quick Start Checklist**

### **Before Starting**
- ✅ **Python installed** (3.8+)
- ✅ **Cursor installed**
- ✅ **Project files transferred**
- ✅ **Dependencies installed**

### **In Cursor**
- ✅ **Project opened**
- ✅ **Python extension installed**
- ✅ **Interpreter selected**
- ✅ **Terminal working**

### **Testing**
- ✅ **Application runs**
- ✅ **Build script works**
- ✅ **Git integration working**

---

## 🎉 **Success Indicators**

### **Cursor Setup**
- **Project loads** without errors
- **Python extension** is active
- **Terminal** shows Python version
- **IntelliSense** works for Python code

### **Application**
- **Server starts** without errors
- **Browser opens** to application
- **API endpoints** respond correctly

### **Build Process**
- **Build script** completes successfully
- **Executable** is created
- **Package** is generated

---

## 🔗 **Useful Cursor Shortcuts**

| Action | Shortcut |
|--------|----------|
| Open Command Palette | Ctrl+Shift+P |
| Open Terminal | Ctrl+` |
| Save File | Ctrl+S |
| Find in Files | Ctrl+Shift+F |
| Go to Line | Ctrl+G |
| Toggle Sidebar | Ctrl+B |
| Split Editor | Ctrl+\ |
| Close Tab | Ctrl+W |

---

## 📞 **Support Resources**

### **Cursor Documentation**
- **Official Docs**: [cursor.sh/docs](https://cursor.sh/docs)
- **Keyboard Shortcuts**: Help → Keyboard Shortcuts Reference
- **Extensions**: Extensions marketplace

### **Python Resources**
- **Python Docs**: [python.org/docs](https://docs.python.org/)
- **pip Docs**: [pip.pypa.io](https://pip.pypa.io/)

### **Project Documentation**
- **README.md**: Project overview
- **BUILD_INSTRUCTIONS.md**: Build process
- **PROJECT_TRANSFER_GUIDE.md**: Transfer methods

---

**🎯 Ready to Develop!** Your project is now set up on Windows with Cursor and ready for development. 