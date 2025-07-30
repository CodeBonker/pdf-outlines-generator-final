
import re
import unicodedata


def score_heading(span, body_size):
    """Score a text span for heading likelihood - multilingual enhanced."""
    score = 0
    text = span["text"].strip()

    # Boost for size larger than body
    if span["size"] > body_size:
        score += (span["size"] - body_size)

    # Boost for bold
    if span.get("font") and "bold" in span["font"].lower():
        score += 2

    # Boost for high caps ratio (works for Latin scripts)
    if span.get("caps_ratio", 0) > 0.6:
        score += 1.5

    # Enhanced pattern matching for different languages/scripts

    # English/Western patterns
    if re.match(r"^\d+(\.\d+)*\s", text):  # 1.1, 1.2.1
        score += 2
    if re.match(r"^[IVXLC]+\.", text):  # Roman numerals
        score += 1.5
    if re.match(r"^[A-Z][a-z]+\s[A-Z][a-z]+", text):  # Title case
        score += 1.2

    # Common heading keywords (multilingual)
    heading_keywords = [
        # English
        r"^(CHAPTER|SECTION|PART|APPENDIX|INTRODUCTION|CONCLUSION)\s+",
        # French
        r"^(CHAPITRE|SECTION|PARTIE|ANNEXE|INTRODUCTION|CONCLUSION)\s+",
        # German
        r"^(KAPITEL|ABSCHNITT|TEIL|ANHANG|EINLEITUNG|FAZIT)\s+",
        # Spanish
        r"^(CAPÍTULO|SECCIÓN|PARTE|APÉNDICE|INTRODUCCIÓN|CONCLUSIÓN)\s+",
        # Italian
        r"^(CAPITOLO|SEZIONE|PARTE|APPENDICE|INTRODUZIONE|CONCLUSIONE)\s+",
        # Portuguese
        r"^(CAPÍTULO|SEÇÃO|PARTE|APÊNDICE|INTRODUÇÃO|CONCLUSÃO)\s+",
    ]

    for pattern in heading_keywords:
        if re.match(pattern, text.upper()):
            score += 2.5
            break

    # Chinese/Japanese patterns
    if re.search(r"第[一二三四五六七八九十\d]+[章节條]", text):  # Chinese chapter/section
        score += 2.5
    if re.search(r"[一二三四五六七八九十]+[、．]", text):  # Chinese numbering
        score += 2

    # Arabic patterns
    if re.search(r"الفصل|الباب|القسم", text):  # Arabic chapter/section words
        score += 2.5
    if re.search(r"[٠-٩]+[\.:]", text):  # Arabic numerals
        score += 2

    # Russian/Cyrillic patterns
    if re.search(r"ГЛАВА|РАЗДЕЛ|ЧАСТЬ", text.upper()):  # Russian chapter words
        score += 2.5

    if re.match(r"^[A-ZÀ-ÿА-я\u4e00-\u9fff\u0600-\u06ff]{2,}\s*$", text) and len(text.strip()) > 2:
        score += 1.0
    word_count = len(text.split())
    if word_count > 12:
        score -= (word_count - 12) * 0.15

    return max(0, score)


def is_valid_heading_text(text):
    """Check if text is suitable for a heading - multilingual enhanced."""
    text = text.strip()
    if not text or len(text) < 2:  # Reduced minimum for single-character languages
        return False
    if len(text.split()) > 20:  # Increased for languages with longer phrases
        return False
    if text.endswith(".") and len(text.split()) > 8:  # Adjusted threshold
        return False
    if re.match(r"^[\W_]+$", text):
        return False

    # Enhanced alphanumeric check for different scripts
    if not re.search(
            r"[a-zA-Z0-9\u4e00-\u9fff\u0600-\u06ff\u0590-\u05ff\u0900-\u097f\u3040-\u309f\u30a0-\u30ff\u1100-\u11ff]",
            text):
        return False

    if text.count(" ") >= 15:  # Increased for languages with more words
        return False

    # Additional validations
    if len(text) > 150:  # Increased length limit
        return False
    if text.lower().startswith("page ") or text.lower().endswith(" page"):
        return False
    if re.search(r"页|頁|صفحة|página|pagina|seite|страница", text.lower()):  # Page indicators in different languages
        return False

    return True


def assign_heading_level(span, score):
    """Assign heading level based on score."""
    if score > 8:
        return "H1"
    elif score > 6:
        return "H2"
    elif score > 3:
        return "H3"
    return None


def get_text_script(text):
    """Detect the script/writing system of the text."""
    scripts = {}
    for char in text:
        if char.isalpha():
            script = unicodedata.name(char, '').split()[0]
            scripts[script] = scripts.get(script, 0) + 1

    if scripts:
        return max(scripts, key=scripts.get)
    return "LATIN"