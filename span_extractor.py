
import fitz  # PyMuPDF
import logging

def extract_spans(pdf_path):
    spans = []
    doc = fitz.open(pdf_path)
    for page_num, page in enumerate(doc):
        width, height = page.rect.width, page.rect.height
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block["type"] == 0:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if not text:
                            continue
                        spans.append({
                            "text": text,
                            "size": span["size"],
                            "font": span["font"],
                            "flags": span["flags"],
                            "x0": span["bbox"][0],
                            "y0": span["bbox"][1],
                            "x1": span["bbox"][2],
                            "y1": span["bbox"][3],
                            "width": width,
                            "height": height,
                            "page": page_num + 1,
                        })
                        logging.debug(f"[DEBUG] Found span: {text}")
    return spans