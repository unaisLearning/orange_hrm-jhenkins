"""
Test cases for login functionality.
"""
import pytest
import allure
import json
from pathlib import Path
from datetime import datetime
import os
import glob
import tempfile
import logging

from tests.base_test import BaseTest
from pages.login_page import LoginPage
from utils.logger import logger
from config.config import Config

@allure.epic('OrangeHRM')
@allure.feature('Authentication')
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
# OrangeHRM Login Test Suite

This test suite verifies the login functionality of OrangeHRM application.

## Test Coverage:
- Valid login scenarios
- Logout functionality

## Prerequisites:
- Valid OrangeHRM credentials
- Access to OrangeHRM demo site
""")
class TestLogin(BaseTest):
    """Test cases for login functionality."""
    
    def setup_method(self, method):
        """
        Setup for each test method.
        
        Args:
            method: The test method being called
        """
        # Call parent setup_method first
        super().setup_method(method)
        
        # Initialize login page
        self.login_page = LoginPage(self.driver)
        self.login_page.navigate()
        
        # Load test data
        test_data_path = Path(__file__).parent.parent / 'test_data' / 'login_test_data.json'
        with open(test_data_path) as f:
            self.test_data = json.load(f)
            
        # Add environment info to Allure
        allure.dynamic.parameter('Browser', Config.BROWSER)
        allure.dynamic.parameter('Environment', Config.CURRENT_ENV)
        allure.dynamic.parameter('Base URL', Config.BASE_URL)
        
        # Attach current log file to Allure report
        log_files = glob.glob('logs/test_run_*.log')
        if log_files:
            latest_log = max(log_files, key=os.path.getctime)
            with open(latest_log, 'r') as f:
                allure.attach(
                    f.read(),
                    name="test_log",
                    attachment_type=allure.attachment_type.TEXT
                )
    
    def teardown_method(self, method):
        """Teardown for each test method."""
        # Attach final log file to Allure report
        log_files = glob.glob('logs/test_run_*.log')
        if log_files:
            latest_log = max(log_files, key=os.path.getctime)
            with open(latest_log, 'r') as f:
                allure.attach(
                    f.read(),
                    name="test_log_final",
                    attachment_type=allure.attachment_type.TEXT
                )
        
        # Call parent teardown_method
        super().teardown_method(method)
    
    @pytest.mark.smoke
    @pytest.mark.critical
    @allure.story('Valid Login')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("""
    # Valid Login Test
    
    ## Test Objective:
    Verify that a user can successfully login with valid credentials.
    
    ## Test Steps:
    1. Navigate to login page
    2. Enter valid username
    3. Enter valid password
    4. Click login button
    5. Verify successful login
    
    ## Expected Result:
    User should be logged in successfully and redirected to dashboard.
    """)
    def test_valid_login(self):
        """Test valid login with correct credentials."""
        with allure.step("Navigate to login page"):
            self.login_page.navigate()
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="login_page",
                attachment_type=allure.attachment_type.PNG
            )
        
        with allure.step("Enter valid credentials"):
            self.login_page.login(
                self.test_data['valid_credentials']['username'],
                self.test_data['valid_credentials']['password']
            )
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="credentials_entered",
                attachment_type=allure.attachment_type.PNG
            )
        
        with allure.step("Verify successful login"):
            assert self.login_page.is_login_successful(), "Login was not successful"
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="login_successful",
                attachment_type=allure.attachment_type.PNG
            )
    
    @pytest.mark.regression  
    @pytest.mark.medium
    @allure.story('Logout')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description("""
    # Logout Test
    
    ## Test Objective:
    Verify that user can successfully logout from the application.
    
    ## Test Steps:
    1. Login with valid credentials
    2. Verify successful login
    3. Perform logout
    4. Verify successful logout
    
    ## Expected Result:
    User should be able to logout successfully.
    """)
    def test_logout(self):
        """Test logout functionality."""
        with allure.step("Login with valid credentials"):
            self.login_page.login(
                self.test_data['valid_credentials']['username'],
                self.test_data['valid_credentials']['password']
            )
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="login_for_logout",
                attachment_type=allure.attachment_type.PNG
            )
        
        with allure.step("Verify successful login"):
            assert self.login_page.is_login_successful(), "Login was not successful"
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="login_successful_for_logout",
                attachment_type=allure.attachment_type.PNG
            )
        
        with allure.step("Perform logout"):
            self.login_page.logout()
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="logout_clicked",
                attachment_type=allure.attachment_type.PNG
            )
        
        with allure.step("Verify successful logout"):
            assert not self.login_page.is_login_successful(), "Logout was not successful"
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="logout_successful",
                attachment_type=allure.attachment_type.PNG
            )

    @pytest.mark.negative
    @pytest.mark.high
    @allure.story('Invalid Login')
    def test_invalid_login(self):
        """Test login with invalid credentials."""
        with allure.step("Enter invalid credentials"):
            self.login_page.login("invalid", "invalid")
        
        with allure.step("Verify login failure"):
            assert not self.login_page.is_login_successful()
            error_msg = self.login_page.get_error_message()
            assert "Invalid credentials" in error_msg or "Username" in error_msg

@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    logging.shutdown() 