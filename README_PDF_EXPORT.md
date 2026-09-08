# Jupyter Notebook to PDF Export Guide

## Quick Start

```bash
python export_notebook_to_pdf.py presentation/FireWatch_Indonesia_Report.ipynb
```

## Requirements

### 1. Pandoc
- Download: https://pandoc.org/installing.html
- Windows: `winget install --id JohnMacFarlane.Pandoc`
- Verify: `pandoc --version`

### 2. MiKTeX (LaTeX distribution)
- Download: https://miktex.org/download
- Windows: `winget install --id MiKTeX.MiKTeX`
- Verify: `xelatex --version`

### 3. Python packages
```bash
pip install jupyter nbconvert
```

## Usage

### Basic
```bash
python export_notebook_to_pdf.py <notebook_path>
```

### Example
```bash
python export_notebook_to_pdf.py presentation/FireWatch_Indonesia_Report.ipynb
```

## Features

The export script automatically applies professional formatting:

✓ **Better margins** - 2cm on all sides (instead of default 0.5 inch)  
✓ **Improved spacing** - Better paragraph and element spacing  
✓ **Code formatting** - Smaller font size for code cells  
✓ **Figure placement** - Fixed position figures (no floating)  
✓ **Two-pass compilation** - Ensures proper references and TOC  

## Output

- Input: `notebook.ipynb`
- Output: `notebook.pdf` (same directory)
- Intermediate: `notebook.tex` (LaTeX source, can be deleted)

## Troubleshooting

### "Pandoc not found"
- Install Pandoc and restart terminal/PowerShell
- Add to PATH: `C:\Users\<Username>\AppData\Local\Pandoc`

### "xelatex not found"
- Install MiKTeX and restart terminal/PowerShell  
- Add to PATH: `C:\Users\<Username>\AppData\Local\Programs\MiKTeX\miktex\bin\x64`

### "PDF not created"
- Check `.log` file in output directory for LaTeX errors
- Ensure notebook has no syntax errors
- Try running notebook cells first to verify they execute

## Manual Alternative

If automated export fails, use Jupyter directly:

1. Open notebook in Jupyter
2. File → Save and Export Notebook As → PDF
3. (Requires Pandoc + LaTeX installed)

## Notes

- First run may be slow as MiKTeX downloads required packages
- Subsequent runs are faster
- Large notebooks with many images will produce larger PDFs
- Default uses XeLaTeX for better Unicode/font support
