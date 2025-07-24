import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import fitz  # PyMuPDF

def ocr_extract(pdf_path):
    images = convert_from_path(pdf_path, dpi=300)
    merged_spans = []

    for page_num, img in enumerate(images):
        ocr_text = pytesseract.image_to_string(img)
        lines = ocr_text.split("\n")

        buffer = []
        page = page_num + 1

        def flush_buffer():
            if buffer:
                line = " ".join(buffer).strip()
                letters = sum(1 for c in line if c.isalpha())
                caps = sum(1 for c in line if c.isupper())
                caps_ratio = caps / letters if letters > 0 else 0

                merged_spans.append({
                    "text": line,
                    "size": 20.0,
                    "font": "ocr",
                    "flags": 16 if line.isupper() else 0,
                    "caps_ratio": caps_ratio,
                    "x0": 0,
                    "y0": 0,
                    "x1": 0,
                    "y1": 0,
                    "width": img.width,
                    "height": img.height,
                    "page": page
                })

        for line in lines:
            line = line.strip()
            if not line:
                flush_buffer()
                buffer = []
                continue
            if line.endswith(".") or len(line.split()) > 5:
                buffer.append(line)
                flush_buffer()
                buffer = []
            else:
                buffer.append(line)

        flush_buffer()

    return merged_spans