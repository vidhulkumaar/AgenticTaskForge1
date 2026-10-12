from dataclasses import dataclass
from typing import Optional, Any

@dataclass
class AgentContext:
    execution_id: Optional[str] = None
    app: Optional[Any] = None
    main_window: Optional[Any] = None
    document: Optional[Any] = None
    
    explorer_window: Optional[Any] = None
    current_folder_path: Optional[str] = None
    
    playwright: Optional[Any] = None
    browser: Optional[Any] = None
    browser_context: Optional[Any] = None
    page: Optional[Any] = None
    
    def cleanup(self):
        """Releases UI references to prevent stale handles."""
        self.app = None
        self.main_window = None
        self.document = None
        
        self.explorer_window = None
        self.current_folder_path = None
        
        if self.page:
            try:
                self.page.close()
            except Exception:
                pass
        if self.browser:
            try:
                self.browser.close()
            except Exception:
                pass
        if self.playwright:
            try:
                self.playwright.stop()
            except Exception:
                pass
                
        self.page = None
        self.browser_context = None
        self.browser = None
        self.playwright = None
