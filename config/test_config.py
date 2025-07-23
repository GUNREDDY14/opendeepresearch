#!/usr/bin/env python3
"""
Test script to verify ODR configuration is working properly
"""

from config.api_keys import config

def test_configuration():
    """Test all configuration components"""
    
    print("🧪 Testing ODR Configuration")
    print("=" * 50)
    
    # Print configuration status
    config.print_config_status()
    
    # Test Ollama connection
    print("\n🔌 Testing Ollama Connection...")
    if config.is_ollama_available():
        print("✅ Ollama server is running and accessible")
        
        # Test model availability
        try:
            import ollama
            models = ollama.list()
            available_models = [model['name'] for model in models['models']]
            
            print(f"📦 Available Models: {len(available_models)}")
            for model in available_models:
                print(f"   • {model}")
                
            # Test if our configured models are available
            required_models = [
                config.OLLAMA_PRIMARY_MODEL,
                config.OLLAMA_CODE_MODEL, 
                config.OLLAMA_FAST_MODEL
            ]
            
            missing_models = []
            for model in required_models:
                if not any(model in available for available in available_models):
                    missing_models.append(model)
            
            if missing_models:
                print(f"⚠️  Missing Models: {missing_models}")
                print("   Run: ollama pull <model_name> to install")
            else:
                print("✅ All required models are available")
                
        except Exception as e:
            print(f"❌ Error checking models: {e}")
    else:
        print("❌ Ollama server not accessible")
        print("   Make sure 'ollama serve' is running")
    
    # Test task-based model selection
    print("\n🎯 Testing Task-Based Model Selection...")
    test_tasks = ["research", "writing", "code", "technical", "fast"]
    for task in test_tasks:
        model = config.get_model_for_task(task)
        print(f"   {task:10} → {model}")
    
    # Test cloud provider availability
    print("\n☁️  Cloud Provider Status...")
    available_providers = config.get_available_providers()
    print(f"   Available: {', '.join(available_providers)}")
    
    if "openai" not in available_providers:
        print("   💡 Add OPENAI_API_KEY to .env for OpenAI support")
    if "anthropic" not in available_providers:
        print("   💡 Add ANTHROPIC_API_KEY to .env for Claude support")
    if "google" not in available_providers:
        print("   💡 Add GOOGLE_API_KEY to .env for Gemini support")
    
    print("\n🎉 Configuration test complete!")

if __name__ == "__main__":
    test_configuration()
