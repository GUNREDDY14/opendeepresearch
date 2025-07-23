#!/usr/bin/env python3
"""
Test Module 3: Research Execution with Supervisor Node
"""

import json
from modules.research_executor import ResearchExecutor, execute_research

def test_research_executor():
    """Test the research execution system"""
    
    print("🧪 Testing Module 3: Research Execution with Supervisor Node")
    print("=" * 70)
    
    # Sample research plan (like what Module 2 would produce)
    sample_plan = {
        "title": "Cross Self-Attention Fusion in Transformers: A Comprehensive Analysis",
        "main_sections": [
            {
                "title": "Background and Fundamentals",
                "objective": "Establish foundational understanding of cross self-attention fusion",
                "subsections": [
                    {"title": "Core Concepts", "data_sources_needed": ["academic", "technical"]},
                    {"title": "Historical Development", "data_sources_needed": ["academic", "web"]}
                ],
                "data_requirements": ["Academic papers", "Technical documentation"]
            },
            {
                "title": "Technical Analysis and Applications", 
                "objective": "Deep dive into technical mechanisms and real-world usage",
                "subsections": [
                    {"title": "Architecture Details", "data_sources_needed": ["technical", "academic"]},
                    {"title": "NLP Applications", "data_sources_needed": ["industry", "academic"]}
                ],
                "data_requirements": ["Technical papers", "Implementation guides", "Case studies"]
            }
        ]
    }
    
    print("📋 Sample Research Plan:")
    print(f"  Title: {sample_plan['title']}")
    print(f"  Sections: {len(sample_plan['main_sections'])}")
    
    print("\n" + "="*70)
    
    # Test the complete research execution
    try:
        research_data = execute_research(sample_plan)
        
        print("\n✅ Module 3 Test Results:")
        print("─" * 40)
        print(f"Sections Researched: {len(research_data['sections_data'])}")
        print(f"Total Sources Found: {research_data['summary']['total_sources']}")
        print(f"Internal Sources: {research_data['summary']['internal_sources']}")
        print(f"External Sources: {research_data['summary']['external_sources']}")
        
        print("\n📊 Section Breakdown:")
        for section_name, section_data in research_data['sections_data'].items():
            sources_count = len(section_data.get('all_sources', []))
            processed_count = len(section_data.get('processed_content', []))
            print(f"  {section_name}: {sources_count} sources, {processed_count} processed")
        
        # Show sample processed content
        print("\n📝 Sample Processed Content:")
        for section_name, section_data in research_data['sections_data'].items():
            processed = section_data.get('processed_content', [])
            if processed:
                sample = processed[0]
                print(f"  {section_name}:")
                print(f"    Source: {sample.get('source_title', 'Unknown')}")
                print(f"    Insights: {sample.get('key_insights', 'None')[:100]}...")
                break
        
        print("\n🎉 Module 3 working successfully!")
        return research_data
        
    except Exception as e:
        print(f"❌ Module 3 Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_research_executor()
