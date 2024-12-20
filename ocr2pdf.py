"""OCR to PDF conversion tool.

This script converts images and PDFs containing text into searchable PDF documents using OCR.
"""
import logging
from pathlib import Path
from typing import List, Optional
import sys
import fitz  # PyMuPDF for PDF handling

import click
from PIL import Image
import pytesseract
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_image(image_path: Path) -> str:
    """Extract text from an image or PDF using OCR.

    Args:
        image_path: Path to the input image or PDF file.

    Returns:
        str: Extracted text from the image or PDF.

    Raises:
        ValueError: If the image or PDF file is invalid or unreadable.
    """
    image = None
    try:
        if image_path.suffix.lower() == '.pdf':
            # Handle PDF input
            pdf_document = fitz.open(image_path)
            text_parts = []
            
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                pix = page.get_pixmap()
                img_data = pix.tobytes("png")
                image = Image.open(io.BytesIO(img_data))
                text = pytesseract.image_to_string(image)
                text_parts.append(text)
                
            pdf_document.close()
            return '\n\n'.join(text_parts)
        else:
            # Handle regular image input
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text
    except Exception as e:
        logger.error(f"Error processing file {image_path}: {str(e)}")
        raise ValueError(f"Failed to process file: {str(e)}")
    finally:
        if image and not isinstance(image, fitz.fitz.Page):
            image.close()

def create_pdf(text: str, output_path: Path) -> None:
    """Create a PDF document from extracted text.

    Args:
        text: Text content to write to PDF.
        output_path: Path where the PDF will be saved.

    Raises:
        ValueError: If PDF creation fails.
    """
    try:
        # Create parent directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        c = canvas.Canvas(str(output_path), pagesize=letter)
        width, height = letter
        
        # Split text into lines and write to PDF
        y_position = height - 40
        for line in text.split('\n'):
            if y_position <= 40:
                c.showPage()
                y_position = height - 40
            c.drawString(40, y_position, line)
            y_position -= 15
            
        c.save()
        c = None  # Release the canvas object
        logger.info(f"PDF created successfully at {output_path}")
    except Exception as e:
        logger.error(f"Error creating PDF: {str(e)}")
        raise ValueError(f"Failed to create PDF: {str(e)}")

@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path())
def main(input_path: str, output_path: str) -> None:
    """Convert image(s) or PDF(s) to searchable PDF using OCR.

    Args:
        input_path: Path to input image, PDF or directory.
        output_path: Path where the PDF will be saved.
    """
    try:
        input_path = Path(input_path)
        output_path = Path(output_path)

        # Ensure output path has .pdf extension
        if output_path.suffix.lower() != '.pdf':
            output_path = output_path.with_suffix('.pdf')
            logger.info(f"Adding .pdf extension to output path: {output_path}")

        # Check if output path is trying to create a directory
        if output_path.exists() and output_path.is_dir():
            raise click.ClickException(f"Output path '{output_path}' is a directory. Please specify a file path for the PDF output.")

        if input_path.is_file():
            logger.info(f"Processing single file: {input_path}")
            text = process_image(input_path)
            create_pdf(text, output_path)
        elif input_path.is_dir():
            logger.info(f"Processing directory: {input_path}")
            all_text = []
            image_files = list(input_path.glob('*.{jpg,jpeg,png,tif,tiff,pdf}'))
            
            if not image_files:
                logger.warning("No image or PDF files found in the directory")
                return
                
            for img_path in sorted(image_files):
                logger.info(f"Processing {img_path}")
                text = process_image(img_path)
                all_text.append(text)
            create_pdf('\n\n'.join(all_text), output_path)
        
        logger.info("Conversion completed successfully!")
        return
        
    except Exception as e:
        logger.error(f"Conversion failed: {str(e)}")
        raise click.ClickException(str(e))

if __name__ == '__main__':
    try:
        main(standalone_mode=False)
        sys.exit(0)
    except click.exceptions.Exit:
        sys.exit(0)
    except Exception as e:
        logger.error(f"Program failed: {str(e)}")
        sys.exit(1)
