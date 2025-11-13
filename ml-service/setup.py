"""
Setup script for SafeGuard ML Service
Installs all required dependencies and verifies installation
"""

import subprocess
import sys
import os
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"📦 {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is 3.9 or higher"""
    print("\n" + "="*60)
    print("🔍 Checking Python version...")
    print("="*60)
    
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is installed")
        return True
    else:
        print(f"❌ Python 3.9+ is required. You have Python {version.major}.{version.minor}.{version.micro}")
        return False

def create_virtual_environment():
    """Create virtual environment"""
    if os.path.exists("venv"):
        print("\n✅ Virtual environment already exists")
        return True
    
    print("\n📦 Creating virtual environment...")
    if platform.system() == "Windows":
        command = f"{sys.executable} -m venv venv"
    else:
        command = f"{sys.executable} -m venv venv"
    
    return run_command(command, "Creating virtual environment")

def get_pip_command():
    """Get the correct pip command based on OS"""
    if platform.system() == "Windows":
        return "venv\\Scripts\\pip"
    else:
        return "venv/bin/pip"

def get_python_command():
    """Get the correct python command based on OS"""
    if platform.system() == "Windows":
        return "venv\\Scripts\\python"
    else:
        return "venv/bin/python"

def upgrade_pip():
    """Upgrade pip to latest version"""
    pip_cmd = get_pip_command()
    return run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip")

def install_requirements():
    """Install requirements from requirements.txt"""
    pip_cmd = get_pip_command()
    
    print("\n" + "="*60)
    print("📦 Installing dependencies...")
    print("="*60)
    print("⚠️  This may take 10-15 minutes (downloading large models)...")
    print("⚠️  Please be patient, especially for PyTorch and Transformers")
    print("="*60)
    
    # Install requirements in steps to handle errors better
    steps = [
        ("Basic dependencies", "fastapi uvicorn pydantic python-multipart requests"),
        ("Scientific libraries", "numpy pandas scikit-learn"),
        ("ML libraries", "torch transformers"),
        ("Language detection", "langdetect"),
        ("Datasets", "datasets"),
    ]
    
    all_success = True
    for step_name, packages in steps:
        print(f"\n📦 Installing {step_name}...")
        success = run_command(
            f"{pip_cmd} install {packages}",
            f"Installing {step_name}"
        )
        if not success:
            print(f"⚠️  Warning: {step_name} installation had issues")
            # Continue anyway, might work
    
    # Try installing from requirements.txt as well
    print("\n📦 Installing from requirements.txt...")
    if os.path.exists("requirements.txt"):
        success = run_command(
            f"{pip_cmd} install -r requirements.txt",
            "Installing from requirements.txt"
        )
        if not success:
            all_success = False
    
    return all_success

def verify_installation():
    """Verify that all required packages are installed"""
    print("\n" + "="*60)
    print("✅ Verifying installation...")
    print("="*60)
    
    python_cmd = get_python_command()
    verification_script = """
import sys
required_packages = [
    'fastapi',
    'uvicorn',
    'pydantic',
    'torch',
    'transformers',
    'numpy',
    'langdetect',
    'datasets',
    'sklearn',
    'pandas',
    'requests',
]

missing_packages = []
for package in required_packages:
    try:
        if package == 'sklearn':
            __import__('sklearn')
        else:
            __import__(package)
        print(f"✅ {package}")
    except ImportError:
        print(f"❌ {package} - MISSING")
        missing_packages.append(package)

if missing_packages:
    print(f"\\n❌ Missing packages: {', '.join(missing_packages)}")
    sys.exit(1)
else:
    print("\\n✅ All packages installed successfully!")
"""
    
    try:
        result = subprocess.run(
            [python_cmd, "-c", verification_script],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(e.stdout)
        print(e.stderr)
        return False

def main():
    """Main setup function"""
    print("="*60)
    print("🚀 SafeGuard ML Service - Setup")
    print("="*60)
    
    # Check Python version
    if not check_python_version():
        print("\n❌ Please install Python 3.9 or higher")
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        print("\n❌ Failed to create virtual environment")
        sys.exit(1)
    
    # Upgrade pip
    if not upgrade_pip():
        print("\n⚠️  Warning: Failed to upgrade pip, but continuing...")
    
    # Install requirements
    if not install_requirements():
        print("\n⚠️  Warning: Some packages may not have installed correctly")
        print("⚠️  Trying to continue anyway...")
    
    # Verify installation
    if not verify_installation():
        print("\n❌ Installation verification failed")
        print("⚠️  Please check the errors above and try again")
        sys.exit(1)
    
    print("\n" + "="*60)
    print("✅ Setup completed successfully!")
    print("="*60)
    print("\n📝 Next steps:")
    print("1. Activate virtual environment:")
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("2. Run the ML service:")
    print("   python main.py")
    print("\n" + "="*60)

if __name__ == "__main__":
    main()

