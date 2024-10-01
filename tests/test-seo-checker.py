import pytest
from src.seo_checker import SEOChecker, SEOMetadata
from src.exceptions import URLFetchError, ParsingError
from src.security_utils import SecurityBypass, RequestManager

def test_security_bypass_user_agent():
    security = SecurityBypass()
    user_agent = security.get_random_user_agent()
    assert isinstance(user_agent, str)
    assert len(user_agent) > 0

def test_request_manager_retry_logic(mocker):
    mock_security = mocker.Mock()
    mock_security.get_with_cloudscraper.return_value = None
    mock_security.get_with_selenium.return_value = "Test content"
    
    manager = RequestManager()
    manager.security = mock_security
    
    content = manager.get_page_content("https://example.com")
    
    assert content == "Test content"
    assert mock_security.get_with_cloudscraper.called
    assert mock_security.get_with_selenium.called

def test_seo_checker_with_security(mocker):
    mock_request_manager = mocker.Mock()
    mock_request_manager.get_page_content.return_value = """
    <html>
        <head>
            <title>Test Title</title>
            <meta name="description" content="Test Description">
        </head>
        <body>
            <h1>Test H1</h1>
        </body>
    </html>
    """
    
    checker = SEOChecker()
    checker.request_manager = mock_request_manager
    
    metadata = checker.extract_metadata('https://example.com')
    
    assert metadata.title == 'Test Title'
    assert metadata.meta_description == 'Test Description'
    assert metadata.h1_tags == ['Test H1']

def test_security_bypass_all_methods_fail(mocker):
    mock_security = mocker.Mock()
    mock_security.get_with_cloudscraper.return_value = None
    mock_security.get_with_selenium.return_value = None
    
    manager = RequestManager()
    manager.security = mock_security
    
    content = manager.get_page_content("https://example.com")
    
    assert content is None
    assert mock_security.get_with_cloudscraper.call_count == 3
    assert mock_security.get_with_selenium.call_count == 3
