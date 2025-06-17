#!/bin/bash

# Jenkins Setup Script for Automated Testing Framework
# This script helps set up Jenkins with all necessary plugins and configurations

echo "Setting up Jenkins for Automated Testing Framework..."

# Check if Jenkins is running
if ! brew services list | grep -q "jenkins.*started"; then
    echo "Starting Jenkins..."
    brew services start jenkins
    sleep 10
fi

echo "Jenkins is running at http://localhost:8080"
echo ""
echo "Please follow these steps to complete the setup:"
echo ""
echo "1. Open http://localhost:8080 in your browser"
echo "2. Get the initial admin password by running:"
echo "   cat ~/Library/Application\\ Support/Jenkins/secrets/initialAdminPassword"
echo ""
echo "3. Install the following plugins:"
echo "   - Pipeline"
echo "   - Allure Jenkins Plugin"
echo "   - Git Integration"
echo "   - Workspace Cleanup Plugin"
echo "   - JUnit Plugin"
echo "   - HTML Publisher Plugin"
echo "   - Blue Ocean (optional but recommended)"
echo ""
echo "4. Configure Allure Commandline:"
echo "   - Go to Manage Jenkins > Global Tool Configuration"
echo "   - Add Allure Commandline"
echo "   - Set installation directory: /usr/local/bin"
echo ""
echo "5. Create a new Pipeline job:"
echo "   - Name: 'Automated-Testing-Pipeline'"
echo "   - Type: Pipeline"
echo "   - Source: Pipeline script from SCM"
echo "   - SCM: Git"
echo "   - Repository URL: [Your Git repository URL]"
echo "   - Branch: */main"
echo "   - Script Path: Jenkinsfile"
echo ""
echo "6. Configure build triggers (optional):"
echo "   - Poll SCM: H/5 * * * * (every 5 minutes)"
echo "   - Or use webhooks for automatic builds"
echo ""
echo "Setup complete! Your Jenkins pipeline is ready to run automated tests." 