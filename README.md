# 🚀 Enterprise Selenium Test Automation Framework

## 🎯 Framework Highlights

- **Page Object Model** with centralized configuration
- **CI/CD Ready** (Jenkins + GitHub Actions)
- **Smart Browser Management** (Headless/GUI auto-detection)
- **Comprehensive Reporting** (Allure + Screenshots)
- **Multi-Environment Support** (Dev/QA/Prod)

## 🏗️ Architecture

# Automated Testing with Jenkins CI/CD

This project implements automated testing with Jenkins CI/CD pipeline.

## Prerequisites

1. Jenkins installed and running
2. Required Jenkins plugins:
   - Pipeline
   - Allure Jenkins Plugin
   - Git Integration
   - Workspace Cleanup Plugin

## Jenkins Setup

1. Install Jenkins:

   ```bash
   # For macOS using Homebrew
   brew install jenkins
   ```

2. Start Jenkins:

   ```bash
   brew services start jenkins
   ```

3. Install required Jenkins plugins:

   - Go to Jenkins Dashboard > Manage Jenkins > Manage Plugins
   - Install the following plugins:
     - Pipeline
     - Allure Jenkins Plugin
     - Git Integration
     - Workspace Cleanup Plugin

4. Configure Allure in Jenkins:
   - Go to Jenkins Dashboard > Manage Jenkins > Global Tool Configuration
   - Add Allure Commandline
   - Set installation directory

## Pipeline Configuration

1. Create a new Pipeline job in Jenkins:

   - Go to Jenkins Dashboard > New Item
   - Enter a name for your job
   - Select "Pipeline"
   - Click OK

2. Configure the pipeline:
   - In the job configuration page, select "Pipeline script from SCM"
   - Select "Git" as SCM
   - Enter your repository URL
   - Set the branch to build (e.g., \*/main)
   - Set the script path to "Jenkinsfile"
   - Save the configuration

## Running the Pipeline

1. The pipeline will automatically run when:

   - Code is pushed to the repository
   - Manual build is triggered
   - Scheduled build (if configured)

2. Pipeline stages:
   - Setup Environment: Creates Python virtual environment and installs dependencies
   - Run Tests: Executes the test suite and generates Allure reports
   - Post-build: Archives test results and cleans up workspace

## Viewing Results

1. Test results can be viewed in:
   - Allure Report: Detailed test execution report
   - Test Results: JUnit test results
   - Console Output: Build log

## Best Practices Implemented

1. Environment Management:

   - Virtual environment for Python dependencies
   - Environment variables for configuration

2. Test Execution:

   - Automated test execution
   - Allure reporting integration
   - Test result archiving

3. Workspace Management:

   - Automatic workspace cleanup
   - Artifact archiving

4. Error Handling:
   - Proper error reporting
   - Build status notifications

## Troubleshooting

1. If tests fail:

   - Check the Allure report for detailed test failures
   - Review the console output for environment setup issues
   - Verify test data and configuration

2. If pipeline fails:
   - Check Jenkins system log
   - Verify plugin installations
   - Ensure proper permissions are set
