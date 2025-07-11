#!/usr/bin/env python3
"""
Initial commit script for project.
This script adds all files and creates the initial commit based on the base folder name.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a git command and handle errors."""
    print(f"Running: {description}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return False
        print(f"Success: {result.stdout}")
        return True
    except Exception as e:
        print(f"Exception: {e}")
        return False

def main():
    """Create initial commit for the project."""
    # Get the base folder name
    project_name = os.path.basename(os.getcwd())
    
    print(f"Creating initial commit for {project_name}")
    print("="*50)
    
    # Check if we're in a git repository
    if not os.path.exists('.git'):
        print("Error: Not in a git repository")
        sys.exit(1)
    
    # Add all files
    if not run_command("git add .", "Adding all files to staging area"):
        sys.exit(1)
    
    # Create initial commit
    commit_message = f"Initial commit - {project_name} project structure"
    if not run_command(f'git commit -m "{commit_message}"', "Creating initial commit"):
        sys.exit(1)
    
    print("\nInitial commit created successfully!")
    print(f"Project: {project_name}")
    print(f"Commit message: {commit_message}")

if __name__ == "__main__":
    main()