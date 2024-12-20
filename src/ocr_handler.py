"""OCR processing module."""

from typing import Dict, Optional, List
import logging
from PIL import Image
import pytesseract
from pathlib import Path
import os

logger = logging.getLogger(__name__)

# Set Tesseract path for Windows
if os.name == 'nt':  # Windows
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class OCRHandler:
    """Handles OCR operations."""

    def __init__(self, lang: str = "eng") -> None:
        """
        Initialize OCR handler.

        Args:
            lang: Language for OCR (default: eng)
        """
        self.lang = lang
        self._verify_tesseract()

    def _verify_tesseract(self) -> None:
        """Verify Tesseract installation."""
        try:
            pytesseract.get_tesseract_version()
        except Exception as e:
            logger.error(f"Tesseract not properly installed: {e}")
            raise RuntimeError("Tesseract OCR is not properly installed")

    def process_image(self, image: Image.Image) -> str:
        """
        Process image with OCR.

        Args:
            image: PIL Image to process

        Returns:
            str: Extracted text
        """
        try:
            # Convert to grayscale
            gray_image = image.convert('L')
            
            # Configure OCR
            custom_config = r'--oem 3 --psm 6'
            
            # Extract text
            text = pytesseract.image_to_string(
                gray_image,
                lang=self.lang,
                config=custom_config
            )
            return text.strip()
        except Exception as e:
            logger.error(f"OCR processing failed: {e}")
            return ""

    def get_text_blocks(self, image: Image.Image) -> List[Dict]:
        """
        Get text blocks with positions.

        Args:
            image: PIL Image to process

        Returns:
            List[Dict]: List of text blocks with positions
        """
        try:
            # Convert to grayscale
            gray_image = image.convert('L')
            
            data = pytesseract.image_to_data(
                gray_image,
                lang=self.lang,
                output_type=pytesseract.Output.DICT
            )
            
            blocks = []
            for i in range(len(data['text'])):
                if int(data['conf'][i]) > 60:  # Confidence threshold
                    block = {
                        'text': data['text'][i],
                        'conf': data['conf'][i],
                        'x': data['left'][i],
                        'y': data['top'][i],
                        'w': data['width'][i],
                        'h': data['height'][i]
                    }
                    blocks.append(block)
            
            return blocks
        except Exception as e:
            logger.error(f"Failed to get text blocks: {e}")
            return []