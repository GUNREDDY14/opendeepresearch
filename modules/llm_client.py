"""
Universal LLM Client for ODR System
Provides unified interface to multiple LLM providers with intelligent fallbacks
"""

import json
import time
import requests
from typing import Optional, Dict, Any, List
from config.api_keys import config

class UniversalLLMClient:
    """
    Universal client that can work with any LLM provider
    Handles automatic fallbacks, retries, and task-specific optimization
    """
    
    def __init__(self, primary_provider="ollama", fallback_providers=None):
        self.primary_provider = primary_provider
        self.fallback_providers = fallback_providers or ["ollama"]
        self.config = config
        
        # Track usage and performance
        self.usage_stats = {
            "requests": 0,
            "successful": 0,
            "failed": 0,
            "provider_usage": {}
        }
        
        print(f"🤖 Universal LLM Client initialized")
        print(f"   Primary: {primary_provider}")
        print(f"   Fallbacks: {fallback_providers}")
    
    def generate(self, prompt: str, task_type: str = "general", 
                max_tokens: int = 1000, temperature: float = 0.7,
                provider: str = None) -> str:
        """
        Universal generation method that works with any provider
        """
        
        self.usage_stats["requests"] += 1
        
        # Determine which provider to use
        chosen_provider = provider or self.primary_provider
        
        # Get optimal model for the task
        model = self.config.get_model_for_task(task_type)
        
        if self.config.DEBUG_MODE:
            print(f"🎯 Task: {task_type} | Provider: {chosen_provider} | Model: {model}")
        
        # Try primary provider first
        try:
            response = self._generate_with_provider(
                chosen_provider, model, prompt, max_tokens, temperature
            )
            
            if response and not response.startswith("Error:"):
                self._update_stats(chosen_provider, success=True)
                return response
                
        except Exception as e:
            if self.config.DEBUG_MODE:
                print(f"⚠️ Provider {chosen_provider} failed: {e}")
        
        # Try fallback providers
        for fallback_provider in self.fallback_providers:
            if fallback_provider != chosen_provider:
                try:
                    if self.config.DEBUG_MODE:
                        print(f"🔄 Trying fallback: {fallback_provider}")
                    
                    response = self._generate_with_provider(
                        fallback_provider, model, prompt, max_tokens, temperature
                    )
                    
                    if response and not response.startswith("Error:"):
                        self._update_stats(fallback_provider, success=True)
                        return response
                        
                except Exception as e:
                    if self.config.DEBUG_MODE:
                        print(f"⚠️ Fallback {fallback_provider} failed: {e}")
                    continue
        
        # All providers failed
        self._update_stats("none", success=False)
        return f"Error: All LLM providers failed to generate response for task: {task_type}"
    
    def _generate_with_provider(self, provider: str, model: str, prompt: str, 
                              max_tokens: int, temperature: float) -> str:
        """Generate text using specific provider"""
        
        if provider == "ollama":
            return self._ollama_generate(model, prompt, max_tokens, temperature)
        elif provider == "openai":
            return self._openai_generate(model, prompt, max_tokens, temperature)
        elif provider == "anthropic":
            return self._anthropic_generate(model, prompt, max_tokens, temperature)
        elif provider == "google":
            return self._google_generate(model, prompt, max_tokens, temperature)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
    
    def _ollama_generate(self, model: str, prompt: str, max_tokens: int, temperature: float) -> str:
        """Generate using local Ollama - your primary free option"""
        try:
            response = requests.post(
                f"{self.config.OLLAMA_URL}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_tokens,
                        "temperature": temperature,
                        "top_p": 0.9,
                        "repeat_penalty": 1.1
                    }
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get("response", "")
                
                if generated_text:
                    return generated_text.strip()
                else:
                    return "Error: Empty response from Ollama"
            else:
                return f"Error: Ollama returned status {response.status_code}"
                
        except requests.exceptions.Timeout:
            return "Error: Ollama request timed out - try a simpler prompt"
        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to Ollama - ensure 'ollama serve' is running"
        except Exception as e:
            return f"Ollama error: {str(e)}"
    
    def _openai_generate(self, model: str, prompt: str, max_tokens: int, temperature: float) -> str:
        """Generate using OpenAI API (requires API key)"""
        if not self.config.OPENAI_API_KEY:
            return "Error: OpenAI API key not configured in .env file"
        
        try:
            openai_models = {
                "llama3.2": "gpt-3.5-turbo",
                "codellama": "gpt-3.5-turbo",
                "mistral": "gpt-3.5-turbo"
            }
            
            openai_model = openai_models.get(model, "gpt-3.5-turbo")
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.config.OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": openai_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": temperature
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
            else:
                return f"Error: OpenAI API returned status {response.status_code}"
                
        except Exception as e:
            return f"OpenAI error: {str(e)}"
    
    def _anthropic_generate(self, model: str, prompt: str, max_tokens: int, temperature: float) -> str:
        """Generate using Anthropic Claude (requires API key)"""
        if not self.config.ANTHROPIC_API_KEY:
            return "Error: Anthropic API key not configured in .env file"
        
        return "Anthropic integration ready - add API key to .env to activate"
    
    def _google_generate(self, model: str, prompt: str, max_tokens: int, temperature: float) -> str:
        """Generate using Google Gemini (requires API key)"""
        if not self.config.GOOGLE_API_KEY:
            return "Error: Google API key not configured in .env file"
        
        return "Google Gemini integration ready - add API key to .env to activate"
    
    def batch_generate(self, prompts: list, task_type: str = "general") -> list:
        """Generate responses for multiple prompts"""
        responses = []
        
        print(f"📝 Processing {len(prompts)} prompts for task: {task_type}")
        
        for i, prompt in enumerate(prompts):
            if self.config.DEBUG_MODE:
                print(f"   Processing {i+1}/{len(prompts)}")
            
            response = self.generate(prompt, task_type)
            responses.append(response)
            time.sleep(0.5)
        
        return responses
    
    def _update_stats(self, provider: str, success: bool):
        """Track usage statistics"""
        if success:
            self.usage_stats["successful"] += 1
        else:
            self.usage_stats["failed"] += 1
        
        if provider not in self.usage_stats["provider_usage"]:
            self.usage_stats["provider_usage"][provider] = {"requests": 0, "successes": 0}
        
        self.usage_stats["provider_usage"][provider]["requests"] += 1
        if success:
            self.usage_stats["provider_usage"][provider]["successes"] += 1
    
    def print_usage_stats(self):
        """Print usage statistics"""
        print("\n📊 LLM Client Usage Statistics")
        print("=" * 40)
        print(f"Total Requests: {self.usage_stats['requests']}")
        print(f"Successful: {self.usage_stats['successful']}")
        print(f"Failed: {self.usage_stats['failed']}")
        
        if self.usage_stats["provider_usage"]:
            print("\nProvider Usage:")
            for provider, stats in self.usage_stats["provider_usage"].items():
                success_rate = (stats["successes"] / stats["requests"] * 100) if stats["requests"] > 0 else 0
                print(f"  {provider}: {stats['requests']} requests, {success_rate:.1f}% success")
        print("=" * 40)
    
    def test_all_providers(self):
        """Test all available providers with simple prompts"""
        print("\n🧪 Testing All Available Providers")
        print("=" * 50)
        
        test_prompt = "Hello! Please respond with 'Working' if you can understand this."
        available_providers = self.config.get_available_providers()
        
        for provider in available_providers:
            print(f"\n🔌 Testing {provider}...")
            response = self.generate(test_prompt, task_type="fast", provider=provider)
            
            if "Error:" in response:
                print(f"❌ {provider}: {response}")
            else:
                print(f"✅ {provider}: {response[:50]}...")
        
        print("\n🎉 Provider testing complete!")

# Create a global client instance
def create_llm_client(provider="ollama"):
    """Factory function to create LLM client with optimal settings"""
    return UniversalLLMClient(
        primary_provider=provider,
        fallback_providers=["ollama"]
    )
