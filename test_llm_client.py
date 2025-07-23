#!/usr/bin/env python3
"""
Test the Universal LLM Client
"""

from modules.llm_client import create_llm_client

def test_llm_client():
    """Test all LLM client functionality"""
    
    print("🚀 Testing Universal LLM Client")
    print("=" * 50)
    
    # Create client
    client = create_llm_client("ollama")
    
    # Test different task types
    test_cases = [
        ("research", "What are the key benefits of renewable energy?"),
        ("writing", "Write a brief introduction about artificial intelligence."),
        ("code", "Write a simple Python function to calculate fibonacci numbers."),
        ("fast", "What is 2+2?")
    ]
    
    print("\n📝 Testing Different Task Types:")
    
    for task_type, prompt in test_cases:
        print(f"\n🎯 Task: {task_type}")
        print(f"Prompt: {prompt}")
        print("Response:")
        
        response = client.generate(prompt, task_type=task_type, max_tokens=200)
        
        if "Error:" in response:
            print(f"❌ {response}")
        else:
            # Show first 200 characters
            print(f"✅ {response[:200]}...")
    
    # Test provider availability
    client.test_all_providers()
    
    # Show usage stats
    client.print_usage_stats()
    
    print("\n🎉 LLM Client testing complete!")

if __name__ == "__main__":
    test_llm_client()
