import asyncio
import io
from PIL import Image
import pytesseract
from langdetect import detect
import docx2txt
import fitz  # PyMuPDF
import os
import shutil


class TextExtractor:
    @staticmethod
    async def extract_text_from_uploaded_file(uploaded_file):
        loop = asyncio.get_event_loop()
        if uploaded_file.type == "application/pdf":
            return await loop.run_in_executor(None, TextExtractor._process_pdf, uploaded_file)
        elif uploaded_file.type in ["application/msword",
                                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            return await loop.run_in_executor(None, TextExtractor._process_docx, uploaded_file)
        elif uploaded_file.type in ["text/plain", "text/markdown"]:
            return await loop.run_in_executor(None, TextExtractor._process_text, uploaded_file)
        return "", "und"

    @staticmethod
    def _process_pdf(uploaded_file):
        text = ''
        bytes_data = uploaded_file.read()
        with fitz.open(stream=bytes_data, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
                image_list = page.get_images(full=True)
                for image_index in image_list:
                    xref = image_index[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image = Image.open(io.BytesIO(image_bytes))
                    text += pytesseract.image_to_string(image)
        language = detect(text) if text else "und"
        return text, language

    @staticmethod
    def _process_docx(uploaded_file):
        text = ''
        bytes_data = uploaded_file.read()
        temp_dir = "temp_docx"
        os.makedirs(temp_dir, exist_ok=True)
        temp_file_path = os.path.join(temp_dir, uploaded_file.name)
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(bytes_data)
        text = docx2txt.process(temp_file_path, temp_dir)
        shutil.rmtree(temp_dir)
        language = detect(text) if text else "und"
        return text, language

    @staticmethod
    def _process_text(uploaded_file):
        text = uploaded_file.read().decode('utf-8')
        language = detect(text) if text else "und"
        return text, language

    @staticmethod
    async def extract_text_from_uploaded_image(uploaded_image):
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, TextExtractor._process_image, uploaded_image)

    @staticmethod
    def _process_image(uploaded_image):
        image = Image.open(io.BytesIO(uploaded_image.getvalue()))
        text = pytesseract.image_to_string(image)
        language = detect(text) if text else "und"
        return text, language
