FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    pkg-config \
    poppler-utils \
    tesseract-ocr \

    tesseract-ocr-eng \
    tesseract-ocr-fra \
    tesseract-ocr-deu \
    tesseract-ocr-spa \
    tesseract-ocr-ita \
    tesseract-ocr-por \
    tesseract-ocr-rus \
    tesseract-ocr-ara \
    tesseract-ocr-chi-sim \
    tesseract-ocr-chi-tra \
    tesseract-ocr-jpn \
    tesseract-ocr-kor \
    tesseract-ocr-hin \

    tesseract-ocr-nld \
    tesseract-ocr-pol \
    tesseract-ocr-tur \
    tesseract-ocr-tha \
    tesseract-ocr-vie \

    libtesseract-dev \
    libleptonica-dev \
    libpoppler-cpp-dev \
    libgomp1 \

    wget \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

WORKDIR /app

RUN mkdir -p /app/input /app/output && \
    chmod 755 /app/input /app/output


COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip wheel setuptools && \
    pip install --no-cache-dir -r requirements.txt


COPY *.py ./

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata/

RUN tesseract --list-langs

CMD ["python", "entrypoint.py"]