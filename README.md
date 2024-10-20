# Automated Web Testing Script with Selenium

## Overview
This Python script automates web testing for the Insider website using Selenium WebDriver. It runs multiple test cases to validate page navigation, job listings, and career page elements. The script interacts with the Selenium Hub, performs checks on the availability of the hub, and runs tests in a loop until the hub is ready.

## Features:
- **Selenium Hub Status Check:** Verifies if the Selenium Hub is up and running before starting tests.
- **Test Case 1:** Validates the successful loading of the Insider homepage.
- **Test Case 2:** Navigates to the Careers page and verifies the visibility of key blocks like "Life at Insider" and "Our Locations."
- **Test Case 3:** Validates job filtering by department and location on the QA careers page.
- **Test Case 4:** Ensures job URLs redirect to the correct job application portal.

## Setup Instructions for Kubernetes

To deploy and run the Selenium Grid and WebDriver service within Kubernetes, follow these steps:

### Prerequisites:
1. **Kubernetes Cluster**: Ensure you have a running Kubernetes cluster and the `kubectl` command configured to interact with it.
2. **Selenium Grid Configuration**: A YAML configuration file for deploying the Selenium Grid on Kubernetes. The grid will include the Selenium Hub and Chrome nodes for remote testing.
3. **apply_k8s.sh script**: This script is used to apply the necessary Kubernetes configurations.

### Step-by-Step Instructions:

1. **Clone the repository** (if applicable) containing the Selenium Grid configuration and the `apply_k8s.sh` script.
   ```bash
   git clone <repository-url>
   cd <repository-directory>

2. **Execute the apply_k8s.sh Script:** The apply_k8s.sh script will apply the necessary Kubernetes configurations to deploy the Selenium Hub and Chrome nodes. Run the following command:
   ```bash
   chmod +x apply_k8s.sh
   ./apply_k8s.sh
This script will:

- Deploy the Selenium Hub service and deployment.
- Deploy the Chrome Nodes as part of the Selenium Grid.

**Verify the Deployment:** After running the script, ensure the services and pods are running successfully in your Kubernetes cluster. You can check the status with:
   ```bash
    kubectl get pods
    kubectl get services
```
Ensure all pods, especially the Selenium Hub, Chrome nodes, and Test case Controller are in the `Running` state.

3. **Check test cases**
    ```bash
    kubectl logs deployment/test-case-controller -f
Now, the output of every test case will be shown


## Setup Instructions for Running Tests Locally

This guide will help you run automated web tests on your local machine using the `test_cases_local.py` script.

### Prerequisites:
1. **Python 3.x**: Ensure Python 3.x is installed on your local machine. You can download it from [Python's official website](https://www.python.org/downloads/).
   
   Verify installation by running:
   ```bash
   python --version
**Google Chrome:** The script uses ChromeDriver to automate browser actions, so make sure Google Chrome is installed on your machine.

**Install Required Python Packages:** The required libraries are listed in `requirements.txt`.
Use `pip` to install them.

If you don’t have the `requirements.txt` file, create it with the following content:
```
    selenium
    pytz
```
Then, install the dependencies:

```bash
pip install -r requirements.txt
```
### Step-by-Step Instructions:

1. **Download ChromeDriver:** Download the correct version of ChromeDriver that matches your installed Chrome browser version.
Once downloaded, place chromedriver in a directory in your system’s PATH or specify its location directly in your script if it's in a non-standard location.

2. **Verify ChromeDriver Installation:** Run the following command to verify that ChromeDriver is correctly installed and accessible:
```bash
chromedriver --version
```
3. **Run the Script:** To execute the `test_cases_local.py` script, run the following command:
```bash
python test_cases_local.py
```
This script will execute the following test cases:

- Test Case 1: Validate the opening of the Insider home page.
- Test Case 2: Navigate to the Careers page, verify the visibility of key blocks, and check locations.
- Test Case 3: Navigate to the QA Careers page, filter by department and location, and validate job details.
- Test Case 4: Validate job URLs to ensure they redirect correctly.

4. **Result Output:** The script will output the results of each test case directly in the console with timestamps in CET timezone, indicating whether each test passed or failed.

## Example of Running the Script:
```bash
python test_cases_local.py
```
The script will automatically open the Chrome browser in headless mode (i.e., no visible browser window) and perform the web tests.

