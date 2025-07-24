# PDF Outline Extractor

A robust Python application that extracts document outlines and titles from PDF files using intelligent text analysis and OCR fallback capabilities.

## 🚀 Features

- **Smart Text Extraction**: Uses PyMuPDF for high-quality text extraction from PDFs
- **OCR Fallback**: Automatically falls back to Tesseract OCR for scanned or image-based PDFs  
- **Intelligent Heading Detection**: Advanced scoring algorithm to identify headings based on:
  - Font size relative to body text
  - Font weight (bold/normal)
  - Capitalization ratio
  - Heading patterns (numbered sections, Roman numerals, title case)
- **Hierarchical Outline Generation**: Creates structured outlines with H1, H2, H3 levels
- **Title Extraction**: Automatically extracts document titles from first page headings
- **Batch Processing**: Processes multiple PDFs in a single run
- **Docker Support**: Containerized for easy deployment and consistent environments

## 📋 Requirements

### System Dependencies
- Docker (Docker Desktop on Windows)
- Python 3.11+ (if running locally)

### Docker Dependencies (Included in Container)
- Tesseract OCR
- Poppler utilities
- PyMuPDF, pytesseract, pdf2image, pillow

## 🛠 Installation & Usage

### Docker Method (Recommended)

#### 1. Build the Docker Image
```bash
docker build --platform linux/amd64 -t pdf-outline-extractor:latest .
```

#### 2. Prepare Your PDFs
```bash
# Place PDF files in the input directory
cp your-document.pdf input/
```

#### 3. Run the Application

**For Windows (Git Bash/Command Prompt):**
```bash
docker run --rm -v "D:/path/to/your/project/input:/app/input" -v "D:/path/to/your/project/output:/app/output" --network none pdf-outline-extractor:latest
```

**For Linux/macOS:**
```bash
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none pdf-outline-extractor:latest
```

#### 4. Check Results
```bash
# List generated files
ls output/

# View a result file
cat output/your-document.json
```

### Local Installation (Alternative)

1. **Install system dependencies**:

   **Ubuntu/Debian**:
   ```bash
   sudo apt-get update
   sudo apt-get install -y poppler-utils tesseract-ocr tesseract-ocr-eng python3-dev gcc g++
   ```

   **macOS** (using Homebrew):
   ```bash
   brew install poppler tesseract
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run locally**:
   ```bash
   python entrypoint.py
   ```

## 📁 Project Structure

```
pdf-outline-extractor/
├── Dockerfile                # Docker build configuration
├── requirements.txt          # Python dependencies
├── entrypoint.py            # Main application entry point
├── span_extractor.py        # PDF text span extraction using PyMuPDF
├── ocr_fallback.py         # OCR fallback for scanned PDFs
├── font_stats_analyzer.py   # Font analysis and statistics
├── heading_scorer.py        # Heading detection and scoring algorithm
├── outline_generator.py     # Outline generation and title extraction
├── input/                   # Place PDF files here for processing
├── output/                  # Generated JSON outlines appear here
└── README.md               # This file
```

## 📊 Output Format

The application generates JSON files with the following structure:

```json
{
  "title": "Document Title Extracted from First Page",
  "outline": [
    {
      "level": "H1",
      "text": "Chapter 1: Introduction",
      "page": 1
    },
    {
      "level": "H2", 
      "text": "1.1 Overview",
      "page": 2
    },
    {
      "level": "H3",
      "text": "1.1.1 Background",
      "page": 2
    }
  ]
}
```

## ⚙️ Algorithm Details

### Heading Detection System

The heading scoring system uses multiple factors:

- **Font Size**: Headings typically use larger fonts than body text
- **Font Weight**: Bold text receives higher scores
- **Capitalization**: High ratio of capital letters indicates headings
- **Pattern Matching**: 
  - Numbered sections (1.1, 1.2.1)
  - Roman numerals (I., II., III.)
  - Title case patterns
  - Chapter/Section keywords

### Scoring Thresholds

- **H1**: Score > 8 (major headings)
- **H2**: Score > 6 (section headings) 
- **H3**: Score > 3 (subsection headings)

### Text Validation

Headings must meet criteria:
- Minimum 3 characters
- Maximum 15 words
- Contains alphanumeric characters
- Not just punctuation or whitespace
- Under 100 characters total

## 🐛 Troubleshooting

### Common Issues

1. **Docker Build Fails**:
   ```bash
   # Clean Docker cache and rebuild
   docker system prune -a
   docker build --platform linux/amd64 -t pdf-outline-extractor:latest . --no-cache
   ```

2. **"No spans extracted" Error**:
   - PDF might be scanned/image-based
   - Application automatically falls back to OCR
   - Check if file is a valid PDF

3. **Permission Errors (Windows)**:
   ```bash
   # Ensure Docker Desktop is running
   # Use full Windows paths in volume mounts
   docker run --rm -v "C:/full/path/to/input:/app/input" -v "C:/full/path/to/output:/app/output" --network none pdf-outline-extractor:latest
   ```

4. **Path Issues on Windows**:
   - Use absolute paths instead of relative paths
   - Replace forward slashes with backslashes if needed
   - Ensure Docker Desktop has access to the drive

5. **Empty Output**:
   - Check if PDF contains text (not just images)
   - Verify PDF is not password protected
   - Check input directory permissions

## 🔧 Customization

### Adjusting Heading Detection

Modify scoring parameters in `heading_scorer.py`:

```python
def score_heading(span, body_size):
    score = 0
    
    # Adjust these multipliers
    if span["size"] > body_size:
        score += (span["size"] - body_size) * 1.5  # Font size weight
    
    if span.get("font") and "bold" in span["font"].lower():
        score += 3  # Bold weight
    
    if span.get("caps_ratio", 0) > 0.6:
        score += 2  # Caps ratio weight
```

### Adding New Heading Patterns

Add patterns in `heading_scorer.py`:

```python
# Custom pattern matching
if re.match(r"^CHAPTER\s+\d+", text.upper()):
    score += 3
if re.match(r"^SECTION\s+[A-Z]", text.upper()):
    score += 2
```

## 📈 Performance

### Typical Processing Times

- **Text-based PDFs**: ~1-3 seconds per page
- **Scanned PDFs (OCR)**: ~5-15 seconds per page  
- **Mixed documents**: Varies based on OCR requirements

### Optimization Tips

- Use SSD storage for input/output directories
- Increase available RAM for large documents
- Process in batches for better resource utilization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [PyMuPDF](https://pymupdf.readthedocs.io/) for excellent PDF processing capabilities
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) for OCR functionality
- [pdf2image](https://github.com/Belval/pdf2image) for PDF to image conversion

---

**Ready to extract PDF outlines! 📄✨**