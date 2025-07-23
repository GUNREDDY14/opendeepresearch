#!/usr/bin/env python3
"""
Open Deep Researcher (ODR) - Complete System
"""

import json
import os
from datetime import datetime
from modules.user_input import UserInputModule
from modules.research_planner import ResearchPlanGenerator
from modules.research_executor import ResearchExecutor
from modules.report_generator import ReportGenerator
from modules.llm_client import create_llm_client

class OpenDeepResearcher:
    """Complete ODR system orchestrator"""
    
    def __init__(self, llm_provider="ollama", model="llama3.2"):
        print("🚀 Initializing Open Deep Researcher System")
        print("=" * 60)
        
        # Initialize LLM client
        self.llm_client = create_llm_client(llm_provider)
        
        # Initialize all modules
        self.user_input = UserInputModule(self.llm_client)
        self.planner = ResearchPlanGenerator(self.llm_client)
        self.executor = ResearchExecutor(self.llm_client)
        self.generator = ReportGenerator(self.llm_client)
        
        # Create directories
        os.makedirs("data", exist_ok=True)
        os.makedirs("outputs", exist_ok=True)
        
        print("✅ ODR System Ready!")
        print()
    
    def run_complete_research(self):
        """Execute complete workflow: Module 1 → 2 → 3 → 4"""
        
        print("🔬 COMPLETE RESEARCH WORKFLOW")
        print("=" * 60)
        
        try:
            # Module 1: User Input
            print("📋 PHASE 1: User Input & Clarification")
            requirements = self.user_input.collect_research_requirements()
            print("✅ Requirements collected\n")
            
            # Module 2: Research Planning
            print("📝 PHASE 2: Research Plan Generation")
            research_plan = self.planner.generate_research_plan(requirements)
            print("✅ Research plan generated\n")
            
            # Module 3: Research Execution
            print("🔍 PHASE 3: Research Execution")
            research_data = self.executor.execute_research_plan(research_plan)
            print("✅ Research data collected\n")
            
            # Module 4: Report Generation
            print("📄 PHASE 4: Report Generation")
            final_report = self.generator.generate_report(research_plan, research_data)
            print("✅ Final report generated\n")
            
            print("🎉 WORKFLOW COMPLETED SUCCESSFULLY!")
            print("📁 Check 'outputs' folder for your research report!")
            
            return final_report
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def quick_research(self, topic: str):
        """Quick research with minimal interaction"""
        
        print(f"⚡ QUICK RESEARCH: {topic}")
        print("=" * 50)
        
        # Auto-generate requirements
        requirements = {
            "research_topic": topic,
            "target_audience": "general",
            "scope": "comprehensive overview", 
            "depth_level": "intermediate",
            "output_format": "research report"
        }
        
        try:
            research_plan = self.planner.generate_research_plan(requirements)
            research_data = self.executor.execute_research_plan(research_plan)
            final_report = self.generator.generate_report(research_plan, research_data)
            
            print("⚡ Quick research completed!")
            return final_report
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

def main():
    """Main menu interface"""
    
    print("🔬 Open Deep Researcher (ODR)")
    print("=" * 40)
    print("1. Complete Interactive Research")
    print("2. Quick Research")
    print("3. Exit")
    print()
    
    choice = input("Choose option (1-3): ")
    
    if choice == "1":
        odr = OpenDeepResearcher()
        odr.run_complete_research()
    elif choice == "2":
        topic = input("Enter research topic: ")
        odr = OpenDeepResearcher()
        odr.quick_research(topic)
    elif choice == "3":
        print("Goodbye!")
    else:
        print("Invalid choice")

# Standalone functions for external use
def run_interactive_research():
    """Run complete interactive research"""
    odr = OpenDeepResearcher()
    return odr.run_complete_research()

def run_quick_research(topic: str):
    """Run quick research"""
    odr = OpenDeepResearcher()
    return odr.quick_research(topic)

if __name__ == "__main__":
    main()
