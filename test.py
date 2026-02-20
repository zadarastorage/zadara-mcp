#!/usr/bin/env python3
"""
Test script for Zadara Storage MCP Server
"""

import os
import sys

def check_environment():
    """Check if environment variables are set"""
    required_vars = {
        'VPSA': ['ZADARA_VPSA_URL', 'ZADARA_VPSA_API_KEY'],
        'Object Storage': ['ZADARA_OBJECT_STORAGE_URL', 'ZADARA_OBJECT_ACCESS_KEY', 'ZADARA_OBJECT_SECRET_KEY']
    }
    
    print("Checking environment configuration...\n")
    
    all_set = True
    for service, vars in required_vars.items():
        print(f"{service}:")
        for var in vars:
            value = os.getenv(var)
            if value:
                # Mask sensitive values
                if 'KEY' in var or 'SECRET' in var:
                    masked = value[:4] + '*' * (len(value) - 8) + value[-4:] if len(value) > 8 else '***'
                    print(f"  ✓ {var}: {masked}")
                else:
                    print(f"  ✓ {var}: {value}")
            else:
                print(f"  ✗ {var}: Not set")
                all_set = False
        print()
    
    return all_set

def check_dependencies():
    """Check if required packages are installed"""
    print("Checking dependencies...\n")
    
    required_packages = ['mcp', 'httpx']
    all_installed = True
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {package}: Installed")
        except ImportError:
            print(f"  ✗ {package}: Not installed")
            all_installed = False
    
    print()
    return all_installed

def test_server_import():
    """Test if server can be imported"""
    print("Testing server import...\n")
    
    try:
        # Add current directory to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import server
        print("  ✓ Server module imported successfully")
        print()
        return True
    except Exception as e:
        print(f"  ✗ Failed to import server: {e}")
        print()
        return False

def main():
    print("=" * 50)
    print("Zadara Storage MCP Server - Test Suite")
    print("=" * 50)
    print()
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    # Check environment
    env_ok = check_environment()
    
    # Test server import
    import_ok = test_server_import()
    
    # Summary
    print("=" * 50)
    print("Test Summary")
    print("=" * 50)
    print()
    print(f"Dependencies: {'✓ OK' if deps_ok else '✗ FAILED'}")
    print(f"Environment:  {'✓ OK' if env_ok else '✗ INCOMPLETE'}")
    print(f"Server:       {'✓ OK' if import_ok else '✗ FAILED'}")
    print()
    
    if deps_ok and import_ok:
        if env_ok:
            print("✓ All tests passed! Server is ready to use.")
            print("  Run: python server.py")
        else:
            print("⚠ Server can run, but environment is not fully configured.")
            print("  Some features may not work without proper credentials.")
            print("  Edit .env file or set environment variables.")
    else:
        print("✗ Tests failed. Please fix the issues above.")
        if not deps_ok:
            print("  Run: pip install -r requirements.txt")
    
    print()
    return 0 if (deps_ok and import_ok) else 1

if __name__ == "__main__":
    sys.exit(main())
