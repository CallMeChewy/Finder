# File: Finder.py
# Path: /home/herb/Desktop/Finder/Finder.py
# Standard: AIDEV-PascalCase-2.1
# Created: 2025-07-18
# Last Modified: 2025-07-18  13:50PM
"""
Finder - Advanced Document Search Application
A comprehensive PySide6-based search tool with logical formula construction,
phrase-based searching, and advanced result display with color coding.
"""

import sys
import os
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Set, Tuple, Optional

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QCheckBox, QRadioButton, QLineEdit, QPushButton,
    QTextEdit, QFileDialog, QButtonGroup, QLabel, QScrollArea,
    QGridLayout, QFrame, QSplitter, QComboBox, QMessageBox
)
from PySide6.QtCore import QThread, QObject, Signal, Qt, QTimer
from PySide6.QtGui import QFont, QTextCharFormat, QColor, QSyntaxHighlighter, QTextDocument


class FormulaHighlighter(QSyntaxHighlighter):
    """Syntax highlighter for formula input with parentheses/bracket matching and error highlighting"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_formats()
        self.finder_app = None  # Will be set by parent
        
    def setup_formats(self):
        """Setup text formats for different elements"""
        self.formats = {}
        
        # Parentheses colors (cycling through colors for nesting)
        self.paren_colors = [
            QColor(255, 100, 100),  # Red
            QColor(100, 255, 100),  # Green
            QColor(100, 100, 255),  # Blue
            QColor(255, 255, 100),  # Yellow
            QColor(255, 100, 255),  # Magenta
            QColor(100, 255, 255),  # Cyan
        ]
        
        # Operators
        self.operator_format = QTextCharFormat()
        self.operator_format.setForeground(QColor(200, 100, 50))
        self.operator_format.setFontWeight(QFont.Weight.Bold)
        
        # Phrase references (A-F)
        self.phrase_format = QTextCharFormat()
        self.phrase_format.setForeground(QColor(50, 150, 200))
        self.phrase_format.setFontWeight(QFont.Weight.Bold)
        
        # Error highlighting
        self.error_format = QTextCharFormat()
        self.error_format.setForeground(QColor(255, 255, 255))
        self.error_format.setBackground(QColor(255, 100, 100))
        self.error_format.setFontWeight(QFont.Weight.Bold)
        
        # Invalid characters
        self.invalid_format = QTextCharFormat()
        self.invalid_format.setForeground(QColor(255, 0, 0))
        self.invalid_format.setBackground(QColor(255, 255, 100))
        self.invalid_format.setFontWeight(QFont.Weight.Bold)
        
    def highlightBlock(self, text):
        """Highlight the current text block with error detection"""
        # First, check for invalid characters (now including common operators)
        valid_chars = set('ABCDEF()[]{}ANDORNOTXRandornotxr \t&|!~^')
        for i, char in enumerate(text):
            if char not in valid_chars:
                self.setFormat(i, 1, self.invalid_format)
        
        # Highlight word-based operators
        word_operators = r'\b(AND|OR|NOT|NOR|XOR|XNOR)\b'
        for match in re.finditer(word_operators, text, re.IGNORECASE):
            self.setFormat(match.start(), match.end() - match.start(), self.operator_format)
            
        # Highlight symbol-based operators
        symbol_operators = r'[&|!~^]+'
        for match in re.finditer(symbol_operators, text):
            self.setFormat(match.start(), match.end() - match.start(), self.operator_format)
        
        # Highlight phrase references
        phrases = r'\b[A-F]\b'
        for match in re.finditer(phrases, text):
            self.setFormat(match.start(), match.end() - match.start(), self.phrase_format)
            
        # Highlight parentheses with color matching and error detection
        paren_stack = []
        for i, char in enumerate(text):
            if char in '([{':
                level = len(paren_stack) % len(self.paren_colors)
                color = self.paren_colors[level]
                format = QTextCharFormat()
                format.setForeground(color)
                format.setFontWeight(QFont.Weight.Bold)
                self.setFormat(i, 1, format)
                paren_stack.append((char, level))
            elif char in ')]}':
                if paren_stack:
                    open_char, level = paren_stack.pop()
                    if self._is_matching_paren(open_char, char):
                        color = self.paren_colors[level]
                        format = QTextCharFormat()
                        format.setForeground(color)
                        format.setFontWeight(QFont.Weight.Bold)
                        self.setFormat(i, 1, format)
                    else:
                        # Mismatched parenthesis - highlight as error
                        self.setFormat(i, 1, self.error_format)
                else:
                    # Unmatched closing parenthesis - highlight as error
                    self.setFormat(i, 1, self.error_format)
        
        # Highlight any remaining unmatched opening parentheses
        for open_char, level in paren_stack:
            # Find the position of unmatched opening parenthesis
            for i, char in enumerate(text):
                if char == open_char:
                    # Check if this is actually unmatched (simple check)
                    self.setFormat(i, 1, self.error_format)
                    break
                    
    def _is_matching_paren(self, open_char, close_char):
        """Check if parentheses match"""
        pairs = {'(': ')', '[': ']', '{': '}'}
        return pairs.get(open_char) == close_char


class SearchWorker(QObject):
    """Worker thread for performing document search operations"""
    
    result_found = Signal(str, str, int, bool)  # file_path, content, line_number, is_unique
    search_finished = Signal(str)
    progress_update = Signal(int, int)  # current, total
    
    def __init__(self, search_params):
        super().__init__()
        self.search_params = search_params
        self.is_cancelled = False
        self.unique_matches = {}  # Track unique matches per file
        
    def run_search(self):
        """Execute the search operation"""
        try:
            files_to_search = self._get_files_to_search()
            total_files = len(files_to_search)
            
            if total_files == 0:
                self.search_finished.emit("No files found matching the criteria.")
                return
                
            match_count = 0
            
            for i, file_path in enumerate(files_to_search):
                if self.is_cancelled:
                    break
                    
                self.progress_update.emit(i + 1, total_files)
                
                try:
                    matches = self._search_file(file_path)
                    for match in matches:
                        if self.is_cancelled:
                            break
                        match_count += 1
                        line_content, line_number, is_unique = match
                        self.result_found.emit(file_path, line_content, line_number, is_unique)
                        
                except Exception as e:
                    self.result_found.emit(file_path, f"ERROR: Cannot read file: {e}", 0, False)
                    
            self.search_finished.emit(f"Search complete. Found {match_count} matches in {total_files} files.")
            
        except Exception as e:
            self.search_finished.emit(f"Search error: {e}")
            
    def _get_files_to_search(self):
        """Get list of files to search based on parameters"""
        files = []
        search_paths = self.search_params['search_paths']
        file_extensions = self.search_params['file_extensions']
        
        for search_path in search_paths:
            if os.path.isfile(search_path):
                if self._is_valid_extension(search_path, file_extensions):
                    files.append(search_path)
            elif os.path.isdir(search_path):
                for root, _, filenames in os.walk(search_path):
                    for filename in filenames:
                        if self._is_valid_extension(filename, file_extensions):
                            files.append(os.path.join(root, filename))
                            
        return files
        
    def _is_valid_extension(self, filename, extensions):
        """Check if file extension matches search criteria"""
        if not extensions:
            return True
        return any(filename.lower().endswith(ext.lower()) for ext in extensions)
        
    def _search_file(self, file_path):
        """Search a single file for matches"""
        matches = []
        phrases = self.search_params['phrases']
        search_mode = self.search_params['search_mode']
        formula = self.search_params['formula']
        unique_mode = self.search_params['unique_mode']
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                if search_mode == 'document':
                    # Search entire document
                    content = f.read()
                    if self._evaluate_formula(content, phrases, formula):
                        is_unique = file_path not in self.unique_matches
                        if is_unique:
                            self.unique_matches[file_path] = True
                        if not unique_mode or is_unique:
                            matches.append((content[:200] + "...", 0, is_unique))
                else:
                    # Search line by line
                    for line_num, line in enumerate(f, 1):
                        if self._evaluate_formula(line, phrases, formula):
                            # Check if this is a unique match for this line content
                            match_key = f"{file_path}:{line.strip()}"
                            is_unique = match_key not in self.unique_matches
                            if is_unique:
                                self.unique_matches[match_key] = True
                            if not unique_mode or is_unique:
                                matches.append((line.strip(), line_num, is_unique))
                                
        except Exception as e:
            matches.append((f"Error reading file: {e}", 0, False))
            
        return matches
        
    def _evaluate_formula(self, content, phrases, formula):
        """Evaluate the logical formula against the content"""
        if not formula.strip():
            return False
            
        # Normalize operators first
        normalized_formula = self._normalize_operators(formula)
            
        # Create a mapping of phrase variables to their presence in content
        phrase_values = {}
        for letter, phrase_data in phrases.items():
            phrase_text = phrase_data.get('text', '')
            case_sensitive = phrase_data.get('case_sensitive', False)
            
            if phrase_text.strip():
                if case_sensitive:
                    # Case-sensitive search
                    phrase_values[letter] = phrase_text in content
                else:
                    # Case-insensitive search
                    phrase_values[letter] = phrase_text.lower() in content.lower()
            else:
                phrase_values[letter] = False
                
        # Replace phrase variables in formula with their boolean values
        eval_formula = normalized_formula.upper()
        for letter in 'ABCDEF':
            eval_formula = eval_formula.replace(letter, str(phrase_values.get(letter, False)))
            
        # Replace logical operators with Python equivalents
        eval_formula = eval_formula.replace('AND', ' and ')
        eval_formula = eval_formula.replace('OR', ' or ')
        eval_formula = eval_formula.replace('NOT', ' not ')
        eval_formula = eval_formula.replace('NOR', ' not (') # Will need special handling
        eval_formula = eval_formula.replace('XOR', ' != ')
        eval_formula = eval_formula.replace('XNOR', ' == ')
        
        # Handle NOR specially - convert "A NOR B" to "not (A or B)"
        eval_formula = re.sub(r'not \(([^)]+)\)', r'not (\1)', eval_formula)
        
        try:
            return eval(eval_formula)
        except:
            return False
            
    def cancel(self):
        """Cancel the search operation"""
        self.is_cancelled = True


class Finder(QMainWindow):
    """Main Finder application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Finder - Advanced Document Search")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize search thread components
        self.search_thread = None
        self.search_worker = None
        
        # Initialize auto-formula tracking
        self._last_auto_formula = ""
        
        # Setup UI
        self._setup_ui()
        self._setup_defaults()
        self._setup_tab_order()
        
    def _setup_ui(self):
        """Setup the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout using splitter
        main_layout = QVBoxLayout(central_widget)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel for controls
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Create control sections
        self._create_phrase_section(left_layout)
        self._create_search_mode_section(left_layout)
        self._create_file_types_section(left_layout)
        self._create_path_section(left_layout)
        self._create_formula_section(left_layout)
        self._create_control_buttons(left_layout)
        
        # Right panel for results
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        self._create_results_section(right_layout)
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([400, 800])
        
        main_layout.addWidget(splitter)
        
    def _create_phrase_section(self, parent_layout):
        """Create the phrase input section (A-F)"""
        group_box = QGroupBox("Search Phrases (A-F)")
        layout = QVBoxLayout()
        
        self.phrase_inputs = {}
        self.case_sensitive_checkboxes = {}
        
        for letter in 'ABCDEF':
            h_layout = QHBoxLayout()
            
            label = QLabel(f"{letter}:")
            label.setMinimumWidth(20)
            label.setMaximumWidth(20)
            
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(f"Enter phrase {letter}")
            
            case_checkbox = QCheckBox("Match Case")
            case_checkbox.setToolTip("Check to make this phrase case-sensitive")
            case_checkbox.setChecked(False)  # Default to case-insensitive
            
            h_layout.addWidget(label)
            h_layout.addWidget(line_edit)
            h_layout.addWidget(case_checkbox)
            
            self.phrase_inputs[letter] = line_edit
            self.case_sensitive_checkboxes[letter] = case_checkbox
            
            # Connect to auto-formula construction (no real-time validation)
            line_edit.textChanged.connect(self._update_auto_formula)
            
            layout.addLayout(h_layout)
            
        group_box.setLayout(layout)
        parent_layout.addWidget(group_box)
        
    def _create_search_mode_section(self, parent_layout):
        """Create search mode selection (Document/Line)"""
        group_box = QGroupBox("Search Mode")
        layout = QHBoxLayout()
        
        self.search_mode_group = QButtonGroup()
        
        self.rb_document = QRadioButton("Document")
        self.rb_document.setToolTip("Search entire document as one unit")
        
        self.rb_line = QRadioButton("Line") 
        self.rb_line.setToolTip("Search line by line")
        self.rb_line.setChecked(True)
        
        self.search_mode_group.addButton(self.rb_document)
        self.search_mode_group.addButton(self.rb_line)
        
        layout.addWidget(self.rb_document)
        layout.addWidget(self.rb_line)
        layout.addStretch()
        
        group_box.setLayout(layout)
        parent_layout.addWidget(group_box)
        
    def _create_file_types_section(self, parent_layout):
        """Create file type selection checkboxes"""
        group_box = QGroupBox("File Types")
        layout = QVBoxLayout()
        
        # Standard file types
        types_layout = QGridLayout()
        
        self.file_type_checkboxes = {}
        file_types = ['txt', 'md', 'html', 'css', 'json', 'js', 'py', 'xml', 'log', 'csv']
        
        for i, file_type in enumerate(file_types):
            cb = QCheckBox(f".{file_type}")
            if file_type in ['txt', 'md']:  # Default selections
                cb.setChecked(True)
            self.file_type_checkboxes[file_type] = cb
            types_layout.addWidget(cb, i // 3, i % 3)
            
        layout.addLayout(types_layout)
        
        # Custom extensions
        custom_layout = QHBoxLayout()
        custom_layout.addWidget(QLabel("Custom:"))
        
        self.custom_extensions = QLineEdit()
        self.custom_extensions.setPlaceholderText("e.g., aaa,bbb,ccc")
        custom_layout.addWidget(self.custom_extensions)
        
        layout.addLayout(custom_layout)
        
        group_box.setLayout(layout)
        parent_layout.addWidget(group_box)
        
    def _create_path_section(self, parent_layout):
        """Create path selection section"""
        group_box = QGroupBox("Search Path")
        layout = QVBoxLayout()
        
        # Current path display
        self.path_display = QLineEdit()
        self.path_display.setReadOnly(True)
        self.path_display.setPlaceholderText("No path selected")
        layout.addWidget(self.path_display)
        
        # Path selection buttons
        button_layout = QHBoxLayout()
        
        self.btn_select_folder = QPushButton("Select Folder")
        self.btn_select_folder.clicked.connect(self._select_folder)
        
        self.btn_select_files = QPushButton("Select Files")
        self.btn_select_files.clicked.connect(self._select_files)
        
        self.btn_current_folder = QPushButton("Current Folder")
        self.btn_current_folder.clicked.connect(self._use_current_folder)
        
        button_layout.addWidget(self.btn_select_folder)
        button_layout.addWidget(self.btn_select_files)
        button_layout.addWidget(self.btn_current_folder)
        
        layout.addLayout(button_layout)
        
        # Store selected paths
        self.selected_paths = []
        
        group_box.setLayout(layout)
        parent_layout.addWidget(group_box)
        
    def _create_formula_section(self, parent_layout):
        """Create formula construction section"""
        group_box = QGroupBox("Search Formula")
        layout = QVBoxLayout()
        
        # Formula input with syntax highlighting
        self.formula_input = QTextEdit()
        self.formula_input.setMaximumHeight(100)
        self.formula_input.setPlaceholderText("Enter formula using A-F, AND/&, OR/|, NOT/!, NOR, XOR/^, XNOR, (, ), [, ], {, } or leave empty for auto-construction")
        
        # Setup syntax highlighter
        self.highlighter = FormulaHighlighter(self.formula_input.document())
        self.highlighter.finder_app = self
        
        layout.addWidget(self.formula_input)
        
        # Unique mode checkbox
        self.cb_unique = QCheckBox("Unique (show only first occurrence)")
        layout.addWidget(self.cb_unique)
        
        # Syntax validation label
        self.syntax_label = QLabel("Syntax: OK")
        self.syntax_label.setStyleSheet("color: green;")
        layout.addWidget(self.syntax_label)
        
        # Connect formula input to validation
        # Remove real-time validation - only validate on button press
        # self.formula_input.textChanged.connect(self._validate_formula)
        
        # Add search and validate buttons directly below formula
        formula_button_layout = QHBoxLayout()
        
        self.btn_search = QPushButton("🔍 Start Search")
        self.btn_search.clicked.connect(self._start_search)
        self.btn_search.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; }")
        self.btn_search.setToolTip("Start searching with current parameters")
        
        self.btn_validate = QPushButton("✓ Validate Formula")
        self.btn_validate.clicked.connect(self._validate_formula_on_demand)
        self.btn_validate.setStyleSheet("QPushButton { background-color: #FF9800; color: white; font-weight: bold; }")
        self.btn_validate.setToolTip("Check formula for errors and warnings")
        
        formula_button_layout.addWidget(self.btn_search)
        formula_button_layout.addWidget(self.btn_validate)
        layout.addLayout(formula_button_layout)
        
        group_box.setLayout(layout)
        parent_layout.addWidget(group_box)
        
    def _create_control_buttons(self, parent_layout):
        """Create control buttons (reset and examples)"""
        button_layout = QHBoxLayout()
        
        self.btn_reset = QPushButton("🔄 Reset/Clear")
        self.btn_reset.clicked.connect(self._reset_form)
        self.btn_reset.setToolTip("Clear all fields and reset to defaults")
        
        self.btn_test_suite = QPushButton("🎓 Run Examples")
        self.btn_test_suite.clicked.connect(self._run_test_suite)
        self.btn_test_suite.setStyleSheet("QPushButton { background-color: #2196F3; color: white; font-weight: bold; }")
        self.btn_test_suite.setToolTip("Run educational test suite with 5 example formulas")
        
        button_layout.addWidget(self.btn_reset)
        button_layout.addWidget(self.btn_test_suite)
        
        parent_layout.addLayout(button_layout)
        
    def _create_results_section(self, parent_layout):
        """Create results display section"""
        group_box = QGroupBox("Search Results")
        layout = QVBoxLayout()
        
        # Results display
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        self.results_display.setFont(QFont("Courier", 10))
        
        layout.addWidget(self.results_display)
        
        group_box.setLayout(layout)
        parent_layout.addWidget(group_box)
        
    def _setup_defaults(self):
        """Setup default values"""
        self.rb_line.setChecked(True)
        self.file_type_checkboxes['txt'].setChecked(True)
        self.file_type_checkboxes['md'].setChecked(True)
        self.cb_unique.setChecked(False)
        self._use_current_folder()
        
    def _setup_tab_order(self):
        """Setup tab order for better navigation"""
        # Create tab order list
        tab_widgets = []
        
        # Add phrase inputs and case checkboxes
        for letter in 'ABCDEF':
            tab_widgets.append(self.phrase_inputs[letter])
            tab_widgets.append(self.case_sensitive_checkboxes[letter])
            
        # Add search mode radio buttons
        tab_widgets.extend([self.rb_document, self.rb_line])
        
        # Add file type checkboxes
        for cb in self.file_type_checkboxes.values():
            tab_widgets.append(cb)
        tab_widgets.append(self.custom_extensions)
        
        # Add path selection buttons
        tab_widgets.extend([self.btn_select_folder, self.btn_select_files, self.btn_current_folder])
        
        # Add formula input and unique checkbox
        tab_widgets.extend([self.formula_input, self.cb_unique])
        
        # Add control buttons
        tab_widgets.extend([self.btn_search, self.btn_validate, self.btn_reset, self.btn_test_suite])
        
        # Set tab order
        for i in range(len(tab_widgets) - 1):
            self.setTabOrder(tab_widgets[i], tab_widgets[i + 1])
            
    def _select_folder(self):
        """Select a folder for searching"""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.selected_paths = [folder]
            self.path_display.setText(folder)
            
    def _select_files(self):
        """Select multiple files for searching"""
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files")
        if files:
            self.selected_paths = files
            if len(files) == 1:
                self.path_display.setText(files[0])
            else:
                self.path_display.setText(f"{len(files)} files selected")
                
    def _use_current_folder(self):
        """Use current working directory"""
        current_dir = os.getcwd()
        self.selected_paths = [current_dir]
        self.path_display.setText(current_dir)
        
    def _validate_formula(self):
        """Validate the formula syntax with detailed error reporting"""
        formula = self.formula_input.toPlainText().strip()
        
        if not formula:
            self.syntax_label.setText("Syntax: OK")
            self.syntax_label.setStyleSheet("color: green;")
            return True
            
        # Comprehensive validation with detailed error reporting
        validation_result = self._comprehensive_formula_validation(formula)
        
        if validation_result['is_valid']:
            if validation_result['warnings']:
                self.syntax_label.setText("Syntax: WARNING - See details")
                self.syntax_label.setStyleSheet("color: orange;")
                self._show_validation_dialog("Formula Warnings", validation_result['warnings'], is_error=False)
            else:
                self.syntax_label.setText("Syntax: OK")
                self.syntax_label.setStyleSheet("color: green;")
            return True
        else:
            self.syntax_label.setText("Syntax: ERROR - See details")
            self.syntax_label.setStyleSheet("color: red;")
            self._show_validation_dialog("Formula Errors", validation_result['errors'], is_error=True)
            return False
        
    def _validate_formula_on_demand(self):
        """Validate formula only when button is pressed - no real-time validation"""
        formula = self.formula_input.toPlainText().strip()
        
        if not formula:
            QMessageBox.information(
                self, 
                "Formula Validation", 
                "No formula to validate.\n\nEnter a formula in the 'Search Formula' field and try again."
            )
            return
            
        # Run comprehensive validation
        validation_result = self._comprehensive_formula_validation(formula)
        
        if validation_result['is_valid']:
            if validation_result['warnings']:
                self.syntax_label.setText("Syntax: WARNING")
                self.syntax_label.setStyleSheet("color: orange;")
                warnings_text = "\n".join([f"• {w}" for w in validation_result['warnings']])
                QMessageBox.warning(
                    self,
                    "Formula Validation - Warnings",
                    f"Formula is valid but has warnings:\n\n{warnings_text}\n\nYou can still search with this formula."
                )
            else:
                self.syntax_label.setText("Syntax: OK")
                self.syntax_label.setStyleSheet("color: green;")
                QMessageBox.information(
                    self,
                    "Formula Validation - Success",
                    "✅ Formula is valid!\n\nNo errors or warnings found. Ready to search."
                )
        else:
            self.syntax_label.setText("Syntax: ERROR")
            self.syntax_label.setStyleSheet("color: red;")
            errors_text = "\n".join([f"• {e}" for e in validation_result['errors']])
            QMessageBox.critical(
                self,
                "Formula Validation - Errors",
                f"❌ Formula has errors:\n\n{errors_text}\n\nPlease fix these errors before searching."
            )
        
    def _comprehensive_formula_validation(self, formula):
        """Comprehensive formula validation with detailed error reporting"""
        errors = []
        warnings = []
        
        # Check for balanced parentheses with detailed reporting
        paren_result = self._check_balanced_parentheses_detailed(formula)
        if paren_result['errors']:
            errors.extend(paren_result['errors'])
            
        # Check for valid tokens with detailed reporting
        token_result = self._check_valid_tokens_detailed(formula)
        if token_result['errors']:
            errors.extend(token_result['errors'])
            
        # Check for logical structure issues
        structure_result = self._check_logical_structure(formula)
        if structure_result['errors']:
            errors.extend(structure_result['errors'])
        if structure_result['warnings']:
            warnings.extend(structure_result['warnings'])
            
        # Check for logical paradoxes with detailed reporting
        paradox_result = self._check_paradoxes_detailed(formula)
        if paradox_result['warnings']:
            warnings.extend(paradox_result['warnings'])
            
        # Check for impossible conditions
        impossible_result = self._check_impossible_conditions(formula)
        if impossible_result['errors']:
            errors.extend(impossible_result['errors'])
        if impossible_result['warnings']:
            warnings.extend(impossible_result['warnings'])
            
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
        
    def _check_balanced_parentheses_detailed(self, formula):
        """Check parentheses balance with detailed error reporting"""
        errors = []
        stack = []
        pairs = {'(': ')', '[': ']', '{': '}'}
        
        for i, char in enumerate(formula):
            if char in pairs:
                stack.append((char, i))
            elif char in pairs.values():
                if not stack:
                    errors.append(f"Unmatched closing '{char}' at position {i+1}")
                else:
                    open_char, open_pos = stack.pop()
                    if pairs[open_char] != char:
                        errors.append(f"Mismatched parentheses: '{open_char}' at position {open_pos+1} closed by '{char}' at position {i+1}")
                        
        # Check for unclosed parentheses
        for open_char, pos in stack:
            errors.append(f"Unclosed '{open_char}' at position {pos+1}")
            
        return {'errors': errors}
        
    def _check_balanced_parentheses(self, formula):
        """Check if parentheses are balanced (legacy method)"""
        result = self._check_balanced_parentheses_detailed(formula)
        return len(result['errors']) == 0
        
    def _check_valid_tokens_detailed(self, formula):
        """Check tokens with detailed error reporting"""
        errors = []
        
        # Normalize formula by converting common operators to standard form
        normalized_formula = self._normalize_operators(formula)
        
        # Remove spaces and convert to upper case for analysis
        clean_formula = normalized_formula.upper().replace(' ', '')
        
        # Check for invalid characters (now including common operators)
        valid_chars = set('ABCDEF()[]{}ANDORNOTXR&|!~^')
        invalid_chars = set(clean_formula) - valid_chars
        if invalid_chars:
            errors.append(f"Invalid characters found: {', '.join(sorted(invalid_chars))}")
            
        # Extract tokens (including symbol operators)
        tokens = re.findall(r'[A-F]|AND|OR|NOT|NOR|XOR|XNOR|&&?|\|\|?|!|~|\^|[()[\]{}]', clean_formula)
        
        if not tokens:
            errors.append("No valid tokens found in formula")
            return {'errors': errors}
            
        # Check for invalid token sequences
        for i in range(len(tokens) - 1):
            current = tokens[i]
            next_token = tokens[i + 1]
            
            # Two variables in a row
            if current in 'ABCDEF' and next_token in 'ABCDEF':
                errors.append(f"Invalid sequence: '{current} {next_token}' - missing operator between variables")
                
            # Two binary operators in a row
            if current in ['AND', 'OR', 'NOR', 'XOR', 'XNOR'] and next_token in ['AND', 'OR', 'NOR', 'XOR', 'XNOR']:
                errors.append(f"Invalid sequence: '{current} {next_token}' - consecutive operators")
                
        return {'errors': errors}
        
    def _check_logical_structure(self, formula):
        """Check logical structure of the formula"""
        errors = []
        warnings = []
        
        # Normalize operators first
        normalized_formula = self._normalize_operators(formula)
        tokens = re.findall(r'[A-F]|AND|OR|NOT|NOR|XOR|XNOR|[()[\]{}]', normalized_formula.upper())
        
        if not tokens:
            return {'errors': errors, 'warnings': warnings}
            
        # Check for operators without operands
        binary_ops = ['AND', 'OR', 'NOR', 'XOR', 'XNOR']
        
        for i, token in enumerate(tokens):
            if token in binary_ops:
                # Check if there's a valid operand before and after
                if i == 0:
                    errors.append(f"'{token}' operator at start of formula needs left operand")
                elif i == len(tokens) - 1:
                    errors.append(f"'{token}' operator at end of formula needs right operand")
                else:
                    # Check left operand
                    left_token = tokens[i-1]
                    if left_token in binary_ops or left_token == 'NOT':
                        errors.append(f"'{token}' operator missing valid left operand")
                    
                    # Check right operand
                    right_token = tokens[i+1]
                    if right_token in binary_ops:
                        errors.append(f"'{token}' operator missing valid right operand")
                        
            elif token == 'NOT':
                # Check if NOT has a valid operand
                if i == len(tokens) - 1:
                    errors.append("'NOT' operator at end of formula needs operand")
                else:
                    next_token = tokens[i+1]
                    if next_token in binary_ops:
                        errors.append("'NOT' operator missing valid operand")
                        
        return {'errors': errors, 'warnings': warnings}
        
    def _check_paradoxes_detailed(self, formula):
        """Check for logical paradoxes with detailed reporting"""
        warnings = []
        
        # Check for obvious contradictions like "A AND NOT A"
        for letter in 'ABCDEF':
            # Pattern: A AND NOT A
            pattern1 = f'{letter} AND NOT {letter}'
            pattern2 = f'NOT {letter} AND {letter}'
            
            if pattern1 in formula.upper() or pattern2 in formula.upper():
                warnings.append(f"Logical paradox detected: '{letter} AND NOT {letter}' - this will always be false")
                
        # Check for tautologies like "A OR NOT A"
        for letter in 'ABCDEF':
            pattern1 = f'{letter} OR NOT {letter}'
            pattern2 = f'NOT {letter} OR {letter}'
            
            if pattern1 in formula.upper() or pattern2 in formula.upper():
                warnings.append(f"Tautology detected: '{letter} OR NOT {letter}' - this will always be true")
                
        return {'warnings': warnings}
        
    def _check_impossible_conditions(self, formula):
        """Check for impossible logical conditions"""
        errors = []
        warnings = []
        
        # Check for empty parentheses
        if '()' in formula or '[]' in formula or '{}' in formula:
            errors.append("Empty parentheses/brackets found - they must contain expressions")
            
        # Check for variables that don't have corresponding phrases
        used_vars = set(re.findall(r'[A-F]', formula.upper()))
        empty_vars = []
        
        for var in used_vars:
            if var in self.phrase_inputs:
                if not self.phrase_inputs[var].text().strip():
                    empty_vars.append(var)
                    
        if empty_vars:
            warnings.append(f"Variables {', '.join(empty_vars)} are used in formula but have no corresponding phrases")
            
        return {'errors': errors, 'warnings': warnings}
        
    def _normalize_operators(self, formula):
        """Convert common logical operators to standard form"""
        # Create a mapping of common operators to standard forms
        operator_map = {
            '&': ' AND ',
            '&&': ' AND ',
            '|': ' OR ',
            '||': ' OR ',
            '!': ' NOT ',
            '~': ' NOT ',
            '^': ' XOR '
        }
        
        # Apply replacements
        normalized = formula
        for symbol, replacement in operator_map.items():
            normalized = normalized.replace(symbol, replacement)
            
        return normalized
        
    def _auto_construct_formula(self):
        """Automatically construct formula from non-empty variables"""
        active_vars = []
        
        # Find all variables with non-empty phrases
        for letter in 'ABCDEF':
            if self.phrase_inputs[letter].text().strip():
                active_vars.append(letter)
                
        if not active_vars:
            return ""
        elif len(active_vars) == 1:
            return active_vars[0]
        else:
            # Join with AND operator
            return " AND ".join(active_vars)
            
    def _update_auto_formula(self):
        """Update formula automatically if user hasn't entered one"""
        current_formula = self.formula_input.toPlainText().strip()
        
        # Only auto-construct if formula is empty or was previously auto-constructed
        if not current_formula or hasattr(self, '_last_auto_formula') and current_formula == self._last_auto_formula:
            auto_formula = self._auto_construct_formula()
            if auto_formula:
                self.formula_input.setPlainText(auto_formula)
                self._last_auto_formula = auto_formula
            elif current_formula:
                self.formula_input.clear()
                self._last_auto_formula = ""
        
    def _show_validation_dialog(self, title, messages, is_error=True):
        """Show validation dialog with detailed error/warning information"""
        dialog = QMessageBox()
        dialog.setWindowTitle(title)
        
        if is_error:
            dialog.setIcon(QMessageBox.Icon.Critical)
        else:
            dialog.setIcon(QMessageBox.Icon.Warning)
            
        # Format messages for display
        formatted_messages = []
        for i, msg in enumerate(messages, 1):
            formatted_messages.append(f"{i}. {msg}")
            
        dialog.setText("\n".join(formatted_messages))
        dialog.setDetailedText("Formula validation found the following issues:\n\n" + "\n".join(formatted_messages))
        
        if is_error:
            dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        else:
            dialog.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Ignore)
            
        dialog.exec()
        
    def _check_valid_tokens(self, formula):
        """Check if all tokens in formula are valid (legacy method)"""
        result = self._check_valid_tokens_detailed(formula)
        return len(result['errors']) == 0
        
    def _check_paradoxes(self, formula):
        """Basic check for logical paradoxes (legacy method)"""
        result = self._check_paradoxes_detailed(formula)
        return len(result['warnings']) > 0
        
    def _start_search(self):
        """Start the search operation"""
        if not self._validate_search_parameters():
            return
            
        # Stop any existing search
        if self.search_thread and self.search_thread.isRunning():
            self.search_worker.cancel()
            self.search_thread.quit()
            self.search_thread.wait()
            
        # Clear results
        self.results_display.clear()
        
        # Prepare search parameters
        search_params = self._prepare_search_parameters()
        
        # Start search
        self.search_thread = QThread()
        self.search_worker = SearchWorker(search_params)
        self.search_worker.moveToThread(self.search_thread)
        
        # Connect signals
        self.search_thread.started.connect(self.search_worker.run_search)
        self.search_worker.result_found.connect(self._display_result)
        self.search_worker.search_finished.connect(self._search_finished)
        self.search_worker.progress_update.connect(self._update_progress)
        
        # Update UI
        self.btn_search.setText("🔍 Searching...")
        self.btn_search.setEnabled(False)
        
        # Start the thread
        self.search_thread.start()
        
    def _validate_search_parameters(self):
        """Validate search parameters before starting"""
        # Check if formula is valid (show error dialog during search)
        formula = self.formula_input.toPlainText().strip()
        if formula:  # Only validate if there's a formula
            validation_result = self._comprehensive_formula_validation(formula)
            if not validation_result['is_valid']:
                errors_text = "\n".join([f"• {e}" for e in validation_result['errors']])
                QMessageBox.critical(
                    self,
                    "Search Error - Invalid Formula",
                    f"❌ Cannot search with invalid formula:\n\n{errors_text}\n\nUse 'Validate Formula' button to check your formula first."
                )
                return False
            
        # Check if any phrases are entered
        has_phrases = any(self.phrase_inputs[letter].text().strip() for letter in 'ABCDEF')
        if not has_phrases:
            QMessageBox.warning(self, "No Phrases", "Please enter at least one search phrase.")
            return False
            
        # Check if any file types are selected
        has_file_types = any(cb.isChecked() for cb in self.file_type_checkboxes.values())
        has_custom = self.custom_extensions.text().strip()
        
        if not has_file_types and not has_custom:
            QMessageBox.warning(self, "No File Types", "Please select at least one file type.")
            return False
            
        # Check if search path is selected
        if not self.selected_paths:
            QMessageBox.warning(self, "No Search Path", "Please select a search path.")
            return False
            
        return True
        
    def _prepare_search_parameters(self):
        """Prepare search parameters for the worker"""
        # Get phrases with case sensitivity settings
        phrases = {}
        for letter in 'ABCDEF':
            phrases[letter] = {
                'text': self.phrase_inputs[letter].text().strip(),
                'case_sensitive': self.case_sensitive_checkboxes[letter].isChecked()
            }
            
        # Get file extensions
        extensions = []
        for file_type, cb in self.file_type_checkboxes.items():
            if cb.isChecked():
                extensions.append(f".{file_type}")
                
        # Add custom extensions
        custom_ext = self.custom_extensions.text().strip()
        if custom_ext:
            for ext in custom_ext.split(','):
                ext = ext.strip()
                if ext and not ext.startswith('.'):
                    ext = '.' + ext
                if ext:
                    extensions.append(ext)
                    
        return {
            'phrases': phrases,
            'search_mode': 'document' if self.rb_document.isChecked() else 'line',
            'file_extensions': extensions,
            'search_paths': self.selected_paths,
            'formula': self.formula_input.toPlainText().strip(),
            'unique_mode': self.cb_unique.isChecked()
        }
        
    def _display_result(self, file_path, content, line_number, is_unique):
        """Display a search result"""
        # Convert absolute path to relative if possible
        try:
            rel_path = os.path.relpath(file_path)
            if len(rel_path) < len(file_path):
                display_path = rel_path
            else:
                display_path = file_path
        except:
            display_path = file_path
            
        # File path in light blue
        self.results_display.setTextColor(QColor(173, 216, 230))  # Light blue
        self.results_display.append(display_path)
        
        # Content with line number
        if line_number > 0:
            # Line number in red if unique, white if not
            line_color = QColor(255, 100, 100) if is_unique else QColor(255, 255, 255)
            content_color = QColor(255, 255, 255)  # White
            
            self.results_display.setTextColor(line_color)
            self.results_display.insertPlainText(f"{line_number}: ")
            
            self.results_display.setTextColor(content_color)
            self.results_display.insertPlainText(content)
            self.results_display.append("")  # New line
        else:
            # Document match
            self.results_display.setTextColor(QColor(255, 255, 255))
            self.results_display.append(content)
            
        self.results_display.append("")  # Extra line for spacing
        
    def _search_finished(self, message):
        """Handle search completion"""
        self.results_display.setTextColor(QColor(100, 255, 100))  # Light green
        self.results_display.append(f"\n{message}")
        
        # Reset button state
        self.btn_search.setText("🔍 Start Search")
        self.btn_search.setEnabled(True)
        
        # Clean up thread
        if self.search_thread:
            self.search_thread.quit()
            self.search_thread.wait()
            
    def _update_progress(self, current, total):
        """Update search progress"""
        self.btn_search.setText(f"🔍 Searching... ({current}/{total})")
        
    def _reset_form(self):
        """Reset/clear the form"""
        # Clear phrases and reset case sensitivity
        for line_edit in self.phrase_inputs.values():
            line_edit.clear()
        for checkbox in self.case_sensitive_checkboxes.values():
            checkbox.setChecked(False)
            
        # Reset search mode
        self.rb_line.setChecked(True)
        
        # Reset file types to defaults
        for cb in self.file_type_checkboxes.values():
            cb.setChecked(False)
        self.file_type_checkboxes['txt'].setChecked(True)
        self.file_type_checkboxes['md'].setChecked(True)
        
        # Clear custom extensions
        self.custom_extensions.clear()
        
        # Reset path to current directory
        self._use_current_folder()
        
        # Clear formula and auto-formula tracking
        self.formula_input.clear()
        self._last_auto_formula = ""
        
        # Reset unique mode
        self.cb_unique.setChecked(False)
        
        # Clear results
        self.results_display.clear()
        
    def _run_test_suite(self):
        """Run the educational test suite"""
        # Show a dialog to explain what the test suite does
        dialog = QMessageBox()
        dialog.setWindowTitle("Educational Test Suite")
        dialog.setIcon(QMessageBox.Icon.Information)
        dialog.setText("Run Educational Examples")
        dialog.setInformativeText(
            "This will run 5 example searches with different complexity levels:\n\n"
            "• Level 1: Simple single variable\n"
            "• Level 2: Basic AND/OR operations\n"
            "• Level 3: Medium complexity with parentheses\n"
            "• Level 4: Advanced multi-variable logic\n"
            "• Level 5: Expert nested formulas\n\n"
            "Each run generates different formulas to show various patterns.\n"
            "Results will be displayed in a terminal window.\n\n"
            "This helps you learn how to construct effective search formulas!"
        )
        dialog.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        
        if dialog.exec() == QMessageBox.StandardButton.Ok:
            self._execute_test_suite()
    
    def _execute_test_suite(self):
        """Execute the test suite in a separate process"""
        try:
            import subprocess
            import os
            
            # Path to the test suite generator
            test_suite_path = os.path.join(os.path.dirname(__file__), 'test_suite_generator.py')
            
            # Run the test suite in a new terminal window
            if os.name == 'nt':  # Windows
                subprocess.Popen(['start', 'cmd', '/c', f'python "{test_suite_path}" && pause'], shell=True)
            else:  # Linux/Mac
                # Try different terminal emulators
                terminal_commands = [
                    ['gnome-terminal', '--', 'python3', test_suite_path],
                    ['xterm', '-e', f'python3 {test_suite_path}; read -p "Press Enter to close..."'],
                    ['konsole', '-e', 'python3', test_suite_path],
                    ['terminal', '-e', 'python3', test_suite_path]
                ]
                
                success = False
                for cmd in terminal_commands:
                    try:
                        subprocess.Popen(cmd)
                        success = True
                        break
                    except FileNotFoundError:
                        continue
                
                if not success:
                    # Fallback: run in current terminal
                    subprocess.run(['python3', test_suite_path])
                    
        except Exception as e:
            # If external execution fails, show results in results display
            self._run_test_suite_internal()
    
    def _run_test_suite_internal(self):
        """Run test suite internally and display results"""
        try:
            # Import and run the test suite generator
            from test_suite_generator import TestSuiteRunner
            
            # Clear results display
            self.results_display.clear()
            self.results_display.setTextColor(QColor(100, 200, 255))
            self.results_display.append("🎓 Running Educational Test Suite...")
            self.results_display.append("=" * 50)
            
            # Run the test suite
            runner = TestSuiteRunner()
            scenarios = runner.generator.generate_test_suite()
            
            # Display each scenario
            for i, scenario in enumerate(scenarios, 1):
                self.results_display.setTextColor(QColor(255, 200, 100))
                self.results_display.append(f"\n📊 Level {scenario['complexity']}: {scenario['name']}")
                self.results_display.append("=" * 40)
                
                # Show variables
                self.results_display.setTextColor(QColor(150, 255, 150))
                self.results_display.append("Variables:")
                for letter, phrase_data in scenario['phrases'].items():
                    if phrase_data['text']:
                        case_info = "Case Sensitive" if phrase_data['case_sensitive'] else "Case Insensitive"
                        self.results_display.append(f"  {letter} = '{phrase_data['text']}' ({case_info})")
                
                # Show formula
                self.results_display.setTextColor(QColor(255, 255, 100))
                self.results_display.append(f"Formula: {scenario['formula']}")
                
                # Show educational note
                self.results_display.setTextColor(QColor(200, 200, 255))
                self.results_display.append(f"💡 {scenario['educational_note']}")
                
                # Offer to try this formula
                self.results_display.setTextColor(QColor(100, 255, 100))
                self.results_display.append("← You can copy this formula to try it yourself!")
            
            # Final message
            self.results_display.setTextColor(QColor(255, 200, 100))
            self.results_display.append("\n" + "=" * 50)
            self.results_display.append("🎓 Educational Examples Complete!")
            self.results_display.append("💡 Try copying any formula above to test it yourself")
            self.results_display.append("🔄 Click 'Run Examples' again for different formulas")
            
        except Exception as e:
            self.results_display.setTextColor(QColor(255, 100, 100))
            self.results_display.append(f"Error running test suite: {e}")
        
    def closeEvent(self, event):
        """Handle application close event"""
        # Clean up search thread
        if self.search_thread and self.search_thread.isRunning():
            self.search_worker.cancel()
            self.search_thread.quit()
            self.search_thread.wait()
        event.accept()


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Finder")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Project Himalaya")
    
    # Create and show the main window
    window = Finder()
    window.show()
    
    # Run the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()