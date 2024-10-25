import os
import subprocess
from kubernetes import config, client

def load_kubeconfig():
    """Load kubeconfig from the default location or prompt user for the path."""
    try:
        config.load_kube_config()
        print("Successfully loaded kubeconfig from the default location.")
    except Exception as e:
        print(f"Failed to load kubeconfig: {e}")
        kubeconfig_path = input("Please provide the path to your kubeconfig: ").strip()
        try:
            config.load_kube_config(config_file=kubeconfig_path)
            print(f"Successfully loaded kubeconfig from: {kubeconfig_path}")
        except Exception as err:
            print(f"Error loading kubeconfig from {kubeconfig_path}: {err}")
            exit(1)

    # List all contexts and ask the user to select one if multiple exist
    contexts, active_context = config.list_kube_config_contexts()
    if len(contexts) > 1:
        print("Multiple contexts found in kubeconfig:")
        for i, context in enumerate(contexts):
            print(f"{i + 1}: {context['name']}")
        choice = input("Select a context by number (default is 1): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(contexts):
            selected_context = contexts[int(choice) - 1]['name']
        else:
            selected_context = active_context['name']
    else:
        selected_context = active_context['name']

    print(f"Using context: {selected_context}")
    config.load_kube_config(context=selected_context)

def run_helm_command(command):
    """Run a Helm command and handle any errors."""
    try:
        print(f"Running command: {' '.join(command)}")
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing Helm command: {e.stderr}")
        exit(1)

def deploy_helm_chart(chart_name, chart_path):
    """Deploy a Helm chart."""
    print(f"Deploying {chart_name} from {chart_path}...")
    command = ["helm", "upgrade", "--install", chart_name, chart_path]
    run_helm_command(command)
    print(f"Successfully deployed {chart_name}.")

def main():
    # Load kubeconfig for cluster access
    load_kubeconfig()

    # Define Helm chart paths and names
    charts = [
        {"name": "chrome-node", "path": "../../chrome-node"},
        {"name": "test-case-controller", "path": "../../test-case-controller"}
    ]

    # Deploy charts in the specified order
    for chart in charts:
        chart_name = chart["name"]
        chart_path = chart["path"]

        # Ensure the chart directory exists
        if not os.path.exists(chart_path):
            print(f"Error: Chart directory not found: {chart_path}")
            exit(1)

        # Deploy the Helm chart
        deploy_helm_chart(chart_name, chart_path)

if __name__ == "__main__":
    main()
