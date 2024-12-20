# OCR to PDF Converter

A Python-based tool for converting images and PDFs to searchable PDF documents using OCR technology.

## Features

- Convert images to searchable PDFs
- Process existing PDFs to add searchable text
- Support for multiple file formats (PNG, JPG, TIFF, PDF)
- Batch processing for multiple files
- Command-line interface for easy automation
- Detailed logging and error handling

## Requirements

### Conda Dependencies
- Python 3.10.12
- PyPDF2 3.0.1 (PDF handling)
- Pytesseract 0.3.10 (OCR processing)
- Pillow 10.0.1 (Image processing)
- Reportlab 4.0.7 (PDF creation)
- Tesseract 5.3.3 (OCR engine)
- Ghostscript 10.04.0 (PDF processing)

### Pip Dependencies
- PyMuPDF 1.23.8 (PDF to image conversion)
- Click ≥8.1.0, <9.0.0 (CLI interface)
- Rich ≥13.0.0, <14.0.0 (Rich text and formatting)

### CLI Interface
- Click ≥8.1.0, <9.0.0
- Rich ≥13.0.0, <14.0.0

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ocr2pdf.git
cd ocr2pdf
```

2. Create and activate conda environment:
```bash
# Create environment with core dependencies
conda env create -f environment.yml
conda activate ocr2pdf

# Install additional pip packages
pip install -r requirements.txt
```

3. Verify installation:
```bash
# Check Tesseract
python -c "import pytesseract; print(pytesseract.get_tesseract_version())"

# Check PyMuPDF
python -c "import fitz; print(fitz.__version__)"
```

## Usage

### Convert a Single File
```bash
python ocr2pdf.py input_file.pdf output.pdf
```

### Process Multiple Files
```bash
python ocr2pdf.py input_directory/ output.pdf
```

### Supported Input Formats
- Images: PNG, JPG, JPEG, TIF, TIFF
- Documents: PDF

## Development

### Setup Development Environment
1. Install development dependencies:
```bash
conda activate ocr2pdf
pre-commit install
```

2. Run tests:
```bash
pytest
```

### Code Quality
- All code is formatted using Black with a line length of 88 characters
- Type hints are required for all functions
- Documentation follows Google style docstrings
- Tests are required for all new features

## Troubleshooting

### Common Issues

1. Program doesn't stop after completion
   - Make sure to use the latest version of the script
   - Check if any background processes are running

2. PDF output issues
   - Verify that the output path is a file path, not a directory
   - Ensure write permissions in the output directory

3. OCR quality issues
   - Ensure input images are clear and well-lit
   - Check if Tesseract is properly installed
   - Try adjusting image preprocessing settings

## License

This project is licensed under the MIT License - see the LICENSE file for details.
