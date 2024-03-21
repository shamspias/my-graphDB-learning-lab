import asyncio
import io
import os
from PIL import Image
import pytesseract
from langdetect import detect
import docx2txt
import fitz  # PyMuPDF


class TextExtractor:
    @staticmethod
    async def extract_text_from_file_path(file_path):
        loop = asyncio.get_event_loop()
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == ".pdf":
            return await loop.run_in_executor(None, TextExtractor._process_pdf_with_ocr, file_path)
        elif file_extension in [".doc", ".docx"]:
            return await loop.run_in_executor(None, TextExtractor._process_docx, file_path)
        elif file_extension in [".txt", ".md"]:
            return await loop.run_in_executor(None, TextExtractor._process_text, file_path)
        else:
            return "", "und"

    @staticmethod
    def _process_pdf_with_ocr(file_path):
        text = ''
        with fitz.open(file_path) as doc:
            for page_num, page in enumerate(doc):
                # Extract text from the page.
                page_text = page.get_text()
                text += page_text

                # Now process images within the page, if any.
                image_list = page.get_images(full=True)
                if image_list:  # Only if there are images on the page
                    text += "\n"  # Ensure separation from the page text
                for image_index in image_list:
                    xref = image_index[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    # Use PIL to open the image in memory
                    image = Image.open(io.BytesIO(image_bytes))
                    # Apply OCR to the image
                    image_text = pytesseract.image_to_string(image, lang='eng')
                    # Append OCR text immediately after the image is processed
                    text += image_text

        language = detect(text) if text else "und"
        return text, language

    @staticmethod
    def _process_docx(file_path):
        text = docx2txt.process(file_path)
        language = detect(text) if text else "und"
        return text, language

    @staticmethod
    def _process_text(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        language = detect(text) if text else "und"
        return text, language

    @staticmethod
    async def extract_text_from_uploaded_image(image_path):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, TextExtractor._process_image_with_ocr, image_path)

    @staticmethod
    def _process_image_with_ocr(image_path):
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        language = detect(text) if text else "und"
        return text, language
