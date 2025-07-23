#!/usr/bin/env python3
"""
Test Module 4: Report Generator
"""

import json
import os
from modules.report_generator import ReportGenerator, generate_report

def test_report_generator():
    """Test the report generation system"""
    
    print("🧪 Testing Module 4: Report Generator")
    print("=" * 60)
    
    # Load the most recent research data
    data_files = [f for f in os.listdir("data") if f.startswith("research_data_fixed_") and f.endswith(".json")]
    
    if not data_files:
        print("❌ No research data files found. Run Module 3 first.")
        return None
    
    # Get the most recent file
    latest_file = sorted(data_files)[-1]
    data_path = f"data/{latest_file}"
    
    print(f"📂 Loading research data: {latest_file}")
    
    with open(data_path, 'r') as f:
        research_data = json.load(f)
    
    # Load research plan (if available)
    plan_files = [f for f in os.listdir("data") if f.startswith("research_plan_") and f.endswith(".json")]
    
    if plan_files:
        latest_plan = sorted(plan_files)[-1]
        with open(f"data/{latest_plan}", 'r') as f:
            research_plan = json.load(f)
        print(f"📂 Loading research plan: {latest_plan}")
    else:
        # Create sample plan
        research_plan = {
            "title": "Cross Self-Attention Fusion in Transformers: A Comprehensive Analysis",
            "research_questions": [
                "What are the fundamental principles of cross self-attention fusion?",
                "How is it currently being applied in practice?",
                "What are the main challenges and limitations?",
                "What future developments can be expected?"
            ],
            "main_sections": [
                {
                    "title": "Background and Fundamentals",
                    "objective": "Establish foundational understanding"
                },
                {
                    "title": "Technical Analysis and Applications",
                    "objective": "Deep dive into technical mechanisms"
                }
            ],
            "metadata": {
                "target_audience": "Machine learning researchers",
                "depth_level": "Expert"
            }
        }
        print("📝 Using sample research plan")
    
    print("\n" + "="*60)
    
    # Test report generation
    try:
        notebook = generate_report(research_plan, research_data)
        
        print("\n✅ Module 4 Test Results:")
        print("─" * 40)
        print(f"Report Title: {research_plan.get('title', 'Unknown')}")
        print(f"Total Cells: {len(notebook.get('cells', []))}")
        print(f"Total Citations: {notebook.get('metadata', {}).get('odr_metadata', {}).get('total_citations', 0)}")
        print(f"Generation Date: {notebook.get('metadata', {}).get('odr_metadata', {}).get('generation_date', 'Unknown')}")
        
        # Show sample content
        print("\n📄 Sample Report Content:")
        for cell in notebook.get('cells', [])[:3]:  # Show first 3 cells
            content = cell.get('source', [''])[0]
            if content.startswith('#'):
                title_line = content.split('\n')[0]
                print(f"  {title_line}")
        
        print("\n🎉 Module 4 working successfully!")
        print("📓 Check the 'outputs' folder for your generated report!")
        
        return notebook
        
    except Exception as e:
        print(f"❌ Module 4 Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_report_generator()
