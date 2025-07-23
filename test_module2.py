#!/usr/bin/env python3
"""
Test Module 2: Research Plan Generator
"""

import json
from modules.research_planner import ResearchPlanGenerator, generate_research_plan

def test_research_planner():
    """Test the research plan generation system"""
    
    print("🧪 Testing Module 2: Research Plan Generator")
    print("=" * 60)
    
    # Sample requirements (like what Module 1 would produce)
    sample_requirements = {
        "research_topic": "Cross self-attention fusion in transformers",
        "target_audience": "Machine learning researchers",
        "scope": "Focus on NLP and computer vision applications",
        "depth_level": "Expert",
        "specific_questions": ["NLP applications", "Computer vision integration", "Transformer architecture"],
        "output_format": "Research report",
        "clarification_1": "NLP",
        "clarification_3": "transformers", 
        "clarification_6": "computer vision"
    }
    
    print("📋 Input Requirements:")
    for key, value in sample_requirements.items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*60)
    
    # Test the complete workflow
    try:
        research_plan = generate_research_plan(sample_requirements)
        
        print("\n✅ Module 2 Test Results:")
        print("─" * 30)
        print(f"Title: {research_plan.get('title', 'N/A')}")
        print(f"Sections: {len(research_plan.get('main_sections', []))}")
        print(f"Research Questions: {len(research_plan.get('research_questions', []))}")
        print(f"Methodology Defined: {'✅' if research_plan.get('methodology') else '❌'}")
        
        print("\n🎉 Module 2 working successfully!")
        return research_plan
        
    except Exception as e:
        print(f"❌ Module 2 Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_research_planner()
