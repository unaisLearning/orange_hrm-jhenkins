"""
Configuration settings for the test framework.
"""
import os
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class EnvironmentConfig:
    """Environment-specific configuration."""
    base_url: str
    implicit_wait: int = 5  # Reduced from default
    explicit_wait: int = 10  # Reduced from default
    page_load_timeout: int = 20  # Reduced from default
    screenshot_dir: str = "screenshots"
    report_dir: str = "reports"
    allure_results_dir: str = "allure-results"
    browser: str = "chrome"
    headless: bool = True  # Enable headless mode
    ci_mode: bool = False

class Config:
    """Configuration manager for different environments."""
    
    # Environment configurations
    ENVIRONMENTS: Dict[str, EnvironmentConfig] = {
        'dev': EnvironmentConfig(
            base_url="https://opensource-demo.orangehrmlive.com",
            implicit_wait=5,
            explicit_wait=10,
            page_load_timeout=20,
            headless=True
        ),
        'qa': EnvironmentConfig(
            base_url="https://qa.orangehrmlive.com",
            implicit_wait=5,
            explicit_wait=10,
            page_load_timeout=20,
            headless=True
        ),
        'prod': EnvironmentConfig(
            base_url="https://orangehrmlive.com",
            implicit_wait=5,
            explicit_wait=10,
            page_load_timeout=20,
            headless=True
        )
    }
    
    # Get current environment from environment variable or default to dev
    CURRENT_ENV = os.getenv('TEST_ENV', 'dev')
    config = ENVIRONMENTS[CURRENT_ENV]
    
    # Environment properties
    BASE_URL = config.base_url
    IMPLICIT_WAIT = config.implicit_wait
    EXPLICIT_WAIT = config.explicit_wait
    PAGE_LOAD_TIMEOUT = config.page_load_timeout
    SCREENSHOT_DIR = config.screenshot_dir
    REPORT_DIR = config.report_dir
    ALLURE_RESULTS_DIR = config.allure_results_dir
    BROWSER = config.browser
    HEADLESS = config.headless
    CI_MODE = config.ci_mode
    
    @classmethod
    def is_ci_mode(cls) -> bool:
        """Check if running in CI mode."""
        return cls.CI_MODE
    
    @classmethod
    def get_allure_environment_properties(cls) -> dict:
        """Get environment properties for Allure reporting."""
        return {
            'Browser': cls.BROWSER,
            'Environment': cls.CURRENT_ENV,
            'Base URL': cls.BASE_URL,
            'Headless': str(cls.HEADLESS),
            'CI Mode': str(cls.CI_MODE)
        }

    # Test credentials
    TEST_USERNAME: str = "Admin"
    TEST_PASSWORD: str = "admin123"
    
    # Screenshot settings
    HTML_REPORT_DIR: str = "reports"
    
    # Updated selectors based on current OrangeHRM demo page
    ERROR_MESSAGE = {'type': 'css', 'value': '.oxd-alert-content-text, .oxd-text--p'}
    REQUIRED_ERROR = {'type': 'css', 'value': '.oxd-input-field-error-message, .oxd-text--p'}
    
    WELCOME_MESSAGE = {'type': 'css', 'value': '.oxd-userdropdown-name, .oxd-userdropdown-tab'}
    
    @classmethod
    def get_browser_options(cls) -> Dict[str, Any]:
        """Get browser-specific options."""
        browser = cls.BROWSER.lower()
        options = {
            "browser_name": browser,
            "headless": cls.HEADLESS,
            "window_size": (1920, 1080),
            "arguments": []
        }
        
        print(f"Current environment: {cls.CURRENT_ENV}")
        print(f"Headless mode is: {cls.HEADLESS}")
        
        if browser == "chrome":
            if cls.HEADLESS:
                options["arguments"].append("--headless")
            options["arguments"].extend([
                "--window-size=1920,1080",
                "--disable-gpu",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-notifications",
                "--disable-extensions",
                "--remote-debugging-port=9222",
                "--disable-blink-features=AutomationControlled",
                "--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
            ])
        elif browser == "firefox":
            if cls.HEADLESS:
                options["arguments"].append("-headless")
            options["arguments"].append("--width=1920")
            options["arguments"].append("--height=1080")
        return options

    @classmethod
    def get_browser_options_for_browser(cls, browser_name: str) -> Dict[str, Any]:
        """Get browser-specific options for a specific browser."""
        options = Config.get_browser_options().get(browser_name, {})
        return options

    @classmethod
    def get_browser_options_for_current_browser(cls) -> Dict[str, Any]:
        """Get browser-specific options for the current browser."""
        return Config.get_browser_options_for_browser(cls.BROWSER.lower()) 