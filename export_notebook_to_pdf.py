"""
Export Jupyter Notebook to Professional PDF

Usage:
    python export_notebook_to_pdf.py <notebook_path>

Example:
    python export_notebook_to_pdf.py presentation/FireWatch_Indonesia_Report.ipynb

Requirements:
    - Pandoc installed (https://pandoc.org/installing.html)
    - MiKTeX installed (https://miktex.org/download)
    - jupyter, nbconvert

Author: FireWatch Indonesia Project
Date: September 2026
"""
import subprocess
import os
import sys

def export_notebook_to_pdf(notebook_path):
    """
    Convert Jupyter notebook to well-formatted PDF
    
    Args:
        notebook_path: Path to .ipynb file
    """
    # Setup PATH for Pandoc and MiKTeX
    os.environ['PATH'] += ';C:\\Users\\Muh Asrul\\AppData\\Local\\Pandoc;C:\\Users\\Muh Asrul\\AppData\\Local\\Programs\\MiKTeX\\miktex\\bin\\x64'
    
    # Validate input
    if not os.path.exists(notebook_path):
        print(f"✗ Error: File not found: {notebook_path}")
        return False
    
    if not notebook_path.endswith('.ipynb'):
        print("✗ Error: File must be a Jupyter notebook (.ipynb)")
        return False
    
    # Get output directory and filename
    output_dir = os.path.dirname(notebook_path)
    base_name = os.path.splitext(os.path.basename(notebook_path))[0]
    tex_file = os.path.join(output_dir, f'{base_name}.tex')
    pdf_file = os.path.join(output_dir, f'{base_name}.pdf')
    
    print(f"Converting: {notebook_path}")
    print(f"Output PDF: {pdf_file}\n")
    
    # Step 1: Generate LaTeX file
    print("Step 1: Generating LaTeX file...")
    latex_cmd = [
        'python', '-m', 'jupyter', 'nbconvert',
        '--to', 'latex',
        notebook_path,
        '--output', f'{base_name}.tex',
        '--output-dir', output_dir if output_dir else '.'
    ]
    
    result = subprocess.run(latex_cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("✗ Error generating LaTeX:")
        print(result.stderr)
        return False
    
    # Step 2: Improve LaTeX formatting
    print("Step 2: Improving LaTeX formatting...")
    
    try:
        with open(tex_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Better margins (2cm all sides)
        content = content.replace(
            r'\usepackage[margin=0.5in]{geometry}',
            r'\usepackage[top=2cm, bottom=2cm, left=2cm, right=2cm]{geometry}'
        )
        
        # Better spacing between paragraphs
        if r'\usepackage{geometry}' in content and r'\setlength{\parskip}' not in content:
            content = content.replace(
                r'\usepackage{geometry}',
                r'''\usepackage{geometry}
\setlength{\parskip}{0.5em}
\setlength{\parindent}{0pt}'''
            )
        
        # Better figure placement
        if r'\usepackage{graphicx}' in content and r'\floatplacement' not in content:
            content = content.replace(
                r'\usepackage{graphicx}',
                r'''\usepackage{graphicx}
\usepackage{float}
\floatplacement{figure}{H}'''
            )
        
        # Smaller code font size for readability
        content = content.replace(
            r'\begin{Verbatim}[commandchars=',
            r'\begin{Verbatim}[fontsize=\small,commandchars='
        )
        
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✓ LaTeX formatting improved")
    
    except Exception as e:
        print(f"✗ Error modifying LaTeX: {e}")
        return False
    
    # Step 3: Compile to PDF (run twice for proper references)
    print("\nStep 3: Compiling to PDF...")
    xelatex_exe = 'C:\\Users\\Muh Asrul\\AppData\\Local\\Programs\\MiKTeX\\miktex\\bin\\x64\\xelatex.exe'
    
    if not os.path.exists(xelatex_exe):
        print("✗ Error: XeLaTeX not found. Please install MiKTeX.")
        return False
    
    for run in [1, 2]:
        print(f"  Compilation run {run}/2...")
        result = subprocess.run([
            xelatex_exe,
            '-interaction=nonstopmode',
            '-output-directory=' + (output_dir if output_dir else '.'),
            tex_file
        ], capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode != 0 and run == 2:
            print(f"✗ Warning: XeLaTeX returned code {result.returncode}")
    
    # Check if PDF was created
    if os.path.exists(pdf_file):
        size_mb = os.path.getsize(pdf_file) / (1024 * 1024)
        print(f"\n✓ PDF created successfully!")
        print(f"  File: {pdf_file}")
        print(f"  Size: {size_mb:.2f} MB")
        return True
    else:
        print("\n✗ PDF file not created. Check LaTeX logs for errors.")
        return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python export_notebook_to_pdf.py <notebook_path>")
        print("Example: python export_notebook_to_pdf.py presentation/FireWatch_Indonesia_Report.ipynb")
        sys.exit(1)
    
    notebook_path = sys.argv[1]
    success = export_notebook_to_pdf(notebook_path)
    sys.exit(0 if success else 1)
