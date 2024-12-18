import subprocess
from datetime import datetime

def read_requirements(file_path):
    """Read package names from a requirements.txt file."""
    packages = []
    try:
        with open(file_path, "r") as file:
            for line in file:
                # Ignore comments and blank lines
                if line.strip() and not line.startswith("#"):
                    # Split to exclude version specifiers like 'package==1.0.0'
                    package = line.split("==")[0].strip()
                    packages.append(package)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    return packages

def get_package_version(package_name):
    """Get the version of a given package using pip show."""
    try:
        result = subprocess.run(
            ["pip", "show", package_name], capture_output=True, text=True, check=True
        )
        for line in result.stdout.split("\n"):
            if line.startswith("Version:"):
                return line.split(":")[1].strip()
    except subprocess.CalledProcessError:
        return "Not Installed"

def save_to_new_requirements(packages_with_versions):
    """Save the package list with versions to a new requirements_<timestamp>.txt file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    new_file_name = f"requirements_{timestamp}.txt"
    
    with open(new_file_name, "w") as file:
        for package, version in packages_with_versions.items():
            file.write(f"{package}=={version}\n")
    print(f"\nPackage list saved to '{new_file_name}'")

if __name__ == "__main__":
    requirements_file = "requirements.txt"  # Path to the requirements file
    
    print("Reading package list from 'requirements.txt'...\n")
    packages = read_requirements(requirements_file)
    
    if not packages:
        print("No packages found in the requirements file.")
    else:
        print("Installed Package Versions:\n")
        packages_with_versions = {}
        
        for package in packages:
            version = get_package_version(package)
            if version == "Not Installed":
                print(f"{package}: Not Installed")
            else:
                print(f"{package}: {version}")
                packages_with_versions[package] = version
        
        # Save the packages with versions to a new requirements file
        save_to_new_requirements(packages_with_versions)
