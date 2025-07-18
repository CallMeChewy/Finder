# File: QUICK_START.md
# Path: /home/herb/Desktop/Finder/QUICK_START.md
# Standard: AIDEV-PascalCase-2.1
# Created: 2025-07-18
# Last Modified: 2025-07-18  13:53PM

# Finder - Quick Start Guide

## 🚀 Launch the Application

```bash
cd /home/herb/Desktop/Finder
python Finder.py
```

## 📝 5-Minute Tutorial

### Step 1: Your First Search (30 seconds)
1. **Enter search term**: Type "import" in the `A:` field
2. **Click Search**: Green "🔍 Start Search" button (below formula box)
3. **View results**: See matches in right panel

### Step 2: Learn with Examples (2 minutes)
1. **Click "🎓 Run Examples"**: Blue button at bottom of controls
2. **Click "OK"**: In the information dialog
3. **Watch the demo**: See 5 different formula examples
4. **Copy formulas**: Use the examples for your own searches

### Step 3: Try Multiple Terms (1 minute)
1. **Clear form**: Click "🔄 Reset/Clear" (at bottom)
2. **Enter terms**:
   - A: "def"
   - B: "class"
3. **Auto-formula**: App creates "A AND B" automatically
4. **Search**: Click "🔍 Start Search" below formula

### Step 4: Use Common Operators (1 minute)
1. **Manual formula**: Clear auto-formula and type: `A | B`
2. **Validate**: Click "✓ Validate Formula" (orange button) to check
3. **Search**: Click "🔍 Start Search" to find either functions OR classes
4. **Try exclusion**: Type: `A & !B` (functions without classes)

### Step 5: Advanced Search (30 seconds)
1. **Complex formula**: `(A & B) | C`
2. **Add third term**: C: "import"
3. **Search**: Find (functions AND classes) OR imports

## 🎯 Common Use Cases

### Find Python Code Patterns
```
Variables: A="def", B="return"
Formula: A & B
Result: Functions that return values
```

### Search Documentation
```
Variables: A="#", B="Standard"  
Formula: A & B
Result: Headers with "Standard"
```

### Exclude Unwanted Content
```
Variables: A="function", B="error"
Formula: A & !B  
Result: Functions without errors
```

### Complex Logic
```
Variables: A="class", B="def", C="self"
Formula: A & (B | C)
Result: Classes with functions or self
```

## 🔧 Key Features

### Auto-Formula Generation
- Enter terms in A, B, C fields
- Formula auto-creates as "A AND B AND C"
- No manual formula needed for simple searches

### Common Operators
- `&` = AND (both terms)
- `|` = OR (either term)  
- `!` = NOT (exclude term)
- `()` = Grouping

### File Type Selection
- ☑ Check desired file types (.py, .txt, .md)
- Custom: Enter your own (.log, .cfg)
- All types: Leave unchecked

### Search Modes
- **Line**: Search line by line (default)
- **Document**: Search whole documents
- **Unique**: Show only first occurrences

## ✅ Formula Validation

### New Validation Workflow
- **No More Errors While Typing**: Enter formulas without interruption
- **✓ Validate Formula**: Orange button below formula - check for errors on demand
- **🔍 Start Search**: Green button below formula - validates automatically before search
- **Detailed Error Messages**: Clear explanations with specific suggestions

### Validation Results
- **✅ Success**: "Formula is valid! No errors or warnings found."
- **⚠️ Warnings**: Potential issues but search can proceed
- **❌ Errors**: Must be fixed before searching

## 💡 Quick Tips

1. **Start Simple**: Use single terms first (just fill A:)
2. **Use Examples**: Click "🎓 Run Examples" to learn patterns
3. **Validate First**: Use "✓ Validate Formula" to check complex formulas
4. **Copy Formulas**: Take formulas from examples and modify them
5. **Test Small**: Search a small folder first to test formulas
6. **Case Matters**: Uncheck "Match Case" for flexible searching

## 🎓 Learning Path

1. **Beginner**: Single terms (A)
2. **Basic**: Two terms (A & B, A | B)  
3. **Intermediate**: Exclusions (A & !B)
4. **Advanced**: Grouping ((A & B) | C)
5. **Expert**: Complex nested logic

## ⚡ Keyboard Shortcuts

- **Tab**: Navigate between fields
- **Enter**: Start search (🔍 Start Search button)
- **Ctrl+R**: Reset form
- **Ctrl+E**: Run examples

## 🔍 Example Searches You Can Try Right Now

### 1. Find Python Imports
```
A: import
Formula: A
File Types: ☑ .py
```

### 2. Find Documentation Headers  
```
A: #
B: File
Formula: A & B  
File Types: ☑ .md
```

### 3. Find Functions Without Errors
```
A: def
B: error  
Formula: A & !B
File Types: ☑ .py
```

### 4. Find Any Code Definitions
```
A: def
B: class
Formula: A | B
File Types: ☑ .py
```

### 5. Complex Pattern
```
A: function
B: method  
C: return
D: class
Formula: (A | B) & C & !D
File Types: ☑ .py
```

## 🆘 Need Help?

- **Run Examples**: Best way to learn - click the blue button!
- **Tool Tips**: Hover over buttons for quick help
- **Error Messages**: Read the red error text for guidance
- **User Guide**: Open `USER_GUIDE.md` for complete documentation

## 🎉 You're Ready!

You now know enough to start using Finder effectively. The most important tip: **Use the "Run Examples" feature** to see working formulas in action!

Happy searching! 🔍