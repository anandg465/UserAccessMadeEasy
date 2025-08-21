#!/bin/bash

# GitHub Repository Setup Script
# Oracle Fusion Resource Fetcher

echo "🚀 Setting up GitHub repository for Oracle Fusion Resource Fetcher"
echo "================================================================"

# Check if git is configured
echo "📋 Checking Git configuration..."
if [ -z "$(git config --global user.name)" ] || [ -z "$(git config --global user.email)" ]; then
    echo "⚠️  Git identity not configured. Please set your name and email:"
    echo ""
    read -p "Enter your name: " git_name
    read -p "Enter your email: " git_email
    
    git config --global user.name "$git_name"
    git config --global user.email "$git_email"
    echo "✅ Git identity configured"
else
    echo "✅ Git identity already configured:"
    echo "   Name: $(git config --global user.name)"
    echo "   Email: $(git config --global user.email)"
fi

echo ""
echo "📝 Next Steps:"
echo "=============="
echo ""
echo "1. Create a GitHub repository:"
echo "   - Go to https://github.com/new"
echo "   - Repository name: oracle-fusion-resource-fetcher"
echo "   - Description: Oracle Fusion Resource Fetcher - HTTP server for fetching and updating Oracle Fusion resources"
echo "   - Choose Public or Private"
echo "   - Don't initialize with README (we already have one)"
echo "   - Click 'Create repository'"
echo ""
echo "2. After creating the repository, run these commands:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/oracle-fusion-resource-fetcher.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Invite team members:"
echo "   - Go to repository Settings → Collaborators"
echo "   - Add team members with appropriate permissions"
echo ""
echo "4. For team members to access:"
echo "   git clone https://github.com/YOUR_USERNAME/oracle-fusion-resource-fetcher.git"
echo "   cd oracle-fusion-resource-fetcher"
echo "   pip install -r requirements.txt"
echo ""
echo "📚 For detailed instructions, see GIT_SETUP_GUIDE.md"
echo ""
echo "🎯 Ready to connect to GitHub!" 