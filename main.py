from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import tempfile
import shutil
from typing import List
from datetime import datetime
import uvicorn


from span_extractor import extract_spans
from ocr_fallback import ocr_extract
from font_stats_analyzer import analyze_fonts, add_caps_ratio
from outline_generator import generate_outline, extract_title

app = FastAPI(
    title="PDF Outline Extractor API",
    description="Extract document outlines and titles from PDF files with multilingual OCR support",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def process_pdf_file(pdf_path: str) -> dict:
    """Process a single PDF file and return outline"""
    try:
        spans = extract_spans(pdf_path)
        if not spans:
            raise ValueError("No spans extracted — fallback to OCR")
    except Exception as e:
        print(f" Falling back to OCR for {pdf_path} due to: {e}")
        spans = ocr_extract(pdf_path)

    body_size, font_stats = analyze_fonts(spans)
    spans = add_caps_ratio(spans)
    outline = generate_outline(spans, body_size)
    title = extract_title(outline or [])

    return {
        "title": title,
        "outline": outline,
        "processing_info": {
            "total_spans": len(spans),
            "body_font_size": body_size,
            "outline_items": len(outline) if outline else 0,
            "processed_at": datetime.now().isoformat()
        }
    }


@app.get("/")
async def root():

    return {
        "service": "PDF Outline Extractor API",
        "version": "2.0.0",
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health",
            "extract_single": "POST /extract-outline/",
            "extract_batch": "POST /batch-extract/",
            "languages": "/supported-languages"
        }
    }


@app.post("/extract-outline/")
async def extract_outline(file: UploadFile = File(...)):

    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")

    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_path = temp_file.name

    try:
        result = process_pdf_file(temp_path)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
    finally:
        if os.path.exists(temp_path):
            os.unlink(temp_path)


@app.post("/batch-extract/")
async def batch_extract(files: List[UploadFile] = File(...)):

    results = {}
    errors = {}

    for file in files:
        if not file.filename.lower().endswith('.pdf'):
            errors[file.filename] = "Not a PDF file"
            continue

        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name

        try:
            result = process_pdf_file(temp_path)
            results[file.filename] = result
        except Exception as e:
            errors[file.filename] = str(e)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    return JSONResponse(content={
        "results": results,
        "errors": errors,
        "summary": {
            "successful": len(results),
            "failed": len(errors),
            "total": len(files)
        }
    })


@app.get("/health")
async def health_check():

    return {
        "status": "healthy",
        "service": "PDF Outline Extractor",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/supported-languages")
async def supported_languages():

    return {
        "languages": [
            {"code": "eng", "name": "English"},
            {"code": "fra", "name": "French"},
            {"code": "deu", "name": "German"},
            {"code": "spa", "name": "Spanish"},
            {"code": "ita", "name": "Italian"},
            {"code": "por", "name": "Portuguese"},
            {"code": "rus", "name": "Russian"},
            {"code": "ara", "name": "Arabic"},
            {"code": "chi_sim", "name": "Chinese (Simplified)"},
            {"code": "chi_tra", "name": "Chinese (Traditional)"},
            {"code": "jpn", "name": "Japanese"},
            {"code": "kor", "name": "Korean"},
            {"code": "hin", "name": "Hindi"}
        ],
        "total": 13
    }


def main():

    print("\n" + "=" * 60)
    print(" PDF Outline Extractor API Starting...")
    print("=" * 60)
    print(f" Server: http://localhost:8000")
    print(f" API Docs: http://localhost:8000/docs")
    print(f" ReDoc: http://localhost:8000/redoc")
    print(f" Health: http://localhost:8000/health")
    print("=" * 60 + "\n")

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )


if __name__ == "__main__":
    main()