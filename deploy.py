#!/usr/bin/env python3
"""
Automated GitHub Deployment Script for Telegram Bot
This script will:
1. Initialize a git repository
2. Create/update GitHub repository
3. Push all files to GitHub
4. Set up GitHub secrets for bot token
5. Trigger the workflow
"""

import os
import subprocess
import sys
import json
import requests
from getpass import getpass
import time

class GitHubDeployer:
    def __init__(self):
        self.token = None
        self.username = None
        self.repo_name = None
        self.bot_token = None
        
    def get_credentials(self):
        """Get GitHub credentials from user"""
        print("🚀 GitHub Bot Deployment Setup")
        print("=" * 40)
        
        self.token = getpass("Enter your GitHub Personal Access Token: ")
        self.username = input("Enter your GitHub username: ")
        self.repo_name = input("Enter repository name (e.g., telegram-bot): ")
        self.bot_token = getpass("Enter your Telegram Bot Token: ")
        
        if not all([self.token, self.username, self.repo_name, self.bot_token]):
            print("❌ All fields are required!")
            sys.exit(1)
    
    def run_command(self, command, capture_output=True):
        """Run shell command"""
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=capture_output,
                text=True,
                check=True
            )
            return result.stdout.strip() if capture_output else True
        except subprocess.CalledProcessError as e:
            print(f"❌ Command failed: {command}")
            print(f"Error: {e}")
            return False
    
    def create_github_repo(self):
        """Create GitHub repository"""
        print("\n📁 Creating GitHub repository...")
        
        headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        data = {
            'name': self.repo_name,
            'description': 'Telegram Bot with GitHub Actions deployment',
            'private': False,
            'auto_init': False
        }
        
        response = requests.post(
            'https://api.github.com/user/repos',
            headers=headers,
            json=data
        )
        
        if response.status_code == 201:
            print("✅ Repository created successfully!")
            return True
        elif response.status_code == 422:
            print("⚠️  Repository already exists, continuing...")
            return True
        else:
            print(f"❌ Failed to create repository: {response.json()}")
            return False
    
    def setup_git_repo(self):
        """Initialize and setup git repository"""
        print("\n🔧 Setting up Git repository...")
        
        # Initialize git if not already done
        if not os.path.exists('.git'):
            self.run_command('git init')
        
        # Create .gitignore
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/
"""
        
        with open('.gitignore', 'w') as f:
            f.write(gitignore_content)
        
        # Create README if it doesn't exist
        if not os.path.exists('README.md'):
            readme_content = f"""# {self.repo_name}

A Telegram chatbot with GitHub Actions deployment.

## Features
- Easy training with brain.py
- Automated deployment with GitHub Actions
- 24/7 hosting on GitHub

## Setup
1. Fork this repository
2. Add your `BOT_TOKEN` to GitHub Secrets
3. Push changes to trigger deployment

## Local Development
```bash
pip install -r requirements.txt
python main.py
```

## Training the Bot
```bash
python brain.py
```

Bot is automatically deployed when you push to the main branch!
"""
            with open('README.md', 'w') as f:
                f.write(readme_content)
        
        # Add all files
        self.run_command('git add .')
        
        # Commit
        self.run_command('git commit -m "Initial commit: Telegram bot with GitHub Actions"')
        
        # Add remote
        remote_url = f'https://{self.username}:{self.token}@github.com/{self.username}/{self.repo_name}.git'
        self.run_command(f'git remote remove origin', capture_output=True)  # Remove if exists
        self.run_command(f'git remote add origin {remote_url}')
        
        # Set main branch
        self.run_command('git branch -M main')
        
        print("✅ Git repository setup complete!")
        return True
    
    def create_github_secret(self):
        """Create GitHub secret for bot token"""
        print("\n🔐 Setting up GitHub secrets...")
        
        # First, get the repository public key
        headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Get public key
        response = requests.get(
            f'https://api.github.com/repos/{self.username}/{self.repo_name}/actions/secrets/public-key',
            headers=headers
        )
        
        if response.status_code != 200:
            print(f"❌ Failed to get public key: {response.json()}")
            return False
        
        public_key_data = response.json()
        
        # Encrypt the secret using PyNaCl
        try:
            from nacl import encoding, public
            
            public_key = public.PublicKey(public_key_data['key'].encode('utf-8'), encoding.Base64Encoder())
            sealed_box = public.SealedBox(public_key)
            encrypted = sealed_box.encrypt(self.bot_token.encode('utf-8'))
            encrypted_value = encoding.Base64Encoder().encode(encrypted).decode('utf-8')
            
        except ImportError:
            print("Installing PyNaCl for secret encryption...")
            self.run_command('pip install PyNaCl')
            from nacl import encoding, public
            
            public_key = public.PublicKey(public_key_data['key'].encode('utf-8'), encoding.Base64Encoder())
            sealed_box = public.SealedBox(public_key)
            encrypted = sealed_box.encrypt(self.bot_token.encode('utf-8'))
            encrypted_value = encoding.Base64Encoder().encode(encrypted).decode('utf-8')
        
        # Create the secret
        secret_data = {
            'encrypted_value': encrypted_value,
            'key_id': public_key_data['key_id']
        }
        
        response = requests.put(
            f'https://api.github.com/repos/{self.username}/{self.repo_name}/actions/secrets/BOT_TOKEN',
            headers=headers,
            json=secret_data
        )
        
        if response.status_code == 201 or response.status_code == 204:
            print("✅ GitHub secret created successfully!")
            return True
        else:
            print(f"❌ Failed to create secret: {response.status_code}")
            return False
    
    def push_to_github(self):
        """Push code to GitHub"""
        print("\n📤 Pushing to GitHub...")
        
        result = self.run_command('git push -u origin main', capture_output=False)
        if result:
            print("✅ Code pushed successfully!")
            return True
        else:
            print("❌ Failed to push code")
            return False
    
    def trigger_workflow(self):
        """Trigger GitHub Actions workflow"""
        print("\n🔄 Triggering GitHub Actions workflow...")
        
        headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        data = {
            'ref': 'main'
        }
        
        response = requests.post(
            f'https://api.github.com/repos/{self.username}/{self.repo_name}/actions/workflows/deploy-bot.yml/dispatches',
            headers=headers,
            json=data
        )
        
        if response.status_code == 204:
            print("✅ Workflow triggered successfully!")
            print(f"🌐 Check your workflow at: https://github.com/{self.username}/{self.repo_name}/actions")
            return True
        else:
            print(f"⚠️  Workflow will auto-trigger on push")
            return True
    
    def deploy(self):
        """Main deployment function"""
        print("🤖 Starting Telegram Bot GitHub Deployment...")
        
        self.get_credentials()
        
        if not self.create_github_repo():
            sys.exit(1)
        
        if not self.setup_git_repo():
            sys.exit(1)
        
        if not self.create_github_secret():
            sys.exit(1)
        
        if not self.push_to_github():
            sys.exit(1)
        
        self.trigger_workflow()
        
        print("\n" + "=" * 50)
        print("🎉 DEPLOYMENT COMPLETE!")
        print("=" * 50)
        print(f"📍 Repository: https://github.com/{self.username}/{self.repo_name}")
        print(f"🔧 Actions: https://github.com/{self.username}/{self.repo_name}/actions")
        print(f"📱 Your bot should be running within 2-3 minutes!")
        print("\n💡 Tips:")
        print("- Edit brain.py to train your bot")
        print("- Push changes to auto-deploy")
        print("- Check Actions tab for deployment status")
        print("- Your bot will run 24/7 on GitHub!")

def main():
    """Main function"""
    deployer = GitHubDeployer()
    deployer.deploy()

if __name__ == "__main__":
    main()