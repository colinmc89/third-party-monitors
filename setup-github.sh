#!/bin/bash
# GitHub Setup Script for Third Party Monitors

echo "🚀 Setting up GitHub repository..."
echo ""
echo "Please provide your GitHub username:"
read GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ GitHub username is required"
    exit 1
fi

echo ""
echo "Repository name (default: third-party-monitors):"
read REPO_NAME
REPO_NAME=${REPO_NAME:-third-party-monitors}

echo ""
echo "📝 Adding remote origin..."
git remote add origin https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git 2>/dev/null || git remote set-url origin https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git

echo "📝 Setting branch to main..."
git branch -M main

echo ""
echo "✅ Ready to push! But first:"
echo "   1. Make sure you've created the repository on GitHub:"
echo "      https://github.com/new"
echo "   2. Repository name should be: ${REPO_NAME}"
echo "   3. Don't initialize with README/gitignore"
echo ""
echo "Press Enter when ready to push..."
read

echo "🚀 Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo "   Repository: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
    echo ""
    echo "📋 Next steps:"
    echo "   1. Go to https://render.com (or https://railway.app)"
    echo "   2. Connect your GitHub account"
    echo "   3. Deploy this repository"
    echo "   4. Share the URL with your CEO!"
else
    echo ""
    echo "❌ Push failed. Make sure:"
    echo "   1. The repository exists on GitHub"
    echo "   2. You have push access"
    echo "   3. You're authenticated (may need to use GitHub token)"
fi

