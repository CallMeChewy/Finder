# File: USER_GUIDE.md
# Path: /home/herb/Desktop/Finder/USER_GUIDE.md
# Standard: AIDEV-PascalCase-2.1
# Created: 2025-07-18
# Last Modified: 2025-07-18  13:52PM

# Finder Application - User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Interface Overview](#interface-overview)
3. [Basic Usage](#basic-usage)
4. [Advanced Features](#advanced-features)
5. [Formula Construction](#formula-construction)
6. [Search Examples](#search-examples)
7. [Educational Test Suite](#educational-test-suite)
8. [Tips and Best Practices](#tips-and-best-practices)
9. [Troubleshooting](#troubleshooting)
10. [Keyboard Shortcuts](#keyboard-shortcuts)

## Getting Started

### Installation and Requirements
- **Python 3.7+** required
- **PySide6** for GUI interface
- All dependencies included in the project

### Launching the Application
```bash
cd /home/herb/Desktop/Finder
python Finder.py
```

### First Time Setup
1. Launch the application
2. The default search path is set to the current directory
3. Default file types are `.txt` and `.md`
4. All settings can be changed before searching

## Interface Overview

### Main Window Layout
The Finder application is divided into two main panels:

#### Left Panel - Search Controls
- **Search Phrases (A-F)**: Input fields for up to 6 search terms
- **Search Mode**: Choose between Document or Line search
- **File Types**: Select which file extensions to search
- **Search Path**: Choose files or folders to search
- **Search Formula**: Construct logical formulas using variables A-F
  - **🔍 Start Search**: Green button below formula - validates and starts search
  - **✓ Validate Formula**: Orange button below formula - checks formula without searching
- **Control Buttons**: Reset/Clear, Run Examples (at bottom of controls)

#### Right Panel - Results Display
- **Search Results**: Shows matching files and content
- **Color-coded Display**: File paths in blue, line numbers in red/white
- **Scrollable Interface**: Navigate through large result sets

### Color Coding System
- **🔵 File Paths**: Light blue text
- **🔴 Unique Line Numbers**: Red numbers for first occurrences
- **⚪ Regular Line Numbers**: White numbers for repeated content
- **⚪ Content**: White text for matched content
- **🟢 Status Messages**: Green text for completion messages

## Basic Usage

### Simple Search (Level 1)
1. **Enter a Search Term**:
   - Click in the "A:" field
   - Type your search term (e.g., "python")
   - Leave other fields empty

2. **Choose File Types**:
   - Check desired file types (.txt, .md, .py, etc.)
   - Or enter custom extensions in the "Custom:" field

3. **Set Search Path**:
   - Click "Current Folder" for current directory
   - Click "Select Folder" to choose a different directory
   - Click "Select Files" to search specific files

4. **Run Search**:
   - Click the green "🔍 Start Search" button (below formula box)
   - Or click "✓ Validate Formula" first to check for errors
   - Results appear in the right panel
   - View matches with file names and line numbers

### Example: Find Python Files
```
Search Phrase:
  A: python

File Types:
  ☑ .py  ☑ .txt  ☑ .md

Formula: (auto-generated)
  A

Results:
  ✓ Found 25 matches in 12 files
```

## Advanced Features

### Multiple Search Terms
1. **Fill Multiple Variables**:
   - A: "class"
   - B: "function"
   - C: "method"

2. **Automatic Formula**:
   - The application automatically creates: `A AND B AND C`
   - Finds content containing all three terms

### Case Sensitivity Control
- **Match Case Checkbox**: Next to each phrase input
- **Unchecked (Default)**: Case-insensitive search
- **Checked**: Exact case matching required

Example:
```
A: "File" (Match Case ☑) - finds only "File"
B: "file" (Match Case ☐) - finds "file", "File", "FILE"
```

### Search Modes
- **Line Mode**: Searches line by line (default)
- **Document Mode**: Searches entire documents as units

### Unique Mode
- **Unique Checkbox**: Show only first occurrence of each match
- **Red Line Numbers**: Indicate unique occurrences
- **White Line Numbers**: Indicate repeated content

## Formula Construction

### Basic Operators
- **AND / &**: Both terms must be present
- **OR / |**: Either term can be present  
- **NOT / !**: Exclude this term
- **XOR / ^**: Exactly one term (but not both)

### Common Operator Variants
- **&& / &**: Both mean AND
- **|| / |**: Both mean OR
- **! / ~**: Both mean NOT

### Parentheses for Grouping
- **( )**: Standard parentheses
- **[ ]**: Square brackets (same as parentheses)
- **{ }**: Curly braces (same as parentheses)

### Formula Examples

#### Simple Formulas
```
A                    # Find content with term A
A AND B             # Find content with both A and B  
A OR B              # Find content with either A or B
NOT A               # Find content without A
```

#### Common Operator Formulas
```
A & B               # Same as A AND B
A | B               # Same as A OR B
!A                  # Same as NOT A
A && B              # Same as A AND B
A || B              # Same as A OR B
```

#### Complex Formulas
```
(A AND B) OR C      # Either (A and B) or C
A AND (B OR C)      # A and either B or C
A AND NOT B         # A but not B
(A OR B) AND (C OR D) # Either A or B, and either C or D
```

#### Expert Level Formulas
```
A & B & !C          # A and B, but not C
(A | B) & !(C | D)  # Either A or B, but not C or D
((A & B) | C) & D   # Complex nested logic
```

## Search Examples

### Example 1: Find Python Functions
```
Variables:
  A: def
  B: return

Formula: A AND B

Intent: Find Python functions that return values
```

### Example 2: Find Documentation Headers
```
Variables:
  A: #
  B: Standard
  C: Design

Formula: A & (B | C)

Intent: Find headers containing "Standard" or "Design"
```

### Example 3: Find Code Without Errors
```
Variables:
  A: function
  B: method
  C: error

Formula: (A | B) & !C

Intent: Find functions or methods without error mentions
```

### Example 4: Complex Pattern Matching
```
Variables:
  A: class
  B: def
  C: init
  D: self
  E: super

Formula: (A & B & D) | (C & E)

Intent: Find class methods with self OR init methods with super
```

## Educational Test Suite

### Accessing the Test Suite
1. **Click "Run Examples" Button**: Blue button in the control panel
2. **Information Dialog**: Read the description and click "OK"
3. **View Results**: Results appear in terminal or results panel

### What the Test Suite Provides
- **5 Complexity Levels**: Simple to Expert
- **Dynamic Generation**: Different examples each run
- **Detailed Explanations**: Learning points for each level
- **Real Examples**: Working formulas you can copy

### Learning Progression
1. **Level 1 (Simple)**: Single variable searches
2. **Level 2 (Basic)**: Two variables with AND/OR
3. **Level 3 (Medium)**: Parentheses and NOT operators
4. **Level 4 (Advanced)**: Multiple grouped conditions
5. **Level 5 (Expert)**: Complex nested logic

### Using Test Suite Results
1. **Copy Formulas**: Use examples in your own searches
2. **Modify Variables**: Change search terms to your needs
3. **Learn Patterns**: Understand common search structures
4. **Practice**: Try different complexity levels

## Tips and Best Practices

### Getting Started Tips
- **Start Simple**: Begin with single-term searches (Level 1)
- **Use Auto-Formula**: Let the app generate formulas automatically
- **Check File Types**: Ensure you're searching the right files
- **Test Small**: Start with a small folder to test formulas

### Formula Construction Tips
- **Use Parentheses**: Group related conditions clearly
- **Test Incrementally**: Add complexity gradually
- **Case Sensitivity**: Consider whether case matters
- **Performance**: Complex formulas take longer to execute

### Search Optimization
- **Specific Terms**: Use precise search terms
- **File Type Filtering**: Limit to relevant file types
- **Path Selection**: Search only necessary directories
- **Unique Mode**: Use when you want distinct results

### Common Patterns
```
# Find related concepts
A & B                # Both terms together

# Find alternatives  
A | B                # Either term

# Exclude unwanted content
A & !B               # A without B

# Complex relationships
(A & B) | (C & D)    # Either relationship

# Nested conditions
A & (B | C)          # A with either B or C
```

## Troubleshooting

### Common Issues

#### No Results Found
- **Check Spelling**: Verify search terms are correct
- **Case Sensitivity**: Try turning off "Match Case"
- **File Types**: Ensure correct file types are selected
- **Search Path**: Verify you're searching the right location

#### Formula Errors
- **Syntax Error**: Check parentheses are balanced
- **Invalid Operators**: Use supported operators (&, |, !, AND, OR, NOT)
- **Empty Variables**: Ensure referenced variables have content
- **Complex Logic**: Simplify formula and test incrementally

#### Performance Issues
- **Large Directories**: Search smaller, specific folders
- **Complex Formulas**: Use simpler formulas for large searches
- **File Filtering**: Limit file types to reduce search scope
- **Unique Mode**: Enable to reduce duplicate results

### Formula Validation

#### On-Demand Validation
- **✓ Validate Formula**: Click orange button below formula to check for errors
- **Validation Results**: Shows detailed analysis in popup dialogs
- **Error Details**: Specific error messages with suggestions
- **Warning Messages**: Alerts for potential issues but allows search
- **Success Confirmation**: ✅ confirmation when formula is valid

#### Validation Types
- **Syntax Errors**: Unbalanced parentheses, invalid operators
- **Structure Errors**: Missing operands, consecutive operators
- **Logic Warnings**: Paradoxes (A AND NOT A), tautologies (A OR NOT A)
- **Variable Warnings**: Undefined variables (G, H, etc.)

### Error Messages

#### "Invalid Formula"
- Use **✓ Validate Formula** button for detailed error analysis
- Check parentheses are balanced: `(A & B)`
- Verify operators are valid: `&, |, !, AND, OR, NOT`
- Ensure variables A-F are used correctly

#### "No Phrases"
- Enter at least one search term in fields A-F
- Check that phrase fields are not empty
- Verify formula references existing variables

#### "No File Types"
- Select at least one file type checkbox
- Or enter custom extensions in "Custom:" field
- Check that file types exist in search location

## Keyboard Shortcuts

### Navigation
- **Tab**: Move to next field
- **Shift+Tab**: Move to previous field
- **Enter**: Start search (when 🔍 Start Search button has focus)
- **Escape**: Cancel current search

### Field Shortcuts
- **Ctrl+A**: Select all text in current field
- **Ctrl+C**: Copy selected text
- **Ctrl+V**: Paste text
- **Ctrl+Z**: Undo in text fields

### Application Shortcuts
- **Ctrl+R**: Reset/Clear all fields
- **Ctrl+E**: Run Examples (Test Suite)
- **Ctrl+Q**: Quit application

## Quick Reference

### Operator Quick Guide
```
&, &&, AND          # Both terms required
|, ||, OR           # Either term acceptable  
!, ~, NOT           # Exclude this term
^, XOR              # Exactly one term
(), [], {}          # Grouping (all equivalent)
```

### Complexity Levels
```
Level 1: A                      # Simple
Level 2: A & B                  # Basic  
Level 3: A & (B | C)            # Medium
Level 4: (A & B) | (C & D)      # Advanced
Level 5: ((A | B) & C) | (D & E) # Expert
```

### File Types
```
Common: .txt, .md, .py, .js, .html, .css, .json
Custom: Enter comma-separated: .log,.cfg,.ini
All: Leave file types empty to search all files
```

### Search Modes
```
Line Mode:     Search line by line (default)
Document Mode: Search entire documents
Unique Mode:   Show only first occurrences  
Case Mode:     Match exact case when checked
```

---

## Getting Help

- **Run Examples**: Click "Run Examples" for learning examples
- **Tool Tips**: Hover over buttons for quick help
- **Formula Validation**: On-demand validation with ✓ Validate Formula button
- **Error Messages**: Detailed error explanations with specific suggestions
- **Validation Workflow**: Check formula before searching or validate on search

For additional support, refer to the Educational Test Suite for hands-on learning examples!

---

*This guide covers all features of the Finder application. For technical details, see the project documentation files.*