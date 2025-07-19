#!/usr/bin/env python3
# File: SetupProject.py
# Path: Tools/SetupProject.py
# Standard: AIDEV-PascalCase-2.1
# Created: 2025-07-17
# Last Modified: 2025-07-17  10:45AM

"""
Set up a new project with links to Project_BaseFiles
Usage: python SetupProject.py /path/to/new/project
"""

import os
import sys
import shutil
from pathlib import Path

def setup_project(project_path):
    """Set up a new project with base file links"""
    
    project_path = Path(project_path).resolve()
    base_path = Path.home() / "Desktop" / "Project_BaseFiles"
    
    print(f"🚀 Setting up project at {project_path}")
    
    # Create project directory
    project_path.mkdir(parents=True, exist_ok=True)
    
    # Create symlinks
    symlinks = {
        "Scripts": base_path / "Scripts",
        "Docs/Standards": base_path / "Docs/Standards",
        "Docs/Templates": base_path / "Docs/Templates",
        ".vscode/settings.json": base_path / "Config/VSCode/settings.json",
        ".vscode/tasks.json": base_path / "Config/VSCode/tasks.json",
        ".gitignore": base_path / "Config/Git/.gitignore-Python"
    }
    
    for link_name, target in symlinks.items():
        link_path = project_path / link_name
        link_path.parent.mkdir(parents=True, exist_ok=True)
        
        if link_path.exists() or link_path.is_symlink():
            if link_path.is_symlink():
                link_path.unlink()
            else:
                if link_path.is_dir():
                    shutil.rmtree(link_path)
                else:
                    link_path.unlink()
        
        os.symlink(target, link_path)
        print(f"  🔗 Linked: {link_name}")
    
    # Copy templates for customization
    templates_to_copy = {
        "README.md": base_path / "Docs/Templates/README-Template.md",
        "CLAUDE.md": base_path / "Docs/Templates/CLAUDE-Template.md",
        "requirements.txt": base_path / "Config/Python/requirements-common.txt"
    }
    
    for dest_name, src_path in templates_to_copy.items():
        dest_path = project_path / dest_name
        if not dest_path.exists():
            shutil.copy2(src_path, dest_path)
            print(f"  📝 Copied: {dest_name}")
    
    # Create project-specific directories
    project_dirs = ["Docs/Technical", "Tests", "Examples"]
    for dir_name in project_dirs:
        (project_path / dir_name).mkdir(parents=True, exist_ok=True)
    
    print(f"✅ Project setup complete!")
    print(f"📝 Don't forget to customize README.md and CLAUDE.md")
    print(f"🚀 Access scripts via: python Scripts/QuickLauncher.py")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python SetupProject.py /path/to/new/project")
        sys.exit(1)
    
    setup_project(sys.argv[1])
