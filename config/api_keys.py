"""
Configuration management for ODR system
Handles API keys, model settings, and system configuration
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ODRConfig:
    """Centralized configuration management"""
    
    def __init__(self):
        # Ollama Configuration (Primary - Free)
        self.OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.OLLAMA_PRIMARY_MODEL = os.getenv("OLLAMA_PRIMARY_MODEL", "llama3.2")
        self.OLLAMA_CODE_MODEL = os.getenv("OLLAMA_CODE_MODEL", "codellama")
        self.OLLAMA_FAST_MODEL = os.getenv("OLLAMA_FAST_MODEL", "mistral")
        
        # Cloud Provider API Keys (Optional)
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        self.ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
        
        # Research Settings
        self.MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "10"))
        self.DEFAULT_RESEARCH_DEPTH = os.getenv("DEFAULT_RESEARCH_DEPTH", "intermediate")
        self.DEFAULT_CITATION_STYLE = os.getenv("DEFAULT_CITATION_STYLE", "APA")
        
        # System Settings
        self.DEBUG_MODE = os.getenv("DEBUG_MODE", "true").lower() == "true"
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    def get_available_providers(self):
        """Return list of available LLM providers"""
        providers = ["ollama"]  # Always available locally
        
        if self.OPENAI_API_KEY:
            providers.append("openai")
        if self.ANTHROPIC_API_KEY:
            providers.append("anthropic")
        if self.GOOGLE_API_KEY:
            providers.append("google")
            
        return providers
    
    def get_model_for_task(self, task_type):
        """Get optimal model for specific task types"""
        task_mapping = {
            "research": self.OLLAMA_PRIMARY_MODEL,
            "writing": self.OLLAMA_PRIMARY_MODEL,
            "analysis": self.OLLAMA_PRIMARY_MODEL,
            "code": self.OLLAMA_CODE_MODEL,
            "technical": self.OLLAMA_CODE_MODEL,
            "fast": self.OLLAMA_FAST_MODEL,
            "quick": self.OLLAMA_FAST_MODEL
        }
        
        return task_mapping.get(task_type, self.OLLAMA_PRIMARY_MODEL)
    
    def is_ollama_available(self):
        """Check if Ollama is running and accessible"""
        try:
            import requests
            response = requests.get(f"{self.OLLAMA_URL}/api/version", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def print_config_status(self):
        """Print current configuration status"""
        print("🔧 ODR Configuration Status")
        print("=" * 40)
        print(f"Ollama URL: {self.OLLAMA_URL}")
        print(f"Ollama Available: {'✅' if self.is_ollama_available() else '❌'}")
        print(f"Primary Model: {self.OLLAMA_PRIMARY_MODEL}")
        print(f"Code Model: {self.OLLAMA_CODE_MODEL}")
        print(f"Fast Model: {self.OLLAMA_FAST_MODEL}")
        print(f"Available Providers: {', '.join(self.get_available_providers())}")
        print(f"Debug Mode: {'✅' if self.DEBUG_MODE else '❌'}")
        print("=" * 40)

# Global configuration instance
config = ODRConfig()
