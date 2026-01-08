#!/usr/bin/env python3
import os
import sys
import subprocess
import zipfile
import urllib.request
import shutil

def run_install():
    repo_name = "Data-Sonification"
    repo_url = f"https://github.com/Tim-Albiges/{repo_name}.git"
    zip_url = f"https://github.com/Tim-Albiges/{repo_name}/archive/refs/heads/main.zip"
    
    # 1. Handle existing directory to avoid errors
    if os.path.exists(repo_name):
        print(f"♻️ Existing '{repo_name}' found. Reinstalling...")
        # Optional: shutil.rmtree(repo_name) # Uncomment to force a clean slate
    else:
        try:
            print("Cloning repository via Git...")
            subprocess.check_call(["git", "clone", repo_url])
        except (FileNotFoundError, subprocess.CalledProcessError):
            print("Git not found or failed. Downloading ZIP fallback...")
            zip_path = "temp_repo.zip"
            urllib.request.urlretrieve(zip_url, zip_path)
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(".")
            
            # ZIP extracts to 'Data-Sonification-main', rename to standard
            extracted_name = f"{repo_name}-main"
            if os.path.exists(extracted_name):
                os.rename(extracted_name, repo_name)
            os.remove(zip_path)

    # 2. Install using the absolute path to avoid os.chdir issues
    root_path = os.path.abspath(repo_name)
    packages = ["sonify-synth", "sonify-plot"]
    
    for pkg in packages:
        pkg_path = os.path.join(root_path, pkg)
        print(f"Installing {pkg}...")
        # Added -q for 'quiet' to keep output clean
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "-e", pkg_path])

    print("\n Installation complete!")
    print("You can now use: from sonify_plot import sonify")

if __name__ == "__main__":
    run_install()