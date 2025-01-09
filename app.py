from pathlib import Path
from PyPDF2 import PdfReader
import fitz
import re
from markitdown import MarkItDown


source_folder = Path("./pdfs")
destination_folder = Path("./output")

# Ensure the destination folder exists
destination_folder.mkdir(parents=True, exist_ok=True)

# Function to extract text from a PDF and write it to a text file
def extract_text_to_file(pdf_path, output_path):
    try:
        reader = PdfReader(pdf_path)
        with open(output_path, "w", encoding="utf-8") as output_file:
            for page in reader.pages:
                output_file.write(page.extract_text())
        print(f"Extracted text from {pdf_path.name} to {output_path.name}")
    except Exception as e:
        print(f"Failed to process {pdf_path.name}: {e}")

# Iterate over PDF files in the source folder
for pdf_file in source_folder.iterdir():
    if pdf_file.is_file() and pdf_file.suffix.lower() == ".pdf":
        # Define the output text file path
        output_file_path = destination_folder / (pdf_file.stem + ".txt")
        # Extract text and save to the text file
        extract_text_to_file(pdf_file, output_file_path)

# Initialize a set to store unique codes
codigo_set = set()

# Regex pattern to match "Código"
codigo_pattern = re.compile(r"^\d{9}$", re.MULTILINE)

# Process each text file in the folder
for txt_file in destination_folder.glob("*.txt"):
    with open(txt_file, "r", encoding="utf-8") as file:
        content = file.read()
        # Find all matches for "Código" pattern
        codigos = codigo_pattern.findall(content)
        codigo_set.update(codigos)

print(codigo_set)
# print(f"Extracted {len(codigo_set)} unique 'Código' entries.")


for pdf_file in source_folder.iterdir():
    if pdf_file.is_file() and pdf_file.suffix.lower() == ".pdf":
        # Define the output text file path
        # output_file_path = destination_folder / (pdf_file.stem + ".txt")
        doc = fitz.open(pdf_file)
        # Iterate through pages and save as HTML
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            html_content = page.get_text("html")
            
            # Save the HTML content to a file
            with open(f"page_{page_num + 1}.html", "w", encoding="utf-8") as html_file:
                html_file.write(html_content)

        print("Conversion complete!")

