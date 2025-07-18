# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the "Finder" project, part of Project Himalaya - a collection of Python-based file system utilities and tools for searching, organizing, and managing files. The project follows the AIDEV-PascalCase-2.1 Design Standard with strict header requirements and accountability protocols.

## Key Commands

### Project Setup
- `python SetupProject.py /path/to/new/project` - Set up a new project with base file links

### File Operations
- `python Scripts/Deployment/UpdateFiles.py` - Process Updates folder and move files to intended paths based on headers
- `python Scripts/System/CodebaseSum.py` - Generate comprehensive codebase snapshot
- `python Scripts/System/BackupProject.py` - Create project backup

### GitHub Operations
- `python Scripts/GitHub/GitHubAutoUpdate.py` - Auto-update GitHub repository
- `python Scripts/GitHub/GitHubInitialCommit.py` - Initial commit setup
- `bash Scripts/GitHub/BackToTheFuture.sh` - Git time manipulation

### File Search and Display
- `python Scripts/FinderDisplay/AdvancedFileSearcher.py` - Advanced GUI file search with include/exclude patterns
- `python Scripts/FinderDisplay/FindText.py` - Text search utilities
- `python Scripts/FinderDisplay/SimpleTree.py` - Directory tree visualization

## Architecture

The codebase is organized into functional script categories:

- **Scripts/FinderDisplay/** - GUI applications for file searching and display (PySide6-based)
- **Scripts/System/** - Core system utilities (backup, codebase analysis)
- **Scripts/GitHub/** - Git/GitHub automation tools
- **Scripts/Deployment/** - File management and deployment utilities
- **Scripts/DataBase/** - Database migration and porting tools
- **Scripts/Tools/** - Miscellaneous utility tools

## Design Standard Requirements

**CRITICAL**: All files must follow Design Standard v2.1 with mandatory header format:

```python
# File: [EXACT FILENAME WITH EXTENSION]
# Path: [EXACT DEPLOYMENT PATH - NO ASSUMPTIONS]
# Standard: AIDEV-PascalCase-2.1
# Created: YYYY-MM-DD
# Last Modified: YYYY-MM-DD  HH:MM[AM|PM]  ← MUST BE ACTUAL CURRENT TIME
```

### Mandatory AI Session Protocol

Before any file operations, Claude must acknowledge:
- Use ACTUAL CURRENT TIME in ALL headers (never placeholder times)
- Update file paths to match ACTUAL deployment locations
- Create unique timestamps for each file (no copy-paste headers)
- Verify header accuracy BEFORE functional changes

### Path Verification Requirements

- Always verify where files will actually be deployed/served
- File paths in headers must match deployment reality
- Announce path changes with explicit verification
- Use progressive timestamps showing actual creation sequence

## Testing and Validation

No specific test framework is configured. The project uses:
- Manual testing of GUI applications
- Validation through `Scripts/Deployment/UpdateFiles.py` for header compliance
- System-level testing of file operations

## Dependencies

- **PySide6** - For GUI applications (AdvancedFileSearcher, etc.)
- **Standard Python libraries** - os, sys, pathlib, shutil, subprocess, datetime
- **pathspec** - For gitignore pattern matching
- **PyPDF2** - For PDF processing in CodebaseSum

## Important Notes

- This is a console-based system with GUI child processes for specific tools
- All Python files use PascalCase naming convention
- Files are automatically processed through UpdateFiles.py based on header Path declarations
- GitHub operations are automated through dedicated scripts
- The system emphasizes user-friendly terminal interfaces following old-school CRT aesthetics