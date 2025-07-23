import pdfplumber
import fitz  # PyMuPDF
import os
import shutil
from pathlib import Path
from langchain.schema import Document
from PIL import Image
import pytesseract

# Tesseract OCR path (make sure it's installed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" 

def is_valid_table_cell(cell):
    return str(cell) if cell is not None else ""


def extract_from_pdf(
    pdf_path: str,
    image_output_dir: str = r"C:\Users\rudra\Desktop\hackathon\extracted_images"
) -> list[Document]:
    # 🧹 Clean old image folder if it exists
    if os.path.exists(image_output_dir):
        shutil.rmtree(image_output_dir)
    os.makedirs(image_output_dir, exist_ok=True)

    text_docs = []
    table_docs = []
    image_docs = []

    # === STEP 1: Text + Table Extraction using pdfplumber ===
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_number = i + 1

            # TEXT
            text = page.extract_text()
            if text:
                text_docs.append(Document(
                    page_content=text,
                    metadata={"page": page_number, "type": "text", "source": pdf_path}
                ))

            # TABLES
            tables = page.extract_tables()
            for table in tables:
                table_text = "\n".join([
                    " | ".join([is_valid_table_cell(cell) for cell in row])
                    for row in table if row
                ])
                table_docs.append(Document(
                    page_content=table_text,
                    metadata={"page": page_number, "type": "table", "source": pdf_path}
                ))

    # === STEP 2: Image Extraction using PyMuPDF + OCR ===
    doc = fitz.open(pdf_path)
    for page_num in range(len(doc)):
        page = doc[page_num]
        images = page.get_images(full=True)

        for j, img in enumerate(images):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_path = os.path.join(image_output_dir, f"page{page_num+1}_img{j}.{image_ext}")

            with open(image_path, "wb") as f:
                f.write(image_bytes)

            # OCR text extraction
            try:
                ocr_text = pytesseract.image_to_string(Image.open(image_path))
                if ocr_text.strip():
                    image_docs.append(Document(
                        page_content=ocr_text.strip(),
                        metadata={"page": page_num + 1, "type": "image", "source": pdf_path}
                    ))
            except Exception as e:
                print(f"⚠️ Error processing {image_path}: {e}")
                
    # print(f"text Docs : {text_docs}\n\n")
    print(f"table_docs: {table_docs}\n\n")
    # print(f"image_docs: {image_docs}\n\n")
    return text_docs + table_docs + image_docs


def extract_from_pdf_folder(
    folder_path: str,
    image_output_base_dir: str = r"C:\Users\rudra\Desktop\hackathon\extracted_images"
) -> list[Document]:
    all_documents = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            # Unique image folder per PDF
            pdf_name = os.path.splitext(filename)[0]
            image_output_dir = os.path.join(image_output_base_dir, pdf_name)

            print(f"\n📄 Processing: {filename}")
            try:
                docs = extract_from_pdf(pdf_path, image_output_dir=image_output_dir)
                all_documents.extend(docs)
            except Exception as e:
                print(f"❌ Error processing {filename}: {e}")

    return all_documents
