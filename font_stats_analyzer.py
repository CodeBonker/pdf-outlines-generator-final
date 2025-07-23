from collections import Counter

def analyze_fonts(spans):
    sizes = [round(span["size"], 1) for span in spans if span.get("size")]
    freq = Counter(sizes)
    most_common = freq.most_common(1)
    body_size = most_common[0][0] if most_common else 12.0
    return body_size, freq

def add_caps_ratio(spans):
    for span in spans:
        text = span["text"]
        letters = sum(1 for c in text if c.isalpha())
        caps = sum(1 for c in text if c.isupper())
        span["caps_ratio"] = caps / letters if letters > 0 else 0
    return spans