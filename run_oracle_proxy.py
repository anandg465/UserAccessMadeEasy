#!/usr/bin/env python3
"""
Oracle Fusion Proxy Server Runner
Simple script to start the proxy server with proper setup
"""

import subprocess
import sys
import os
import socket
import time

def find_available_port(start_port=5001, max_attempts=10):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False
    return True

def start_server():
    """Start the Flask proxy server"""
    print("🚀 Starting Oracle Fusion Proxy Server...")
    
    # Find available port
    port = find_available_port(5001, 10)
    if not port:
        print("❌ Error: No available ports found between 5001-5010")
        return False
    
    print(f"📱 Server will be available at: http://localhost:{port}")
    print("🔧 This server bypasses CORS restrictions by making server-side requests")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 60)
    
    try:
        # Set environment variable for the port
        env = os.environ.copy()
        env['FLASK_PORT'] = str(port)
        
        subprocess.run([sys.executable, "oracle_fusion_proxy_server.py"], env=env)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False
    
    return True

def main():
    """Main function"""
    print("🔧 Oracle Fusion Resource Fetcher - Server Proxy Setup")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists("oracle_fusion_proxy_server.py"):
        print("❌ Error: oracle_fusion_proxy_server.py not found!")
        print("Please run this script from the directory containing the proxy server files.")
        return
    
    # Install requirements
    if not install_requirements():
        return
    
    # Start server
    start_server()

if __name__ == "__main__":
    main() 