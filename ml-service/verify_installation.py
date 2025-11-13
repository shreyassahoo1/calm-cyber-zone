"""
Verify that all required packages are installed correctly
"""

import sys

def check_package(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        return True, None
    except ImportError as e:
        return False, str(e)

def main():
    """Check all required packages"""
    print("="*60)
    print("🔍 Verifying ML Service Installation")
    print("="*60)
    
    # Required packages
    packages = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("pydantic", "pydantic"),
        ("torch", "torch"),
        ("transformers", "transformers"),
        ("numpy", "numpy"),
        ("langdetect", "langdetect"),
        ("datasets", "datasets"),
        ("scikit-learn", "sklearn"),
        ("pandas", "pandas"),
        ("requests", "requests"),
    ]
    
    all_installed = True
    missing_packages = []
    
    for package_name, import_name in packages:
        is_installed, error = check_package(package_name, import_name)
        if is_installed:
            # Try to get version
            try:
                module = __import__(import_name)
                version = getattr(module, "__version__", "unknown")
                print(f"✅ {package_name:<20} (version: {version})")
            except:
                print(f"✅ {package_name:<20}")
        else:
            print(f"❌ {package_name:<20} - MISSING")
            print(f"   Error: {error}")
            missing_packages.append(package_name)
            all_installed = False
    
    print("="*60)
    
    if all_installed:
        print("✅ All packages are installed correctly!")
        print("\n📝 You can now run the ML service:")
        print("   python main.py")
        return 0
    else:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("\n📝 To install missing packages:")
        print("   pip install " + " ".join(missing_packages))
        print("\n   Or install all requirements:")
        print("   pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())

