import subprocess

def install_requirements(requirements_file):
    with open(requirements_file, 'r') as file:
        packages = file.read().splitlines()

    for package in packages:
        subprocess.check_call(['pip', 'install', package])

if __name__ == "__main__":
    requirements_file = "requirements.txt"
    install_requirements(requirements_file)