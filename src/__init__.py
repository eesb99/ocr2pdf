"""OCR to PDF conversion package."""

from .form_handler import FormProcessor
from .pdf_handler import PDFHandler
from .ocr_handler import OCRHandler

__version__ = "1.0.0"
__all__ = ["FormProcessor", "PDFHandler", "OCRHandler"]

# src/__init__.py - with complete workflow implementation

import logging
from pathlib import Path
import argparse
from typing import Optional, Tuple

from .pdf_handler import PDFHandler
from .ocr_handler import OCRHandler
from .form_handler import FormProcessor
from config.settings import get_config

logging.basicConfig(
   level=logging.INFO,
   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FormProcessor:
   """Main class to orchestrate form processing workflow"""
   
   def __init__(self):
       self.pdf_handler = PDFHandler()
       self.ocr_handler = OCRHandler()
       self.config = get_config()
       
   def process_form(self, input_path: str, output_path: str) -> bool:
       """
       Main workflow to process form
       
       Args:
           input_path: Path to input PDF
           output_path: Path to save digital output
           
       Returns:
           bool: True if successful, False otherwise
       """
       try:
           # Step 1: Read PDF
           logger.info(f"Reading PDF: {input_path}")
           if not self.pdf_handler.read_pdf(input_path):
               return False
               
           # Step 2: Process each page
           page_images = self.pdf_handler.get_page_images()
           
           for idx, image in enumerate(page_images):
               logger.info(f"Processing page {idx + 1}")
               
               # Process image with OCR
               text = self.ocr_handler.process_image(image)
               if text:
                   logger.info(f"Extracted text: {text[:100]}...")
           
           # Step 3: Save processed PDF
           if not self.pdf_handler.save_pdf(output_path):
               logger.error("Failed to save processed PDF")
               return False
               
           logger.info("Form processing completed successfully")
           return True
           
       except Exception as e:
           logger.error(f"Error in form processing: {str(e)}")
           return False

   def validate_form(self, pdf_path: str) -> bool:
       """
       Validate form structure
       
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
           logger.error(f"Form validation failed: {str(e)}")
           return False

   def get_form_info(self, pdf_path: str) -> dict:
       """
       Get form information
       
       Args:
           pdf_path: Path to PDF file
           
       Returns:
           dict: Form information
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
           logger.error(f"Failed to get form info: {str(e)}")
           return {}

def process_pdf(input_file: str, output_file: str) -> bool:
   """
   Process single PDF file
   
   Args:
       input_file: Input PDF path
       output_file: Output PDF path
       
   Returns:
       bool: True if successful, False otherwise
   """
   processor = FormProcessor()
   return processor.process_form(input_file, output_file)

def main():
   """CLI entry point"""
   parser = argparse.ArgumentParser(description='Process PDF forms')
   parser.add_argument('input', help='Input PDF file')
   parser.add_argument(
       '-o', 
       '--output',
       help='Output PDF file (default: input_digital.pdf)'
   )
   
   args = parser.parse_args()
   
   # Handle output path
   output_path = args.output
   if not output_path:
       input_path = Path(args.input)
       output_path = str(input_path.parent / f"{input_path.stem}_digital.pdf")
   
   # Process the form
   if process_pdf(args.input, output_path):
       logger.info("PDF processing completed successfully")
   else:
       logger.error("PDF processing failed")
       exit(1)

if __name__ == "__main__":
   main()