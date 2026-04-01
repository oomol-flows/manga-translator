#region generated meta
import typing

class Inputs(typing.TypedDict):
    file_path: str

class Outputs(typing.TypedDict):
    images: list[str]
    format: str
    title: str | None
    author: str | None
    reading_order: str

#endregion

from oocana import Context
import os
import re
import zipfile
from pathlib import Path
import subprocess

# Image extensions to look for
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff', '.tif', '.avif'}

def get_file_format(file_path: str) -> str:
    """Determine file format from extension"""
    ext = Path(file_path).suffix.lower()
    format_map: dict[str, str] = {
        '.cbz': 'cbz',
        '.cbr': 'cbr',
        '.epub': 'epub',
        '.pdf': 'pdf',
        '.zip': 'zip'
    }
    return format_map.get(ext, 'unknown')

def natural_sort_key(s: str) -> list[int | str]:
    """Natural sorting key for filenames with numbers"""
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'([0-9]+)', s)]

def extract_images_from_zip(zip_path: str, output_dir: str) -> list[str]:
    """Extract images from a ZIP file (including CBZ)"""
    images: list[str] = []
    
    with zipfile.ZipFile(zip_path, 'r') as zf:
        # Get all image files
        image_files = [
            f for f in zf.namelist()
            if not f.endswith('/') and Path(f).suffix.lower() in IMAGE_EXTENSIONS
        ]
        
        # Sort by natural order (numeric sorting for filenames like 001.jpg, 002.jpg)
        image_files.sort(key=lambda x: natural_sort_key(Path(x).name))
        
        # Extract images
        for img_file in image_files:
            zf.extract(img_file, output_dir)
            images.append(os.path.join(output_dir, img_file))
    
    return images

def extract_from_epub(epub_path: str, output_dir: str) -> list[str]:
    """Extract images from EPUB file"""
    images: list[str] = []
    
    with zipfile.ZipFile(epub_path, 'r') as zf:
        # EPUB is a ZIP with specific structure
        # Images are usually in OPS/images/ or similar
        image_files = [
            f for f in zf.namelist()
            if not f.endswith('/') and Path(f).suffix.lower() in IMAGE_EXTENSIONS
        ]
        
        image_files.sort(key=lambda x: natural_sort_key(Path(x).name))
        
        for img_file in image_files:
            zf.extract(img_file, output_dir)
            images.append(os.path.join(output_dir, img_file))
    
    return images

async def main(params: Inputs, context: Context) -> Outputs:
    file_path = params["file_path"]
    
    if not os.path.exists(file_path):
        raise ValueError(f"File not found: {file_path}")
    
    file_format = get_file_format(file_path)
    
    if file_format == 'unknown':
        raise ValueError(f"Unsupported file format: {Path(file_path).suffix}")
    
    # Create session directory for extraction
    session_dir = context.session_dir
    extract_dir = os.path.join(session_dir, "extracted_images")
    os.makedirs(extract_dir, exist_ok=True)
    
    images = []
    title = None
    author = None
    reading_order = "to-right"  # Default reading order
    
    if file_format in ['zip', 'cbz']:
        # ZIP and CBZ can be extracted directly
        images = extract_images_from_zip(file_path, extract_dir)
        title = Path(file_path).stem
        
    elif file_format == 'epub':
        # EPUB is also a ZIP format
        images = extract_from_epub(file_path, extract_dir)
        title = Path(file_path).stem
        
    elif file_format == 'cbr':
        # CBR is RAR format - need unrar
        try:
            # Try using unrar command
            result = subprocess.run(
                ['unrar', 'x', '-o+', file_path, extract_dir],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                raise ValueError(f"Failed to extract CBR: {result.stderr}")
            
            # Collect extracted images
            for root, dirs, files in os.walk(extract_dir):
                for f in files:
                    if Path(f).suffix.lower() in IMAGE_EXTENSIONS:
                        images.append(os.path.join(root, f))
            
            images.sort(key=lambda x: natural_sort_key(Path(x).name))
            title = Path(file_path).stem
            
        except FileNotFoundError:
            raise ValueError("CBR format requires 'unrar' to be installed")
            
    elif file_format == 'pdf':
        # PDF requires pdf2image
        try:
            from pdf2image import convert_from_path
            
            pages = convert_from_path(file_path, dpi=150)
            
            for i, page in enumerate(pages):
                img_path = os.path.join(extract_dir, f"page_{i+1:04d}.jpg")
                page.save(img_path, 'JPEG')
                images.append(img_path)
            
            title = Path(file_path).stem
            
        except ImportError:
            raise ValueError("PDF format requires 'pdf2image' package. Install with: poetry add pdf2image")
    
    if not images:
        raise ValueError(f"No images found in {file_path}")
    
    return {
        "images": images,
        "format": file_format,
        "title": title,
        "author": author,
        "reading_order": reading_order
    }