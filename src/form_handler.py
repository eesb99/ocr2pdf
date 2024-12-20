# src/form_handler.py - with implemented form processing functionality

"""Form processing module."""

from typing import Dict, Optional
import logging
from pathlib import Path
from .pdf_handler import PDFHandler
from .ocr_handler import OCRHandler

logger = logging.getLogger(__name__)

class FormProcessor:
    """Main form processing class."""

    def __init__(self, lang: str = "eng") -> None:
        """
        Initialize form processor.

        Args:
            lang: Language for OCR (default: eng)
        """
        self.pdf_handler = PDFHandler()
        self.ocr_handler = OCRHandler(lang=lang)

    def process_form(self, input_path: str, output_path: str) -> bool:
        """
        Process form from input path to output path.

        Args:
            input_path: Path to input PDF
            output_path: Path to save processed PDF

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Read PDF and convert to images
            if not self.pdf_handler.read_pdf(input_path):
                return False

            # Process each page image with OCR
            for image in self.pdf_handler.get_page_images():
                text = self.ocr_handler.process_image(image)
                if text:
                    logger.info(f"Extracted text: {text[:100]}...")

            # Save processed PDF
            return self.pdf_handler.save_pdf(output_path)

        except Exception as e:
            logger.error(f"Form processing failed: {e}")
            return False

    def validate_form(self, pdf_path: str) -> bool:
        """
        Validate form structure.

        Args:
            pdf_path: Path to PDF file

        Returns:
            bool: True if valid, False otherwise
        """
        try:
            if not self.pdf_handler.read_pdf(pdf_path):
                return False

            fields = self.pdf_handler.get_form_fields()
            return len(fields) > 0

        except Exception as e:
            logger.error(f"Form validation failed: {e}")
            return False

    def get_form_info(self, pdf_path: str) -> Dict:
        """
        Get form information.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Dict: Form information
        """
        try:
            if not self.pdf_handler.read_pdf(pdf_path):
                return {}

            fields = self.pdf_handler.get_form_fields()
            return {
                "fields": fields,
                "form_type": "fillable" if fields else "scanned",
                "pages": len(self.pdf_handler.reader.pages) if self.pdf_handler.reader else 0,
                "images": len(self.pdf_handler.get_page_images())
            }

        except Exception as e:
            logger.error(f"Failed to get form info: {e}")
            return {}