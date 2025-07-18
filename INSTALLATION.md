# File: INSTALLATION.md
# Path: /home/herb/Desktop/Finder/INSTALLATION.md
# Standard: AIDEV-PascalCase-2.1
# Created: 2025-07-18
# Last Modified: 2025-07-18  13:54PM

# Finder Application - Installation Guide

## System Requirements

### Minimum Requirements
- **Operating System**: Linux, macOS, or Windows
- **Python**: Version 3.7 or higher
- **Memory**: 512 MB RAM
- **Storage**: 50 MB free space
- **Display**: 1024x768 resolution

### Recommended Requirements
- **Python**: Version 3.9 or higher
- **Memory**: 2 GB RAM
- **Storage**: 100 MB free space
- **Display**: 1280x720 or higher

## Dependencies

### Required Python Packages
- **PySide6**: GUI framework
- **pathlib**: File path handling (built-in Python 3.4+)
- **re**: Regular expressions (built-in)
- **os**: Operating system interface (built-in)
- **sys**: System-specific parameters (built-in)
- **datetime**: Date and time handling (built-in)
- **tempfile**: Temporary file handling (built-in)
- **unittest**: Testing framework (built-in)

### Installing Dependencies

#### Option 1: Using pip (Recommended)
```bash
pip install PySide6
```

#### Option 2: Using conda
```bash
conda install -c conda-forge pyside6
```

#### Option 3: Using system package manager

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3-pyside6.qtwidgets python3-pyside6.qtcore python3-pyside6.qtgui
```

**CentOS/RHEL/Fedora:**
```bash
sudo dnf install python3-pyside6
```

**macOS (using Homebrew):**
```bash
brew install python3
pip3 install PySide6
```

## Installation Methods

### Method 1: Direct Download (Recommended)
1. **Download the application files** to your desired directory
2. **Ensure all files are present**:
   ```
   Finder/
   ├── Finder.py                    # Main application
   ├── test_suite_generator.py      # Educational test suite
   ├── USER_GUIDE.md               # User documentation
   ├── QUICK_START.md              # Quick start guide
   ├── INSTALLATION.md             # This file
   ├── CLAUDE.md                   # Project documentation
   └── test_*.py                   # Test files (optional)
   ```

3. **Install dependencies**:
   ```bash
   pip install PySide6
   ```

4. **Test installation**:
   ```bash
   cd /path/to/Finder
   python Finder.py
   ```

### Method 2: Git Clone
```bash
# Clone the repository (if available)
git clone <repository-url> Finder
cd Finder

# Install dependencies
pip install PySide6

# Run the application
python Finder.py
```

### Method 3: Virtual Environment (Recommended for Development)
```bash
# Create virtual environment
python3 -m venv finder_env

# Activate virtual environment
# Linux/macOS:
source finder_env/bin/activate
# Windows:
finder_env\Scripts\activate

# Install dependencies
pip install PySide6

# Copy application files to directory
# Run application
python Finder.py
```

## Verification

### Test Basic Functionality
```bash
# Navigate to Finder directory
cd /path/to/Finder

# Test main application
python Finder.py

# Test educational suite (in separate terminal)
python test_suite_generator.py

# Run unit tests (optional)
python test_finder_working.py
```

### Expected Output
- **Main Application**: GUI window should open with search interface
- **Test Suite**: Colored terminal output with 5 example scenarios
- **Unit Tests**: Test results with success/failure statistics

## Platform-Specific Setup

### Linux Setup
```bash
# Install Python and pip
sudo apt update
sudo apt install python3 python3-pip

# Install PySide6
pip3 install PySide6

# Make scripts executable (optional)
chmod +x Finder.py
chmod +x test_suite_generator.py

# Create desktop shortcut (optional)
cat > ~/Desktop/Finder.desktop << EOF
[Desktop Entry]
Type=Application
Name=Finder
Exec=python3 /path/to/Finder/Finder.py
Path=/path/to/Finder
Icon=applications-accessories
Categories=Utility;
EOF
```

### macOS Setup
```bash
# Install Python (if not already installed)
# Download from python.org or use Homebrew
brew install python3

# Install PySide6
pip3 install PySide6

# Create application alias (optional)
echo "alias finder='cd /path/to/Finder && python3 Finder.py'" >> ~/.bash_profile
source ~/.bash_profile
```

### Windows Setup
```cmd
# Install Python from python.org
# Ensure "Add Python to PATH" is checked during installation

# Install PySide6
pip install PySide6

# Create batch file for easy launching
echo @echo off > Finder.bat
echo cd /d "C:\path\to\Finder" >> Finder.bat
echo python Finder.py >> Finder.bat

# Create desktop shortcut to Finder.bat
```

## Configuration

### Default Settings
The application starts with these default settings:
- **Search Path**: Current directory
- **File Types**: .txt and .md selected
- **Search Mode**: Line-by-line
- **Case Sensitivity**: Off (case-insensitive)
- **Unique Mode**: Off

### Customizing Defaults
Edit the `_setup_defaults()` method in `Finder.py`:
```python
def _setup_defaults(self):
    """Setup default values"""
    self.rb_line.setChecked(True)  # Default to line mode
    
    # Customize default file types
    self.file_type_checkboxes['txt'].setChecked(True)
    self.file_type_checkboxes['md'].setChecked(True)
    self.file_type_checkboxes['py'].setChecked(True)  # Add Python files
    
    self.cb_unique.setChecked(False)  # Unique mode off
    self._use_current_folder()  # Use current directory
```

## Troubleshooting Installation

### Common Issues

#### "PySide6 not found"
```bash
# Ensure PySide6 is installed
pip show PySide6

# If not found, install it
pip install PySide6

# For permission issues, try
pip install --user PySide6
```

#### "Python not found"
```bash
# Check Python installation
python --version
python3 --version

# Add Python to PATH (Windows)
# Add to system environment variables:
# C:\Python39\
# C:\Python39\Scripts\
```

#### "Qt platform plugin error"
```bash
# Linux: Install Qt platform libraries
sudo apt install qt6-base-dev

# Set environment variable if needed
export QT_QPA_PLATFORM=xcb
```

#### "Permission denied"
```bash
# Make files executable (Linux/macOS)
chmod +x Finder.py

# Or run with python explicitly
python3 Finder.py
```

### Dependency Issues

#### Missing Qt Libraries (Linux)
```bash
# Ubuntu/Debian
sudo apt install libqt6core6 libqt6gui6 libqt6widgets6

# CentOS/Fedora
sudo dnf install qt6-qtbase qt6-qtbase-gui
```

#### Python Version Issues
```bash
# Check Python version
python --version

# If too old, install newer version
# Ubuntu
sudo apt install python3.9

# Use specific Python version
python3.9 Finder.py
```

## Performance Optimization

### For Large Projects
1. **Limit Search Scope**:
   - Search specific directories instead of entire drives
   - Select only necessary file types
   - Use more specific search terms

2. **System Resources**:
   - Close other applications to free memory
   - Use SSD storage for better I/O performance
   - Increase virtual memory if needed

3. **Search Optimization**:
   - Start with simple formulas
   - Use Unique mode for large result sets
   - Test formulas on small directories first

## Uninstallation

### Remove Application
```bash
# Simply delete the Finder directory
rm -rf /path/to/Finder

# Remove Python dependencies (if not needed elsewhere)
pip uninstall PySide6

# Remove desktop shortcuts (if created)
rm ~/Desktop/Finder.desktop
```

### Clean Virtual Environment
```bash
# If using virtual environment
deactivate
rm -rf finder_env
```

## Getting Help

### Support Resources
- **User Guide**: `USER_GUIDE.md` - Comprehensive usage instructions
- **Quick Start**: `QUICK_START.md` - 5-minute tutorial
- **Test Suite**: Click "🎓 Run Examples" button (bottom of controls)
- **Error Messages**: Application provides detailed error descriptions

### Reporting Issues
When reporting issues, include:
- Operating system and version
- Python version (`python --version`)
- PySide6 version (`pip show PySide6`)
- Error messages (full text)
- Steps to reproduce the issue

### Community
- Use the Educational Test Suite to learn formula patterns
- Share useful search formulas with other users
- Contribute improvements to documentation

---

## Quick Installation Summary

```bash
# 1. Install Python 3.7+ (if not already installed)
# 2. Install PySide6
pip install PySide6

# 3. Download/copy Finder application files
# 4. Run the application
cd /path/to/Finder
python Finder.py

# 5. Try the educational examples
# Click "🎓 Run Examples" button in the application
```

You're now ready to use the Finder application! See `QUICK_START.md` for a 5-minute tutorial.