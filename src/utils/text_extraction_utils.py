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
    async def extract_text_from_file_path(file_path):
        loop = asyncio.get_event_loop()
        file_extension = os.path.splitext(file_path)[1].lower()
        if file_extension == ".pdf":
            return await loop.run_in_executor(None, TextExtractor._process_pdf, file_path)
        elif file_extension in [".doc", ".docx"]:
            return await loop.run_in_executor(None, TextExtractor._process_docx, file_path)
        elif file_extension in [".txt", ".md"]:
            return await loop.run_in_executor(None, TextExtractor._process_text, file_path)
        return "", "und"

    @staticmethod
    def _process_pdf(file_path):
        text = ''
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
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
