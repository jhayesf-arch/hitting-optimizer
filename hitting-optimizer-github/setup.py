#!/usr/bin/env python3
"""
Setup script for Enhanced Hitting Optimizer Web Interface
Installs dependencies and initializes directories
"""

import os
import subprocess
import sys

def main():
    print("╔" + "═" * 60 + "╗")
    print("║" + " " * 15 + "ENHANCED HITTING OPTIMIZER SETUP" + " " * 13 + "║")
    print("╚" + "═" * 60 + "╝")
    
    # Check Python version
    print("\n✓ Checking Python version...")
    if sys.version_info < (3, 8):
        print("✗ Python 3.8+ required. You have:", sys.version_info.major, ".", sys.version_info.minor)
        return False
    print(f"  Using Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Install requirements
    print("\n✓ Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"])
        print("  ✓ All dependencies installed")
    except Exception as e:
        print(f"  ✗ Error installing dependencies: {e}")
        return False
    
    # Create directories
    print("\n✓ Creating directories...")
    dirs = [
        os.path.expanduser("~/hitting_optimizer_uploads"),
        os.path.expanduser("~/hitting_optimizer_results"),
        os.path.expanduser("~/hitting_optimizer_downloads_cache")
    ]
    
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        print(f"  ✓ {d}")
    
    # Verify files
    print("\n✓ Verifying project files...")
    files = [
        "app.py",
        "hitting_optimizer_enhanced.py",
        "requirements.txt",
        "templates/index.html",
        "README.md"
    ]
    
    for f in files:
        if os.path.exists(f):
            print(f"  ✓ {f}")
        else:
            print(f"  ✗ {f} - MISSING")
            return False
    
    print("\n" + "=" * 64)
    print("✅ SETUP COMPLETE!")
    print("=" * 64)
    print("\nTo start the web interface:")
    print("  1. Run: python app.py")
    print("  2. Open: http://localhost:5000")
    print("\nFor command-line analysis:")
    print("  1. Run: python hitting_optimizer_enhanced.py")
    print("\nFor more info:")
    print("  - Read README.md")
    print("\n" + "=" * 64)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
