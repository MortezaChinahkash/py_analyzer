# Code Analyzer Suite

A comprehensive Python-based code analysis toolkit for web development projects. This suite provides multiple specialized analyzers to help maintain code quality, documentation standards, and file organization across HTML, CSS, JavaScript, and TypeScript codebases.

**Made by Morteza Chinahkash**

## 🔍 Overview

The Code Analyzer Suite consists of four specialized tools that can be run individually or together through a central control interface:

1. **📏 File Length Analyzer** - Identifies oversized files that may need refactoring
2. **📝 JSDoc Coverage Analyzer** - Ensures comprehensive documentation coverage
3. **🔧 Method Length Analyzer** - Finds methods that exceed recommended length limits
4. **🧹 Console.log Remover** - Safely removes console.log statements with backup functionality

## 🚀 Quick Start

### Installation
No installation required! Just download all files and place them in your project directory.

### Requirements
- Python 3.6 or higher
- Standard library modules only (no external dependencies)

### Basic Usage
```bash
# Run the main controller for interactive menu
python main_analyzer.py

# Or run individual analyzers
python analyze_file_length.py
python analyze_jsdoc_coverage.py
python analyze_method_length_simple.py
python remove_console_logs.py
```

## 🎯 Main Controller Features

The `main_analyzer.py` provides a central control interface with:

- **🎨 Colored Output**: ANSI color-coded console output for better readability
- **📋 Interactive Menu**: User-friendly selection interface
- **🔥 Multiple Selection**: Run multiple analyzers with comma-separated input (e.g., `1,2,4`)
- **🚀 Run All**: Execute all analyzers sequentially with one command
- **⚠️ Safety Confirmations**: Confirmation prompts for file-modifying operations
- **📊 Summary Reports**: Consolidated results and success/failure tracking

### Menu Options
```
1 - 📏 File Length Analyzer
2 - 📝 JSDoc Coverage Analyzer  
3 - 🔧 Method Length Analyzer
4 - 🧹 Console.log Remover
5 - 🚀 Run All Analyzers
0 - ❌ Exit
```

## 📏 File Length Analyzer

Identifies files that exceed recommended size limits to help maintain code quality and readability.

### Features
- **Multi-Format Support**: Analyzes HTML, CSS, SCSS, SASS, JavaScript, and TypeScript files
- **Intelligent Analysis**: Distinguishes between total lines, non-empty lines, comments, and code
- **Smart Filtering**: Automatically excludes build and dependency directories
- **Top 10 Ranking**: Identifies the largest files for priority refactoring

### Default Threshold
- **400 lines** - Files exceeding this limit are flagged for review

### File Types Analyzed
- HTML files (`.html`)
- CSS files (`.css`, `.scss`, `.sass`)
- JavaScript files (`.js`)
- TypeScript files (`.ts`)

### Output
- Console progress and summary
- Detailed report: `file_length_analysis.txt`
- File-by-file breakdown with line counts
- Top 10 largest files ranking

### Refactoring Guidelines
- **Critical (>600 lines)**: Immediate action required
- **High Priority (500-600 lines)**: Plan refactoring in next sprint
- **Medium Priority (400-500 lines)**: Monitor and prevent further growth

## 📝 JSDoc Coverage Analyzer

Ensures comprehensive documentation coverage across your TypeScript and JavaScript codebase.

### Features
- **Comprehensive Method Detection**: Identifies various code constructs including:
  - Regular methods and functions
  - Constructors and lifecycle hooks
  - Arrow functions and async functions
  - Getters, setters, and static methods
  - Private, public, and protected methods

- **Smart JSDoc Detection**: Recognizes different JSDoc patterns
  - Multi-line JSDoc blocks (`/** ... */`)
  - Single-line JSDoc comments
  - Proper positioning above methods

### Method Types Analyzed
- **High Priority**: Public methods, constructors, getters/setters, event handlers
- **Medium Priority**: Private methods, arrow functions, lifecycle hooks
- **Lower Priority**: Test functions, animation definitions, simple assignments

### Coverage Goals
- **Production Code**: 95%+ JSDoc coverage
- **Service Classes**: 100% for public methods
- **Components**: 90%+ for public methods and lifecycle hooks
- **Utilities**: 100% for all exported functions

### Output
- Real-time analysis progress
- Detailed report: `jsdoc_coverage_analysis.txt`
- Missing JSDoc grouped by method type
- Top 10 files with most missing documentation
- Coverage statistics and recommendations

### JSDoc Best Practices
```javascript
/**
 * Brief description of what the method does
 * @param {string} paramName - Description of parameter
 * @param {number} optionalParam - Optional parameter description
 * @returns {boolean} Description of return value
 * @throws {Error} When something goes wrong
 * @example
 * // Usage example
 * const result = methodName('value', 42);
 */
methodName(paramName: string, optionalParam?: number): boolean {
    // Method implementation
}
```

## 🔧 Method Length Analyzer

Identifies methods and functions that exceed recommended length limits for better maintainability.

### Features
- **Universal Compatibility**: Works in any TypeScript/JavaScript project
- **Smart Method Detection**: Recognizes various method types including:
  - Regular methods and functions
  - Angular lifecycle hooks
  - Constructors and async functions
  - Private/public/protected methods
  - Static methods, getters, and setters

### Default Threshold
- **14 lines of code** - Methods exceeding this limit are flagged for review

### Quality Guidelines
- **15-20 lines**: Consider minor refactoring
- **20+ lines**: Strong candidate for breaking down
- **30+ lines**: High priority for refactoring

### Output
- Console progress with method details
- Detailed report: `method_length_analysis.txt`
- Top 10 longest methods ranking
- Line numbers and method declarations
- Refactoring recommendations

### Why 14 Lines?
- Functions under 15 lines are easier to understand
- Smaller functions are easier to test
- Better compliance with Single Responsibility Principle
- Improved code maintainability

## 🧹 Console.log Remover

Safely removes console.log statements from JavaScript and TypeScript files with built-in backup functionality.

### Features
- **Safe File Modification**: Built-in backup system with timestamped folders
- **Intelligent Detection**: Complex regex patterns for various console.log formats
- **Smart Filtering**: Excludes build directories and dependencies
- **Detailed Reporting**: Comprehensive removal statistics and remaining logs

### Backup System
- **Automatic Backup Creation**: Timestamped backup folders (`YYYYMMDD_HHMMSS`)
- **Directory Structure Preservation**: Maintains original folder hierarchy
- **User Confirmation**: Optional backup creation with user prompt
- **Safety First**: Prevents data loss during file modification

### Console.log Patterns Detected
- Standard: `console.log('message')`
- Multi-line: `console.log('multi', 'line', 'arguments')`
- Complex expressions: `console.log(object.property, calculations)`
- Commented logs: `// console.log('debug')`

### Safety Features
- **⚠️ Warning Prompts**: Clear warnings about file modification
- **💾 Backup Confirmation**: Ask before creating backups
- **📊 Detailed Reporting**: Shows exactly what was removed
- **🔒 Error Handling**: Graceful handling of file access issues

### Output
- Real-time processing with colored feedback
- Detailed report: `console_log_removal_report_TIMESTAMP.txt`
- Backup location information
- Removal success rate and statistics

## 🛠️ Customization

### Changing Thresholds

**File Length Analyzer**
```python
if file_info and file_info['total_lines'] > 400:  # Change 400 to your limit
```

**Method Length Analyzer**
```python
if method_info and method_info['code_lines'] > 14:  # Change 14 to your limit
```

### Adding File Types
```python
file_patterns = [
    "**/*.html",
    "**/*.css", 
    "**/*.scss",
    "**/*.sass",
    "**/*.js",
    "**/*.ts",
    "**/*.vue",    # Add Vue files
    "**/*.jsx",    # Add JSX files
    "**/*.tsx"     # Add TSX files
]
```

### Custom Excluded Directories
```python
excluded_dirs = [
    'node_modules', '.git', 'dist', 'build', 
    '.angular', 'coverage', '.vscode', '.idea', 
    'your_custom_dir'  # Add your directories
]
```

## 🔧 Integration with Development Workflow

### Pre-commit Hook
Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash
python main_analyzer.py
# Add logic to fail commit based on analysis results
```

### VS Code Tasks
Add to `.vscode/tasks.json`:
```json
{
    "label": "Run Code Analysis",
    "type": "shell",
    "command": "python",
    "args": ["main_analyzer.py"],
    "group": "build",
    "presentation": {
        "echo": true,
        "reveal": "always",
        "focus": false,
        "panel": "shared"
    }
}
```

### Continuous Integration
```yaml
# GitHub Actions example
- name: Code Quality Analysis
  run: |
    python main_analyzer.py
    # Parse results for quality gates
```

## 📊 Output Files

Each analyzer generates detailed reports:

1. **`file_length_analysis.txt`** - File size analysis with refactoring priorities
2. **`jsdoc_coverage_analysis.txt`** - Documentation coverage with missing JSDoc details
3. **`method_length_analysis.txt`** - Method length analysis with refactoring candidates
4. **`console_log_removal_report_TIMESTAMP.txt`** - Console.log removal results with backup info

## 🚫 Excluded Directories

All analyzers automatically exclude these common directories:
- `node_modules/` - Package dependencies
- `.git/` - Git repository data
- `dist/`, `build/` - Build output
- `.angular/` - Angular CLI cache
- `coverage/` - Test coverage reports
- `.vscode/`, `.idea/` - IDE settings
- `backups/` - Backup folders

## 🎯 Best Practices

### Regular Monitoring
- Run analysis monthly or before major releases
- Track metrics over time to measure improvement
- Set up automated alerts for threshold violations

### Team Guidelines
- Establish file size and method length standards
- Include analysis in code review checklist
- Document refactoring decisions and improvements

### Code Quality Goals
- **File Length**: Keep files under 400 lines
- **Method Length**: Keep methods under 15 lines
- **Documentation**: Maintain 90%+ JSDoc coverage
- **Clean Code**: Remove debug console.log statements

## 🔍 Troubleshooting

### No Files Found
- Ensure scripts are in your project root directory
- Check that project contains supported file types
- Verify excluded directories aren't filtering your code

### Encoding Issues
- Ensure files are UTF-8 encoded
- Check for BOM (Byte Order Mark) issues
- Verify file permissions

### Performance Issues
- Large codebases may take longer to analyze
- Consider running on specific directories
- Use file filtering options for targeted analysis

## 🚀 Example Workflows

### Initial Project Assessment
```bash
# Run full analysis suite
python main_analyzer.py
# Select option 5 (Run All Analyzers)
# Review all generated reports
```

### Focused Analysis
```bash
# Run specific analyzers
python main_analyzer.py
# Select "1,2,4" for file length, JSDoc, and console.log removal
```

### Pre-deployment Check
```bash
# Quick method and file length check
python main_analyzer.py
# Select "1,3" for file and method length analysis
```

### Documentation Audit
```bash
# Focus on documentation coverage
python analyze_jsdoc_coverage.py
# Review missing JSDoc and improve coverage
```

## 🔮 Future Enhancements

Potential improvements for the suite:
1. **Enhanced Parsing**: More sophisticated language-specific parsers
2. **IDE Integration**: VS Code extension with real-time feedback
3. **Historical Tracking**: Track improvements over time
4. **Custom Templates**: Generate JSDoc templates for missing documentation
5. **Quality Scoring**: Advanced metrics beyond simple line counts
6. **Export Formats**: JSON, CSV output options for CI/CD integration

## 📄 License

This tool suite is provided as-is for code quality analysis. Feel free to modify and distribute according to your project's needs.

## 🤝 Contributing

To enhance this tool suite:
1. Add support for more programming languages
2. Implement configurable thresholds per file type
3. Add complexity metrics analysis
4. Create web-based dashboard for results
5. Develop IDE plugins for real-time analysis

---

## 🎉 Summary

The Code Analyzer Suite provides comprehensive code quality analysis for web development projects. With its user-friendly interface, multiple selection capabilities, and detailed reporting, it helps teams maintain high code quality standards across their entire codebase.

**Key Benefits:**
- 🎯 **Focused Analysis**: Target specific quality aspects
- 🔄 **Flexible Execution**: Run individually or as a complete suite
- 💾 **Safe Operations**: Built-in backup functionality for file modifications
- 📊 **Detailed Reporting**: Comprehensive analysis results
- 🎨 **User-Friendly**: Colored output and interactive interface

**Keep your code clean, documented, and well-organized!** 🏗️

---

**Made by Morteza Chinahkash** - *Professional Code Quality Analysis Tools*

*"Well-analyzed code is maintainable code. Invest in quality analysis to invest in your project's future."*
