# heading_scorer.py
import re

def score_heading(span, body_size):
    score = 0
    text = span["text"].strip()

    # Boost for size larger than body
    if span["size"] > body_size:
        score += (span["size"] - body_size)

    # Boost for bold
    if span.get("font") and "bold" in span["font"].lower():
        score += 2

    # Boost for high caps ratio
    if span.get("caps_ratio", 0) > 0.6:
        score += 1.5

    # for heading-like patterns
    if re.match(r"^\d+(\.\d+)*\s", text):  # number-dot heading
        score += 2
    if re.match(r"^[IVXLC]+\.", text):  # roman numeral heading
        score += 1.5
    if re.match(r"^[A-Z][a-z]+\s[A-Z][a-z]+", text):  # title case
        score += 1.2

    return score

def is_valid_heading_text(text):
    text = text.strip()
    if not text or len(text) < 3:
        return False
    if len(text.split()) > 15:
        return False
    if text.endswith(".") and len(text.split()) > 6:
        return False
    if re.match(r"^[\W_]+$", text):
        return False
    if not re.search(r"[a-zA-Z0-9]", text):
        return False
    if text.count(" ") >= 10:
        return False
    return True

def assign_heading_level(span, score):
    if score > 8:
        return "H1"
    elif score > 6:
        return "H2"
    elif score > 3:
        return "H3"
    return None
