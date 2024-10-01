from dataclasses import dataclass
from typing import Optional, List
from bs4 import BeautifulSoup
from loguru import logger
from .exceptions import URLFetchError, ParsingError
from .security_utils import RequestManager

@dataclass
class SEOMetadata:
    url: str
    title: Optional[str] = None
    meta_description: Optional[str] = None
    h1_tags: List[str] = None
    fetch_method: Optional[str] = None

    def __post_init__(self):
        self.h1_tags = self.h1_tags or []

class SEOChecker:
    def __init__(self, anticaptcha_key: Optional[str] = None):
        self.request_manager = RequestManager(anticaptcha_key)
    
    def fetch_url(self, url: str) -> str:
        content = self.request_manager.get_page_content(url)
        if not content:
            raise URLFetchError(f"Failed to fetch URL: {url}")
        return content

    def extract_metadata(self, url: str) -> SEOMetadata:
        html_content = self.fetch_url(url)
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            title = soup.title.string.strip() if soup.title else None
            
            meta_desc_tag = soup.find('meta', attrs={'name': 'description'})
            meta_description = meta_desc_tag['content'].strip() if meta_desc_tag else None
            
            h1_tags = [h1.get_text().strip() for h1 in soup.find_all('h1')]
            
            return SEOMetadata(
                url=url,
                title=title,
                meta_description=meta_description,
                h1_tags=h1_tags
            )
        except Exception as e:
            logger.error(f"Failed to parse HTML from {url}: {str(e)}")
            raise ParsingError(f"Failed to parse HTML: {str(e)}")

    def analyze_metadata(self, metadata: SEOMetadata) -> dict:
        analysis = {
            'title': {
                'present': metadata.title is not None,
                'length': len(metadata.title or ''),
                'issues': []
            },
            'meta_description': {
                'present': metadata.meta_description is not None,
                'length': len(metadata.meta_description or ''),
                'issues': []
            },
            'h1': {
                'count': len(metadata.h1_tags),
                'issues': []
            }
        }
        
        # Title analysis
        if not metadata.title:
            analysis['title']['issues'].append("Missing title tag")
        elif len(metadata.title) < 30:
            analysis['title']['issues'].append("Title too short (< 30 characters)")
        elif len(metadata.title) > 60:
            analysis['title']['issues'].append("Title too long (> 60 characters)")
        
        # Meta description analysis
        if not metadata.meta_description:
            analysis['meta_description']['issues'].append("Missing meta description")
        elif len(metadata.meta_description) < 120:
            analysis['meta_description']['issues'].append("Meta description too short (< 120 characters)")
        elif len(metadata.meta_description) > 160:
            analysis['meta_description']['issues'].append("Meta description too long (> 160 characters)")
        
        # H1 analysis
        if not metadata.h1_tags:
            analysis['h1']['issues'].append("Missing H1 tag")
        elif len(metadata.h1_tags) > 1:
            analysis['h1']['issues'].append("Multiple H1 tags found")
        
        return analysis