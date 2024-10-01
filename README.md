# SEO Metadata Checker

A Python tool for extracting and analyzing SEO metadata from web pages.

## Features

- Extracts page titles, meta descriptions, and H1 tags
- Analyzes metadata for common SEO issues
- Exports results to CSV or JSON
- Comprehensive error handling
- Unit tests included

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

```python
from src.seo_checker import SEOChecker

checker = SEOChecker()
metadata = checker.extract_metadata('https://example.com')
analysis = checker.analyze_metadata(metadata)

print(f"Title: {metadata.title}")
print(f"Meta Description: {metadata.meta_description}")
print(f"H1 Tags: {metadata.h1_tags}")
print(f"Analysis: {analysis}")
```

## Running Tests

```
pytest tests/
```

## Project Structure
```
.
├── README.md
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── seo_checker.py
│   ├── exceptions.py
│   └── utils.py
└── tests
    ├── __init__.py
    └── test_seo_checker.py
```
