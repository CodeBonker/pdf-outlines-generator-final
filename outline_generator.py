# outline_generator.py
from heading_scorer import score_heading, assign_heading_level, is_valid_heading_text

def generate_outline(spans, body_size):
    outline = []

    for span in spans:
        score = score_heading(span, body_size)
        level = assign_heading_level(span, score)

        if level and is_valid_heading_text(span["text"]):
            outline.append({
                "level": level,
                "text": span["text"].strip(),
                "page": span["page"]
            })

    return merge_consecutive_h1s(outline)

def extract_title(outline):
    page1_titles = [item["text"].strip() for item in outline if item["level"] == "H1" and item["page"] == 1]
    return " ".join(page1_titles).strip()

def merge_consecutive_h1s(outline):
    merged = []
    i = 0
    while i < len(outline):
        curr = outline[i]
        if curr["level"] == "H1":
            text = curr["text"]
            page = curr["page"]
            j = i + 1
            while j < len(outline) and outline[j]["level"] == "H1" and outline[j]["page"] == page:
                text += " " + outline[j]["text"]
                j += 1
            merged.append({"level": "H1", "text": text.strip(), "page": page})
            i = j
        else:
            merged.append(curr)
            i += 1
    return merged