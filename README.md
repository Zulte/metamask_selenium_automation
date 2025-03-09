# MetaMask Automation Module

This module provides a set of functions to automate interactions with the MetaMask browser extension using Selenium. It includes features for wallet registration, logging in with a recovery phrase, approving connection requests, switching networks, signing in, and more—all while logging events with Loguru.

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Module Overview](#module-overview)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Automated Wallet Registration:**  
  Registers a new MetaMask wallet and retrieves the generated recovery phrase.

- **Automated Login:**  
  Logs into MetaMask using a provided recovery phrase and sets up a password.

- **Connection Approvals:**  
  Approves connection requests by interacting with open browser windows.

- **Network Switching:**  
  Switches the MetaMask network using automated UI navigation and JavaScript execution.

- **Sign In Automation:**  
  Automates the sign-in process through UI interactions and JavaScript.

- **Error Logging:**  
  Uses Loguru to log errors and capture screenshots for troubleshooting.

---

## Requirements

- **Python 3.x**  
- **Selenium**  
- **Loguru**  
- **WebDriver** for your browser (e.g., ChromeDriver for Google Chrome)

---

## Installation

1. **Clone this Repository:**

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name

2. **Create and Activate a Virtual Environment (optional but recommended):**

python -m venv venv
source venv/bin/activate

3. **Install the Required Packages:**

pip install -r requirments.txt

4. **Download the ChromeDriver and Metamask extension and ensure it is in your system’s PATH or specify its path when initializing Selenium.**


## Usage
Below is a sample snippet on how to use the module:

```python
from selenium import webdriver
from your_module_name import Metamask  # Replace with the actual module name

# Initialize the Selenium WebDriver (using Chrome in this example)
driver = webdriver.Chrome()

# Create an instance of the Metamask class with the driver
mm = Metamask(driver)

# Example: Register a new wallet and obtain recovery words
recovery_phrase = mm.register_new_wallet()
print("Recovery Phrase:", recovery_phrase)

# Example: Login using the recovered recovery phrase
mm.login_to_metamask(recovery_phrase)

# Remember to close the driver after operations are complete
driver.quit()
```


## Module Overview
The module is structured around the Metamask class which includes the following methods:

```python
 __init__(self, driver)
```
Initializes the module with a Selenium WebDriver instance and sets up logging.

```python 
_click_element(self, element)
```
A helper method to click elements using an XPath.

```python
login_to_metamask(self, recovery_words)
```
Automates the login process by navigating through MetaMask’s onboarding flow, entering the recovery phrase, and setting a password.

```python
register_new_wallet(self)
```
Automates the process of registering a new wallet. It guides through the setup process and retrieves the generated recovery phrase.

```python
approve_connect(self)
```
Iterates through browser windows to find and approve connection requests by clicking the appropriate confirmation button.

```python
switch_network(self)
```
Switches the MetaMask network by navigating to network settings, entering the password, and using JavaScript to trigger the network change.

```python
connect(self)
```
Executes JavaScript across open browser windows to approve a generic connection request.

```python
sign_in(self)
```
Automates the sign-in process by locating and clicking a 'Confirm' button.

```python
pass_or_login(self, wallet)
```
Determines if a wallet is already set up by checking for a password input field; if not, it triggers the full login process using the provided recovery phrase.

Each method includes error handling and logging, ensuring that issues are recorded and screenshots are captured when needed.


## Contributing
Contributions are welcome! If you find an issue or have suggestions for improvements:

Fork the repository.
Create a new branch for your feature or bug fix.
Commit your changes and push your branch.
Open a pull request describing your changes.

## License
Feel free to adjust the sections (such as the repository URL, module name, and any additional instructions) to match your project’s specifics. This README provides a clear overview of the module’s functionality, setup instructions, and usage examples for potential users or contributors.
