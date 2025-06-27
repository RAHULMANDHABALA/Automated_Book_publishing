from playwright.sync_api import sync_playwright
import os
from datetime import datetime
from config import Config
from utils.logger import logger

class ChapterScraper:
    def __init__(self):
        os.makedirs(Config.SCREENSHOT_DIR, exist_ok=True)
        
    def scrape_chapter(self, url, chapter_name):
        """Scrape chapter content and take screenshot"""
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=Config.HEADLESS)
                page = browser.new_page()
                
                logger.info(f"Scraping chapter from {url}")
                page.goto(url, timeout=10000)
                
                # Extract content
                content = self._extract_content(page)
                
                # Take screenshot
                screenshot_path = self._take_screenshot(page, chapter_name)
                
                browser.close()
                
                return {
                    "content": content,
                    "screenshot": screenshot_path,
                    "timestamp": datetime.now().isoformat(),
                    "source_url": url
                }
                
        except Exception as e:
            logger.error(f"Scraping failed: {str(e)}")
            raise

    def _extract_content(self, page):
        """Extract main content using smart selectors"""
        # Try multiple selectors for robustness
        selectors = [
            "#content",
            ".chapter",
            "div.mw-parser-output",
            "article"
        ]
        
        for selector in selectors:
            if page.locator(selector).count() > 0:
                return page.locator(selector).inner_text()
        
        return page.inner_text("body")

    def _take_screenshot(self, page, chapter_name):
        """Take full page screenshot with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{chapter_name}_{timestamp}.png"
        path = os.path.join(Config.SCREENSHOT_DIR, filename)
        page.screenshot(path=path, full_page=True)
        return path