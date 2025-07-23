#!/usr/bin/env python3
"""
Test Module 1: User Input and Clarification
"""

from modules.user_input import UserInputModule, collect_user_requirements

def test_user_input_module():
    """Test the user input collection system"""
    
    print("🧪 Testing Module 1: User Input & Clarification")
    print("=" * 60)
    
    # Test the complete workflow
    try:
        requirements = collect_user_requirements()
        
        print("\n✅ Module 1 Test Results:")
        print("─" * 30)
        
        for key, value in requirements.items():
            print(f"{key}: {value}")
        
        print("\n🎉 Module 1 working successfully!")
        return requirements
        
    except Exception as e:
        print(f"❌ Module 1 Error: {e}")
        return None

if __name__ == "__main__":
    test_user_input_module()
