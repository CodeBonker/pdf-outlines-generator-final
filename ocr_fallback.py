
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import fitz


def detect_language(img):
    """Detect language of the document for better OCR"""
    try:

        langs = pytesseract.image_to_osd(img)

        return 'eng'
    except:
        return 'eng'  # Fallback to English


def ocr_extract(pdf_path, target_languages='eng+fra+deu+spa+ita+por+rus+ara+chi_sim+jpn+kor+hin'):
    """
    Extract text using OCR with multilingual support

    Args:
        pdf_path: Path to PDF file
        target_languages: Tesseract language codes separated by +
    """
    images = convert_from_path(pdf_path, dpi=300)
    merged_spans = []

    for page_num, img in enumerate(images):
        try:
            # Use multilingual OCR
            ocr_text = pytesseract.image_to_string(
                img,
                lang=target_languages,
                config='--psm 6'
            )
        except Exception as e:
            print(f"[⚠] Multilingual OCR failed, falling back to English: {e}")

            ocr_text = pytesseract.image_to_string(img, lang='eng')

        lines = ocr_text.split("\n")
        buffer = []
        page = page_num + 1

        def flush_buffer():
            if buffer:
                line = " ".join(buffer).strip()
                if not line:
                    return

                # Enhanced character counting for Unicode
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

            # Enhanced line breaking logic for different languages
            if line.endswith((".", "。", "！", "？", "।", "۔")) or len(line.split()) > 5:
                buffer.append(line)
                flush_buffer()
                buffer = []
            else:
                buffer.append(line)

        flush_buffer()

    return merged_spans


def ocr_extract_with_language_detection(pdf_path):
    """
    OCR extraction with automatic language detection
    """
    images = convert_from_path(pdf_path, dpi=300)
    if not images:
        return []

    detected_lang = detect_language(images[0])

    lang_mapping = {
        'eng': 'eng',
        'fra': 'fra',
        'deu': 'deu',
        'spa': 'spa',
        'ita': 'ita',
        'por': 'por',
        'rus': 'rus',
        'ara': 'ara',
        'chi': 'chi_sim+chi_tra',
        'jpn': 'jpn',
        'kor': 'kor',
        'hin': 'hin'
    }

    target_lang = lang_mapping.get(detected_lang, 'eng')
    print(f"[] Detected language: {detected_lang}, using OCR language: {target_lang}")

    return ocr_extract(pdf_path, target_lang)