#!/usr/bin/env python3
"""
Simple Oracle Fusion Server Runner
Alternative approach using Python's built-in HTTP server
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        print("✅ Packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False
    return True

def start_server():
    """Start the simple HTTP server"""
    print("🚀 Starting Simple Oracle Fusion Server...")
    print("📱 This uses Python's built-in HTTP server (no Flask required)")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 60)
    
    try:
        subprocess.run([sys.executable, "simple_oracle_fetcher.py"])
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    """Main function"""
    print("🔧 Oracle Fusion Resource Fetcher - Simple HTTP Server")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("simple_oracle_fetcher.py"):
        print("❌ Error: simple_oracle_fetcher.py not found!")
        print("Please run this script from the directory containing the server files.")
        return
    
    # Install requirements
    if not install_requirements():
        return
    
    # Start server
    start_server()

if __name__ == "__main__":
    main() 