import os
import glob

# ANSI Color Codes für farbige Ausgabe
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    
    @staticmethod
    def colorize(text: str, color: str) -> str:
        return f"{color}{text}{Colors.RESET}"
    
    @staticmethod
    def colorize_for_file(text: str, color: str) -> str:
        """Für Dateien ohne ANSI-Codes - nur reiner Text"""
        return text

def analyze_file_length(file_path):
    """
    Analyze file lengths for HTML, CSS, SCSS, SASS, JS, TS files
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        total_lines = len(lines)
        
        # Count non-empty lines
        non_empty_lines = sum(1 for line in lines if line.strip())
        
        # Count comment lines and JSDoc separately
        comment_lines = 0
        jsdoc_lines = 0
        in_multiline_comment = False
        in_jsdoc_block = False
        
        for line in lines:
            stripped = line.strip()
            
            # Check for JSDoc start
            if stripped.startswith('/**'):
                in_jsdoc_block = True
                jsdoc_lines += 1
                continue
            
            # Check for multiline comment start (but not JSDoc)
            elif stripped.startswith('/*') and not stripped.startswith('/**'):
                in_multiline_comment = True
                comment_lines += 1
                continue
            
            # Check for comment/JSDoc end
            elif stripped.endswith('*/'):
                if in_jsdoc_block:
                    jsdoc_lines += 1
                    in_jsdoc_block = False
                elif in_multiline_comment:
                    comment_lines += 1
                    in_multiline_comment = False
                continue
            
            # Lines inside JSDoc block
            elif in_jsdoc_block:
                jsdoc_lines += 1
            
            # Lines inside multiline comment block
            elif in_multiline_comment:
                comment_lines += 1
            
            # Single line comments and other comment types
            elif (stripped.startswith('//') or  # JS/TS single line comments
                  stripped.startswith('*') or   # continuation of multiline comments
                  stripped.startswith('<!--') or  # HTML comments
                  stripped.startswith('#')):    # SCSS/SASS comments
                comment_lines += 1
        
        # Calculate code lines (non-empty, non-comment, non-jsdoc)
        code_lines = non_empty_lines - comment_lines - jsdoc_lines
        
        return {
            'file': file_path,
            'total_lines': total_lines,
            'non_empty_lines': non_empty_lines,
            'comment_lines': comment_lines,
            'jsdoc_lines': jsdoc_lines,
            'code_lines': code_lines,
            'file_type': get_file_type(file_path)
        }
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def get_file_type(file_path):
    """Get the file type based on extension"""
    extension = os.path.splitext(file_path)[1].lower()
    type_mapping = {
        '.html': 'HTML',
        '.css': 'CSS',
        '.scss': 'SCSS',
        '.sass': 'SASS',
        '.js': 'JavaScript',
        '.ts': 'TypeScript'
    }
    return type_mapping.get(extension, 'Unknown')

def scan_all_files():
    """Scan all HTML, CSS, SCSS, SASS, JS, TS files for length analysis"""
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define file patterns to search for
    file_patterns = [
        "**/*.html",
        "**/*.css", 
        "**/*.scss",
        "**/*.sass",
        "**/*.js",
        "**/*.ts"
    ]
    
    # Collect all files
    all_files = []
    for pattern in file_patterns:
        full_pattern = os.path.join(script_dir, pattern)
        files = glob.glob(full_pattern, recursive=True)
        all_files.extend(files)
    
    # Filter out unwanted directories
    excluded_dirs = ['node_modules', '.git', 'dist', 'build', '.angular', 'coverage', '.vscode', '.idea']
    files = []
    for file_path in all_files:
        # Check if file contains any excluded directory in its path
        should_exclude = any(excluded_dir in file_path for excluded_dir in excluded_dirs)
        if not should_exclude:
            files.append(file_path)
    
    # Group files by type
    files_by_type = {
        'HTML': [f for f in files if f.endswith('.html')],
        'CSS': [f for f in files if f.endswith('.css')],
        'SCSS': [f for f in files if f.endswith('.scss')],
        'SASS': [f for f in files if f.endswith('.sass')],
        'JavaScript': [f for f in files if f.endswith('.js')],
        'TypeScript': [f for f in files if f.endswith('.ts')]
    }
    
    # Prepare output content
    output_lines = []
    output_lines.append("FILE LENGTH ANALYSIS REPORT")
    output_lines.append(f"Generated: {os.popen('date /t').read().strip()} {os.popen('time /t').read().strip()}")
    output_lines.append("=" * 80)
    output_lines.append(f"Analyzing {len(files)} files for length > 400 lines...")
    output_lines.append(f"Search directory: {script_dir}")
    
    # Display file counts by type with colors
    print(Colors.colorize("FILE LENGTH ANALYSIS REPORT", Colors.BOLD + Colors.CYAN))
    print(Colors.colorize("=" * 80, Colors.CYAN))
    print(Colors.colorize(f"Analyzing {len(files)} files for length > 400 lines...", Colors.YELLOW))
    print(Colors.colorize(f"Search directory: {script_dir}", Colors.BLUE))
    print()
    
    for file_type, type_files in files_by_type.items():
        if type_files:
            count_msg = f"{file_type} files: {len(type_files)}"
            print(Colors.colorize(count_msg, Colors.GREEN))
            output_lines.append(count_msg)
    
    output_lines.append(f"Excluded directories: {', '.join(excluded_dirs)}")
    output_lines.append("")
    print(Colors.colorize(f"Excluded directories: {', '.join(excluded_dirs)}", Colors.MAGENTA))
    print("")
    
    all_large_files = []
    files_over_400 = 0
    
    # Analyze each file
    for file_path in files:
        file_info = analyze_file_length(file_path)
        if file_info and file_info['total_lines'] > 400:
            files_over_400 += 1
            all_large_files.append(file_info)
            
            file_output = f"File: {file_path}"
            separator = "-" * 80
            
            print(Colors.colorize(file_output, Colors.BOLD + Colors.YELLOW))
            print(Colors.colorize(separator, Colors.YELLOW))
            output_lines.append(file_output)
            output_lines.append(separator)
            
            details = f"  Type: {file_info['file_type']} | Total lines: {file_info['total_lines']}"
            breakdown = f"  Non-empty: {file_info['non_empty_lines']} | Comments: {file_info['comment_lines']} | JSDoc: {file_info['jsdoc_lines']} | Code: {file_info['code_lines']}"
            
            # Color coding based on file size
            if file_info['total_lines'] > 800:
                print(Colors.colorize(details, Colors.RED))
                print(Colors.colorize(breakdown, Colors.RED))
            elif file_info['total_lines'] > 600:
                print(Colors.colorize(details, Colors.YELLOW))
                print(Colors.colorize(breakdown, Colors.YELLOW))
            else:
                print(Colors.colorize(details, Colors.WHITE))
                print(Colors.colorize(breakdown, Colors.BLUE))
            print("")
            
            output_lines.append(details)
            output_lines.append(breakdown)
            output_lines.append("")
    
    # Sort by total lines (largest first)
    all_large_files.sort(key=lambda x: x['total_lines'], reverse=True)
    
    # Top 10 largest files
    top_section = "=" * 80
    top_header = "=== TOP 10 LARGEST FILES ==="
    
    print(Colors.colorize(top_section, Colors.MAGENTA))
    print(Colors.colorize(top_header, Colors.BOLD + Colors.MAGENTA))
    print(Colors.colorize(top_section, Colors.MAGENTA))
    
    output_lines.append(top_section)
    output_lines.append(top_header)
    output_lines.append(top_section)
    
    for i, file_info in enumerate(all_large_files[:10]):
        rank_line = f"{i+1:2d}. {os.path.basename(file_info['file'])} ({file_info['total_lines']} lines)"
        type_line = f"    Type: {file_info['file_type']}"
        file_line = f"    File: {file_info['file']}"
        
        # Color coding for ranking
        if i < 3:  # Top 3
            print(Colors.colorize(rank_line, Colors.BOLD + Colors.RED))
        elif i < 6:  # 4-6
            print(Colors.colorize(rank_line, Colors.BOLD + Colors.YELLOW))
        else:  # 7-10
            print(Colors.colorize(rank_line, Colors.BOLD + Colors.GREEN))
            
        print(Colors.colorize(type_line, Colors.CYAN))
        print(Colors.colorize(file_line, Colors.BLUE))
        print("")
        
        output_lines.append(rank_line)
        output_lines.append(type_line)
        output_lines.append(file_line)
        output_lines.append("")
    
    # Summary by file type
    summary_header = "=== SUMMARY BY FILE TYPE ==="
    print(Colors.colorize(summary_header, Colors.BOLD + Colors.CYAN))
    output_lines.append(summary_header)
    
    type_summary = {}
    for file_info in all_large_files:
        file_type = file_info['file_type']
        if file_type not in type_summary:
            type_summary[file_type] = {
                'count': 0,
                'total_lines': 0,
                'max_lines': 0,
                'files': []
            }
        type_summary[file_type]['count'] += 1
        type_summary[file_type]['total_lines'] += file_info['total_lines']
        type_summary[file_type]['max_lines'] = max(type_summary[file_type]['max_lines'], file_info['total_lines'])
        type_summary[file_type]['files'].append(file_info)
    
    for file_type in ['HTML', 'CSS', 'SCSS', 'SASS', 'JavaScript', 'TypeScript']:
        if file_type in type_summary:
            data = type_summary[file_type]
            avg_lines = data['total_lines'] / data['count']
            type_line = f"{file_type}: {data['count']} files > 400 lines (avg: {avg_lines:.1f}, max: {data['max_lines']})"
            print(Colors.colorize(type_line, Colors.GREEN))
        else:
            type_line = f"{file_type}: 0 files > 400 lines"
            print(Colors.colorize(type_line, Colors.BLUE))
        
        output_lines.append(type_line)
    
    # Overall summary
    overall_header = "\n=== OVERALL SUMMARY ==="
    files_analyzed = f"Files analyzed: {len(files)}"
    files_over_limit = f"Files over 400 lines: {files_over_400}"
    
    print(Colors.colorize(overall_header, Colors.BOLD + Colors.YELLOW))
    print(Colors.colorize(files_analyzed, Colors.WHITE))
    print(Colors.colorize(files_over_limit, Colors.YELLOW))
    
    output_lines.append(overall_header)
    output_lines.append(files_analyzed)
    output_lines.append(files_over_limit)
    
    if files_over_400 == 0:
        no_large_files_msg = "No files longer than 400 lines found!"
        print(Colors.colorize(no_large_files_msg, Colors.BOLD + Colors.GREEN))
        output_lines.append(no_large_files_msg)
    else:
        avg_length = sum(f['total_lines'] for f in all_large_files) / len(all_large_files)
        largest = max(all_large_files, key=lambda x: x['total_lines'])
        avg_msg = f"Average length of large files: {avg_length:.1f} lines"
        largest_msg = f"Largest file: {os.path.basename(largest['file'])} ({largest['total_lines']} lines)"
        
        print(Colors.colorize(avg_msg, Colors.WHITE))
        print(Colors.colorize(largest_msg, Colors.BOLD + Colors.RED))
        
        output_lines.append(avg_msg)
        output_lines.append(largest_msg)
        
        # Recommendations
        recommendations = [
            "\n=== RECOMMENDATIONS ===",
            "• Files > 500 lines: Consider splitting into multiple files",
            "• HTML files > 400 lines: Break into components or templates", 
            "• CSS/SCSS files > 600 lines: Use modular architecture (BEM, modules)",
            "• JS/TS files > 400 lines: Split into smaller modules or services"
        ]
        
        for i, rec in enumerate(recommendations):
            if i == 0:
                print(Colors.colorize(rec, Colors.BOLD + Colors.MAGENTA))
            else:
                print(Colors.colorize(rec, Colors.CYAN))
            output_lines.append(rec)
    
    # Write to file
    output_file = "file_length_analysis.txt"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output_lines))
        print(Colors.colorize(f"\nResults saved to: {output_file}", Colors.BOLD + Colors.GREEN))
    except Exception as e:
        print(Colors.colorize(f"\nError saving to file: {e}", Colors.RED))

if __name__ == "__main__":
    scan_all_files()
