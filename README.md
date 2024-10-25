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
   git clone https://github.com/faridamrah/test-project.git
   cd test-project

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

# Inter-pod communication


### Environment Variables

- **`CHROME_NODE_SERVICE`**: Specifies the service name of the Selenium Hub. The default value is set to `selenium-hub`. Ensure that this variable is set to the correct service name in your Kubernetes deployment.

## Architecture

The framework uses inter-pod communication to interact with the Selenium infrastructure:

1. **Test Case Controller**: This is the main script that contains various test cases.
2. **Selenium Hub Communication**: The test case controller communicates with the Selenium Hub using the `selenium_hub_url`. This URL is constructed using the `CHROME_NODE_SERVICE` environment variable, allowing the controller to send requests to the Hub.

3. **Request Flow**:
   - The test case controller checks the status of the Selenium Hub by sending a request to `http://{CHROME_NODE_SERVICE}:4444/wd/hub/status`.
   - If the Selenium Hub is available and ready, the controller sends test execution requests to it.
   - The Selenium Hub receives these requests and forwards them to the available Chrome node pods for execution.
   - Once the tests are executed, the results are logged by the test case controller.

# Helm Chart Deployment Script

This Python script automates the deployment of Helm charts to a Kubernetes cluster. It first attempts to load the kubeconfig from the default location, and if that fails, it prompts the user for the path to their kubeconfig file. The script deploys two Helm charts: `chrome-node` and `test-case-controller`, in that specific order.

## Prerequisites

Before using this script, ensure that you have the following installed:

- **Python** (version 3.6 or higher)
- **Helm** (version 3.x)
- **Kubernetes CLI (`kubectl`)** (for interacting with the Kubernetes cluster)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/faridamrah/test-project.git
   cd test-project
   ```
2. Install the required Python packages:

   ```bash
   pip install kubernetes 

   or

   pip install -r python/deployment/requirements.txt
   ```
3. Ensure that Helm is installed. You can install Helm by running:
   ```bash
   curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
   ```

## Usage

1. Place your Helm chart folders (`chrome-node` and `test-case-controller`) in the same directory as the script, or modify the paths in the script to point to their locations.

2. Run the script:

   ```bash
   python python/deployment/deploy_helm.py
   ```

3. If the script does not find the kubeconfig at the default location (`~/.kube/config)`, it will prompt you to provide the path to your kubeconfig file.

4. Script will list all contexts from the kubeconfig file. If multiple contexts are available, it will prompt the user to select one of them before proceeding with the Helm chart deployments.

## How It Works

- **Load Kubeconfig**: The script first tries to load the kubeconfig from the default location. If it fails, it prompts the user for an alternative path.
- **Deploy Helm Charts**: The script deploys the Helm charts using the `helm upgrade --install` command. The charts are applied in the order specified in the script (first `chrome-node`, then `test-case-controller`).
- **Error Handling:** The script includes error handling for kubeconfig loading and Helm command execution, providing clear feedback for troubleshooting.

## Example Output

```
Successfully loaded kubeconfig from the default location.
Deploying chrome-node from ./chrome-node...
Running command: helm upgrade --install chrome-node ./chrome-node
Successfully deployed chrome-node.
Deploying test-case-controller from ./test-case-controller...
Running command: helm upgrade --install test-case-controller ./test-case-controller
Successfully deployed test-case-controller.
```