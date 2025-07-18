#!/usr/bin/env python3
"""
Initial commit and push script for a new project.

This script automates the following steps:
1. Initializes a git repository if one doesn't exist (`git init`).
2. Checks for an existing repository on GitHub.
3. If the GitHub repository exists and already has commits, the script will exit.
4. If there are no local commits, it creates an initial commit with all current files (`git add .`, `git commit`).
5. If the GitHub repository doesn't exist, it creates it using `gh repo create`.
6. Pushes the local repository to GitHub, setting up the 'origin' remote and upstream branch.
"""

import subprocess
import sys
import os

def run_command(command, description, check=True):
    """Run a shell command and handle errors."""
    print(f"-> {description}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout.strip())
        if result.stderr:
            print(result.stderr.strip(), file=sys.stderr)
        if check and result.returncode != 0:
            print(f"Error: Command failed: {command}", file=sys.stderr)
            sys.exit(1)
        return result
    except Exception as e:
        print(f"Exception while running '{command}': {e}", file=sys.stderr)
        sys.exit(1)

def main():
    """Create initial commit for the project and push to GitHub."""
    project_name = os.path.basename(os.getcwd())
    
    print(f"Starting setup for project: {project_name}")
    print("="*50)
    
    # Check if GitHub CLI is available and authenticated
    run_command("gh auth status", "Checking GitHub CLI authentication status")

    # 1. Ensure we are in a git repository
    if not os.path.isdir('.git'):
        print("This is not a git repository.")
        run_command("git init", "Initializing new git repository")
    else:
        print("Git repository already exists locally.")

    # 2. Check if the repository on GitHub exists
    print(f"Checking for GitHub repository '{project_name}'...")
    repo_check_result = run_command(f"gh repo view {project_name}", "Checking GitHub repository existence", check=False)
    repo_exists_on_github = repo_check_result.returncode == 0

    if repo_exists_on_github:
        print("Repository exists on GitHub.")
        # If it exists, check if it's empty.
        # First, ensure remote 'origin' is set up to point to it.
        remote_check_result = run_command("git remote get-url origin", "Checking for remote 'origin'", check=False)
        if remote_check_result.returncode != 0:
            gh_user = run_command("gh api user --jq .login", "Getting GitHub username").stdout.strip()
            add_remote_cmd = f"git remote add origin https://github.com/{gh_user}/{project_name}.git"
            run_command(add_remote_cmd, "Adding remote 'origin'")
        
        # Now check for commits on the remote.
        remote_commit_check = run_command("git ls-remote --heads origin", "Checking for commits on remote", check=False)
        if remote_commit_check.stdout.strip():
            print("GitHub repository is not empty. Aborting script.", file=sys.stderr)
            print("This script is for initializing a project. The remote already has content.", file=sys.stderr)
            sys.exit(1)
        print("GitHub repository is empty. Ready to push.")
    
    # 3. Check for local commits
    local_commit_check = run_command("git rev-parse --verify HEAD", "Checking for local commits", check=False)
    has_local_commits = local_commit_check.returncode == 0

    if not has_local_commits:
        print("No local commits found. Creating initial commit.")
        # Use 'git add -A' to ensure all changes (new, modified, and deleted files) are staged.
        run_command("git add -A", "Adding all files and changes to staging area")
        
        # Check if there is anything to commit
        status_check = run_command("git status --porcelain", "Checking for changes to commit", check=False)
        if not status_check.stdout.strip():
            print("No changes to commit. Working directory is clean.")
            # If remote is also empty, there is nothing to do.
            if not repo_exists_on_github:
                 print("Aborting because there are no local changes to create a new repository with.")
                 sys.exit(0)
        else:
            commit_message = f"Initial commit for {project_name}"
            run_command(f'git commit -m "{commit_message}"', "Creating initial commit")
    else:
        print("Local commits already exist.")

    # 4. Push to GitHub
    if not repo_exists_on_github:
        print("Creating new GitHub repository and pushing...")
        # This command creates the repo, sets the remote, and pushes.
        create_cmd = f"gh repo create {project_name} --public --source=. --remote=origin --push"
        run_command(create_cmd, "Creating GitHub repository and pushing initial commit")
    else:
        # The repo exists on GitHub (but is empty), and we have local commits.
        print("Pushing local commits to empty GitHub repository...")
        # Find current branch to push
        branch_name = run_command("git symbolic-ref --short HEAD", "Getting current branch name").stdout.strip()
        run_command(f"git push -u origin {branch_name}", f"Pushing to origin/{branch_name}")

    print("\nInitial setup and push completed successfully!")
    gh_user = run_command("gh api user --jq .login", "Getting GitHub username").stdout.strip()
    print(f"GitHub URL: https://github.com/{gh_user}/{project_name}")

if __name__ == "__main__":
    main()
