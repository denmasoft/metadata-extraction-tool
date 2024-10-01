class SEOCheckerError(Exception):
    """Base exception for SEO Checker"""
    pass

class URLFetchError(SEOCheckerError):
    """Raised when unable to fetch URL"""
    pass

class ParsingError(SEOCheckerError):
    """Raised when unable to parse HTML content"""
    pass
