"""Script to check required dependencies."""
import importlib
import sys

required_packages = [
    'pandas',
    'numpy',
    'plotly',
    'pptx',
    'kaleido'
]

def check_requirements():
    missing_packages = []
    for package in required_packages:
        try:
            importlib.import_module(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing required packages:")
        for package in missing_packages:
            print(f"- {package}")
        print("\nPlease install missing packages using:")
        print(f"pip install {' '.join(missing_packages)}")
        sys.exit(1)
    
    print("All required packages are installed.")

if __name__ == "__main__":
    check_requirements() 