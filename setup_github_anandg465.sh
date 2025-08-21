#!/bin/bash

# Personalized GitHub Repository Setup Script
# Oracle Fusion Resource Fetcher - for anandg465

echo "🚀 Setting up GitHub repository for Oracle Fusion Resource Fetcher"
echo "================================================================"
echo "GitHub Account: anandg465"
echo "Email: anand.gaurav@hotmail.com"
echo ""

# Verify Git configuration
echo "📋 Verifying Git configuration..."
echo "   Name: $(git config --global user.name)"
echo "   Email: $(git config --global user.email)"
echo ""

echo "✅ Git is properly configured!"
echo ""

echo "📝 Next Steps:"
echo "=============="
echo ""
echo "1. Create GitHub repository:"
echo "   - Go to https://github.com/new"
echo "   - Repository name: oracle-fusion-resource-fetcher"
echo "   - Description: Oracle Fusion Resource Fetcher - HTTP server for fetching and updating Oracle Fusion resources"
echo "   - Choose Public or Private"
echo "   - Don't initialize with README (we already have one)"
echo "   - Click 'Create repository'"
echo ""
echo "2. After creating the repository, run these commands:"
echo "   git remote add origin https://github.com/anandg465/oracle-fusion-resource-fetcher.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Repository URL will be:"
echo "   https://github.com/anandg465/oracle-fusion-resource-fetcher"
echo ""
echo "4. For team members to access:"
echo "   git clone https://github.com/anandg465/oracle-fusion-resource-fetcher.git"
echo "   cd oracle-fusion-resource-fetcher"
echo "   pip install -r requirements.txt"
echo ""
echo "📚 For detailed instructions, see GIT_SETUP_GUIDE.md"
echo ""
echo "🎯 Ready to connect to GitHub!" 