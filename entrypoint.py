# entrypoint.py
import os
import json
from span_extractor import extract_spans
from ocr_fallback import ocr_extract
from font_stats_analyzer import analyze_fonts, add_caps_ratio
from outline_generator import generate_outline, extract_title

import os

INPUT_DIR = os.getenv("INPUT_DIR", "input")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")


def process_pdf(pdf_path, output_path):
    try:
        spans = extract_spans(pdf_path)
        if not spans:
            raise ValueError("No spans extracted — fallback to OCR")
    except Exception as e:
        print(f"Falling back to OCR for {pdf_path} due to: {e}")
        spans = ocr_extract(pdf_path)

    body_size, _ = analyze_fonts(spans)
    spans = add_caps_ratio(spans)
    outline = generate_outline(spans, body_size)
    title = extract_title(outline or [])

    result = {
        "title": title,
        "outline": outline
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"Saved: {output_path}")

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(INPUT_DIR, filename)
            json_filename = os.path.splitext(filename)[0] + ".json"
            output_path = os.path.join(OUTPUT_DIR, json_filename)
            print(f"Processing: {filename}")
            process_pdf(pdf_path, output_path)

if __name__ == "__main__":
    main()
