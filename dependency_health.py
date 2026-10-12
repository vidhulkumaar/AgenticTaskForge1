import sys
import subprocess
import urllib.request
from config import Config
from utils import get_logger

logger = get_logger("HealthChecker")

class DependencyHealthChecker:
    @staticmethod
    def check_all():
        healthy = True
        
        # 1. Playwright
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                if not p.chromium.executable_path:
                    logger.error("Playwright Chromium browser not found. Run: playwright install chromium")
                    healthy = False
        except Exception as e:
            logger.error(f"Playwright check failed: {e}")
            healthy = False
            
        # 2. Ollama & Embedding model
        try:
            req = urllib.request.Request(f"{Config.OLLAMA_BASE_URL}/api/tags")
            with urllib.request.urlopen(req, timeout=2) as response:
                if response.status == 200:
                    data = response.read().decode('utf-8')
                    if Config.EMBEDDING_MODEL not in data:
                        logger.error(f"Ollama running, but model '{Config.EMBEDDING_MODEL}' not found. Run: ollama pull {Config.EMBEDDING_MODEL}")
                        healthy = False
                else:
                    logger.error("Ollama API returned non-200 status.")
                    healthy = False
        except Exception as e:
            logger.error(f"Ollama check failed: {e}")
            healthy = False
            
        # 3. OCR (Tesseract)
        try:
            import pytesseract
            import PIL.Image
            img = PIL.Image.new('RGB', (10, 10), color = (255, 255, 255))
            pytesseract.image_to_string(img)
        except Exception as e:
            logger.error(f"OCR check failed: {e}. Ensure Tesseract is installed locally and in PATH.")
            healthy = False
            
        if not healthy:
            logger.critical("Dependency health check failed. System cannot start safely.")
            sys.exit(1)
        else:
            logger.info("All dependencies healthy.")
