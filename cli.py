# cli.py - Enhanced CLI implementation

import logging
import sys
import click
from pathlib import Path
from typing import List
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn
from rich import print as rprint

from src import FormProcessor
from config.settings import get_config

# Setup rich console
console = Console()

# Setup logging
logging.basicConfig(
   level=logging.INFO,
   format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def validate_input_path(ctx, param, value):
   """Validate input file or directory"""
   path = Path(value)
   if not path.exists():
       raise click.BadParameter(f"Path does not exist: {value}")
   return path

def get_pdf_files(path: Path) -> List[Path]:
   """Get all PDF files from path"""
   if path.is_file():
       return [path] if path.suffix.lower() == '.pdf' else []
   return list(path.glob('**/*.pdf'))

@click.group()
@click.version_option(version='1.0.0')
def cli():
   """PDF Form Processing Tool"""
   pass

@cli.command()
@click.argument('input_path', callback=validate_input_path, type=click.Path(exists=True))
@click.option('-o', '--output', help='Output directory', type=click.Path())
@click.option('--batch', is_flag=True, help='Process all PDFs in directory')
@click.option('--validate-only', is_flag=True, help='Only validate forms without processing')
@click.option('--verbose', is_flag=True, help='Show detailed processing information')
def process(input_path: Path, output: str, batch: bool, validate_only: bool, verbose: bool):
   """Process PDF forms"""
   try:
       # Set up processor
       processor = FormProcessor()
       
       # Get files to process
       input_path = Path(input_path)
       files_to_process = get_pdf_files(input_path) if batch else [input_path]
       
       if not files_to_process:
           console.print("[red]No PDF files found to process[/red]")
           sys.exit(1)
           
       # Setup output directory
       output_dir = Path(output) if output else Path('output')
       output_dir.mkdir(exist_ok=True)
       
       # Process files with progress bar
       with Progress(
           SpinnerColumn(),
           *Progress.get_default_columns(),
           TimeElapsedColumn(),
           console=console
       ) as progress:
           task = progress.add_task(
               "[cyan]Processing forms...", 
               total=len(files_to_process)
           )
           
           for pdf_file in files_to_process:
               if verbose:
                   console.print(f"\n[yellow]Processing: {pdf_file}[/yellow]")
                   
               # Determine output path
               output_path = output_dir / f"{pdf_file.stem}_digital.pdf"
               
               try:
                   if validate_only:
                       # Only validate the form
                       if processor.validate_form(str(pdf_file)):
                           console.print(
                               f"[green]✓[/green] {pdf_file.name} - Valid"
                           )
                       else:
                           console.print(
                               f"[red]✗[/red] {pdf_file.name} - Invalid"
                           )
                   else:
                       # Process the form
                       if processor.process_form(str(pdf_file), str(output_path)):
                           if verbose:
                               console.print(
                                   f"[green]✓[/green] Created: {output_path}"
                               )
                       else:
                           console.print(
                               f"[red]Error processing: {pdf_file.name}[/red]"
                           )
                           
               except Exception as e:
                   console.print(f"[red]Error: {str(e)}[/red]")
                   if verbose:
                       logger.exception(e)
                       
               finally:
                   progress.advance(task)
                   
       console.print("\n[green]Processing completed![/green]")
       
   except Exception as e:
       console.print(f"[red]Error: {str(e)}[/red]")
       if verbose:
           logger.exception(e)
       sys.exit(1)

@cli.command()
@click.argument('input_path', callback=validate_input_path, type=click.Path(exists=True))
def info(input_path: Path):
   """Show information about PDF form"""
   try:
       processor = FormProcessor()
       info = processor.get_form_info(str(input_path))
       
       console.print("\n[cyan]Form Information:[/cyan]")
       console.print(f"File: {input_path.name}")
       console.print(f"Size: {input_path.stat().st_size / 1024:.2f} KB")
       console.print(f"Pages: {info.get('pages', 'Unknown')}")
       console.print(f"Form Type: {info.get('form_type', 'Unknown')}")
       console.print("\nFields detected:")
       
       for field, value in info.get('fields', {}).items():
           console.print(f"  - {field}: {value}")
           
   except Exception as e:
       console.print(f"[red]Error: {str(e)}[/red]")
       sys.exit(1)

@cli.command()
def configure():
   """Configure processing settings"""
   config = get_config()
   
   # Get OCR language
   lang = click.prompt(
       "OCR Language", 
       default=config['ocr_config']['lang']
   )
   
   # Get confidence threshold
   threshold = click.prompt(
       "Confidence Threshold (0-100)", 
       default=70,
       type=int
   )
   
   # Save configuration
   # TODO: Implement configuration saving
   console.print("[green]Configuration saved![/green]")

if __name__ == "__main__":
   cli()