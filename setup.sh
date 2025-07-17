#!/bin/bash

# Quick setup script for Telegram Bot GitHub deployment

echo "🤖 Telegram Bot GitHub Deployment Setup"
echo "======================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ and try again."
    exit 2
fi

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git and try again."
    exit 1
fi

# Create directory structure
mkdir -p .github/workflows

# Install required dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Make deploy script executable
chmod +x deploy.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Get your GitHub Personal Access Token from:"
echo "   https://github.com/settings/tokens"
echo "   (Make sure to select 'repo' and 'workflow' scopes)"
echo ""
echo "2. Run the deployment script:"
echo "   python deploy.py"
echo ""
echo "3. Follow the prompts to enter your:"
echo "   - GitHub Personal Access Token"
echo "   - GitHub username"
echo "   - Repository name"
echo "   - Telegram Bot Token"
echo ""
echo "The script will automatically:"
echo "- Create GitHub repository"
echo "- Setup GitHub Actions workflow"
echo "- Push your code"
echo "- Start your bot running 24/7!"