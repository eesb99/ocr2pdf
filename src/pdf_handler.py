"""PDF handling module."""

from typing import Dict, Optional, List
from pathlib import Path
import logging
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import io

logger = logging.getLogger(__name__)

class PDFHandler:
    """Handles PDF file operations."""

    def __init__(self) -> None:
        """Initialize PDF handler."""
        self.reader: Optional[PdfReader] = None
        self.writer = PdfWriter()
        self.page_images: List[Image.Image] = []

    def read_pdf(self, pdf_path: str) -> bool:
        """
        Read a PDF file and convert pages to images.

        Args:
            pdf_path: Path to PDF file

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            path = Path(pdf_path)
            if not path.exists():
                logger.error(f"File not found: {pdf_path}")
                return False

            if not path.suffix.lower() == '.pdf':
                logger.error(f"Not a PDF file: {pdf_path}")
                return False

            # Read the PDF file
            self.reader = PdfReader(pdf_path)
            
            # Convert pages to images for OCR
            for page_num in range(len(self.reader.pages)):
                page = self.reader.pages[page_num]
                
                # Extract each image resource from the page
                for image_file_object in page.images:
                    image = Image.open(io.BytesIO(image_file_object.data))
                    self.page_images.append(image)
            
            logger.info(f"Successfully read PDF: {pdf_path} with {len(self.page_images)} pages")
            return True
            
        except Exception as e:
            logger.error(f"Error reading PDF: {str(e)}")
            return False

    def get_form_fields(self) -> Dict:
        """
        Get form fields from PDF.

        Returns:
            Dict: Dictionary of form fields
        """
        if not self.reader:
            return {}
        return self.reader.get_form_text_fields()

    def save_pdf(self, output_path: str) -> bool:
        """
        Save PDF to file.

        Args:
            output_path: Path to save PDF

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create new PDF with digital content
            for page in self.reader.pages:
                self.writer.add_page(page)
            
            # Save the new PDF
            with open(output_path, "wb") as output_file:
                self.writer.write(output_file)
            return True
        except Exception as e:
            logger.error(f"Failed to save PDF: {e}")
            return False

    def get_page_images(self) -> List[Image.Image]:
        """
        Get list of page images.

        Returns:
            List[Image.Image]: List of page images
        """
        return self.page_images