"""
Module 2: Research Plan Generator
Creates structured research plans from user requirements
"""

import json
from datetime import datetime
from typing import Dict, List, Any
from modules.llm_client import create_llm_client

class ResearchPlanGenerator:
    """
    Generates comprehensive research plans based on user requirements
    """
    
    def __init__(self, llm_client=None):
        self.llm_client = llm_client or create_llm_client()
        self.plan_template = {
            "metadata": {},
            "introduction": {},
            "main_sections": [],
            "conclusion": {},
            "methodology": {},
            "citations": {},
            "timeline": {}
        }
    
    def generate_research_plan(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main entry point: Generate complete research plan from requirements
        
        Args:
            requirements: Structured requirements from Module 1
            
        Returns:
            Complete research plan ready for Module 3
        """
        
        print("📋 Research Plan Generator")
        print("=" * 50)
        print("Creating structured research plan based on your requirements...\n")
        
        # Step 1: Generate plan outline
        plan_outline = self._generate_plan_outline(requirements)
        
        # Step 2: Develop detailed sections
        detailed_sections = self._develop_section_details(plan_outline, requirements)
        
        # Step 3: Create methodology
        methodology = self._create_research_methodology(requirements)
        
        # Step 4: Structure introduction and conclusion
        intro_conclusion = self._structure_intro_conclusion(requirements, detailed_sections)
        
        # Step 5: Compile complete plan
        complete_plan = self._compile_complete_plan(
            requirements, plan_outline, detailed_sections, 
            methodology, intro_conclusion
        )
        
        # Step 6: Validate and refine
        final_plan = self._validate_and_refine_plan(complete_plan)
        
        # Step 7: Export plan
        self._export_plan(final_plan)
        
        print("\n✅ Research plan generated successfully!")
        return final_plan
    
    def _generate_plan_outline(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate high-level research plan structure"""
        
        print("🎯 Step 1: Generating Plan Outline...")
        
        outline_prompt = f"""
        Research Topic: {requirements.get('research_topic', '')}
        Target Audience: {requirements.get('target_audience', '')}
        Research Scope: {requirements.get('scope', '')}
        Depth Level: {requirements.get('depth_level', '')}
        Specific Focus: {requirements.get('specific_questions', [])}
        
        Create a comprehensive research plan outline for this topic. The plan should be structured for {requirements.get('depth_level', 'intermediate')} level and targeted at {requirements.get('target_audience', 'general audience')}.
        
        Generate a JSON structure with:
        1. "title": Clear, academic title for the research
        2. "abstract": Brief summary of what the research will cover
        3. "main_sections": Array of 4-6 main sections, each with:
           - "title": Section name
           - "objective": What this section aims to achieve
           - "key_topics": Array of 3-4 key topics to cover
           - "estimated_length": Approximate word count or pages
        4. "research_questions": 3-5 specific questions this research will answer
        5. "scope_boundaries": What is included and excluded
        
        Ensure the structure is logical, comprehensive, and appropriate for the specified depth level.
        """
        
        outline_response = self.llm_client.generate(
            outline_prompt,
            task_type="research",
            max_tokens=800,
            temperature=0.3
        )
        
        try:
            outline = json.loads(outline_response)
            print("✅ Plan outline generated")
            return outline
        except json.JSONDecodeError:
            print("⚠️ Using fallback outline structure")
            return self._create_fallback_outline(requirements)
    
    def _create_fallback_outline(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback outline if JSON parsing fails"""
        
        topic = requirements.get('research_topic', 'Research Topic')
        
        return {
            "title": f"Comprehensive Analysis of {topic}",
            "abstract": f"This research provides a detailed examination of {topic}, exploring key concepts, current developments, and practical applications.",
            "main_sections": [
                {
                    "title": "Background and Fundamentals",
                    "objective": "Establish foundational understanding",
                    "key_topics": ["Core concepts", "Historical context", "Terminology"],
                    "estimated_length": "800-1000 words"
                },
                {
                    "title": "Current State and Developments", 
                    "objective": "Analyze current landscape and recent advances",
                    "key_topics": ["Recent research", "Current implementations", "Emerging trends"],
                    "estimated_length": "1000-1200 words"
                },
                {
                    "title": "Technical Analysis and Applications",
                    "objective": "Deep dive into technical aspects and real-world usage",
                    "key_topics": ["Technical mechanisms", "Use cases", "Performance analysis"],
                    "estimated_length": "1200-1500 words"
                },
                {
                    "title": "Challenges and Future Directions",
                    "objective": "Identify limitations and future research opportunities",
                    "key_topics": ["Current limitations", "Open problems", "Future prospects"],
                    "estimated_length": "800-1000 words"
                }
            ],
            "research_questions": [
                f"What are the fundamental principles of {topic}?",
                f"How is {topic} currently being applied?",
                f"What are the main challenges and limitations?",
                f"What future developments can be expected?"
            ],
            "scope_boundaries": {
                "included": ["Core concepts", "Current applications", "Technical analysis"],
                "excluded": ["Implementation details", "Code examples", "Vendor comparisons"]
            }
        }
    
    def _develop_section_details(self, outline: Dict[str, Any], requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Develop detailed specifications for each section"""
        
        print("📝 Step 2: Developing Section Details...")
        
        detailed_sections = []
        
        for i, section in enumerate(outline.get('main_sections', [])):
            print(f"   Detailing section {i+1}: {section['title']}")
            
            detail_prompt = f"""
            Research Topic: {requirements.get('research_topic', '')}
            Section Title: {section['title']}
            Section Objective: {section['objective']}
            Key Topics: {section.get('key_topics', [])}
            Target Audience: {requirements.get('target_audience', '')}
            Depth Level: {requirements.get('depth_level', '')}
            
            Create detailed specifications for this research section. Generate JSON with:
            
            1. "title": Section title
            2. "introduction": Brief intro to the section (2-3 sentences)
            3. "subsections": Array of 3-4 subsections, each with:
               - "title": Subsection name
               - "content_outline": What specific content to include
               - "data_sources_needed": Types of sources required (academic, industry, web, internal)
               - "key_points": 2-3 specific points to address
            4. "data_requirements": Overall data needs for this section
            5. "expected_insights": What conclusions this section should reach
            6. "connection_to_next": How this section leads to the next one
            
            Make it specific and actionable for research execution.
            """
            
            detail_response = self.llm_client.generate(
                detail_prompt,
                task_type="analysis",
                max_tokens=600,
                temperature=0.3
            )
            
            try:
                section_details = json.loads(detail_response)
                detailed_sections.append(section_details)
            except json.JSONDecodeError:
                # Fallback section structure
                detailed_sections.append(self._create_fallback_section(section))
        
        print("✅ Section details developed")
        return detailed_sections
    
    def _create_fallback_section(self, section: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback section details"""
        
        return {
            "title": section['title'],
            "introduction": f"This section explores {section['title'].lower()} in detail.",
            "subsections": [
                {
                    "title": "Overview",
                    "content_outline": "General introduction and key concepts",
                    "data_sources_needed": ["academic", "web"],
                    "key_points": ["Definition", "Importance"]
                },
                {
                    "title": "Technical Details", 
                    "content_outline": "In-depth technical analysis",
                    "data_sources_needed": ["academic", "industry"],
                    "key_points": ["Mechanisms", "Implementation"]
                },
                {
                    "title": "Applications",
                    "content_outline": "Real-world applications and examples",
                    "data_sources_needed": ["industry", "web"],
                    "key_points": ["Use cases", "Benefits"]
                }
            ],
            "data_requirements": ["Academic papers", "Industry reports", "Technical documentation"],
            "expected_insights": "Comprehensive understanding of the topic area",
            "connection_to_next": "Provides foundation for subsequent analysis"
        }
    
    def _create_research_methodology(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Define research methodology and approach"""
        
        print("🔬 Step 3: Creating Research Methodology...")
        
        methodology_prompt = f"""
        Research Topic: {requirements.get('research_topic', '')}
        Target Audience: {requirements.get('target_audience', '')}
        Depth Level: {requirements.get('depth_level', '')}
        
        Define a comprehensive research methodology for this project. Create JSON with:
        
        1. "approach": Research approach (systematic review, analytical study, etc.)
        2. "data_sources": 
           - "primary": Primary sources to prioritize
           - "secondary": Secondary sources to use
           - "search_strategy": Keywords and search terms
        3. "quality_criteria": How to evaluate source quality and relevance
        4. "analysis_framework": How to analyze and synthesize information
        5. "validation_methods": How to ensure accuracy and completeness
        6. "limitations": Potential limitations and how to address them
        
        Make it appropriate for the specified depth level and audience.
        """
        
        methodology_response = self.llm_client.generate(
            methodology_prompt,
            task_type="analysis",
            max_tokens=500,
            temperature=0.2
        )
        
        try:
            methodology = json.loads(methodology_response)
            print("✅ Research methodology defined")
            return methodology
        except json.JSONDecodeError:
            print("⚠️ Using fallback methodology")
            return self._create_fallback_methodology()
    
    def _create_fallback_methodology(self) -> Dict[str, Any]:
        """Fallback methodology structure"""
        
        return {
            "approach": "Systematic literature review and analysis",
            "data_sources": {
                "primary": ["Academic journals", "Conference papers", "Technical reports"],
                "secondary": ["Industry publications", "News articles", "Blog posts"],
                "search_strategy": ["Topic keywords", "Related terms", "Author searches"]
            },
            "quality_criteria": ["Source credibility", "Recency", "Relevance", "Citation count"],
            "analysis_framework": "Thematic analysis with systematic categorization",
            "validation_methods": ["Cross-referencing sources", "Expert validation", "Peer review"],
            "limitations": ["Time constraints", "Source availability", "Language barriers"]
        }
    
    def _structure_intro_conclusion(self, requirements: Dict[str, Any], sections: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create introduction and conclusion structure"""
        
        print("📖 Step 4: Structuring Introduction and Conclusion...")
        
        intro_conclusion_prompt = f"""
        Research Topic: {requirements.get('research_topic', '')}
        Main Sections: {[s.get('title', '') for s in sections]}
        Target Audience: {requirements.get('target_audience', '')}
        
        Create introduction and conclusion structures. Generate JSON with:
        
        1. "introduction":
           - "hook": Engaging opening statement
           - "background": Brief context and importance
           - "objectives": Clear research objectives
           - "structure_overview": How the paper is organized
           - "key_contributions": What this research contributes
        
        2. "conclusion":
           - "summary_approach": How to summarize key findings
           - "implications": Types of implications to discuss
           - "future_work": Areas for future research
           - "final_thoughts": How to end meaningfully
        
        Make it engaging and appropriate for the target audience.
        """
        
        intro_conclusion_response = self.llm_client.generate(
            intro_conclusion_prompt,
            task_type="writing",
            max_tokens=600,
            temperature=0.4
        )
        
        try:
            intro_conclusion = json.loads(intro_conclusion_response)
            print("✅ Introduction and conclusion structured")
            return intro_conclusion
        except json.JSONDecodeError:
            print("⚠️ Using fallback introduction/conclusion structure")
            return self._create_fallback_intro_conclusion()
    
    def _create_fallback_intro_conclusion(self) -> Dict[str, Any]:
        """Fallback introduction and conclusion structure"""
        
        return {
            "introduction": {
                "hook": "Engaging opening statement about topic relevance",
                "background": "Context and importance of the research area",
                "objectives": "Clear statement of research goals and questions",
                "structure_overview": "Overview of paper organization and flow",
                "key_contributions": "Summary of unique insights and value provided"
            },
            "conclusion": {
                "summary_approach": "Synthesize key findings from each major section",
                "implications": "Discuss theoretical, practical, and strategic implications",
                "future_work": "Identify promising areas for continued research",
                "final_thoughts": "Conclude with broader significance and impact"
            }
        }
    
    def _compile_complete_plan(self, requirements: Dict[str, Any], outline: Dict[str, Any], 
                             sections: List[Dict[str, Any]], methodology: Dict[str, Any],
                             intro_conclusion: Dict[str, Any]) -> Dict[str, Any]:
        """Compile all components into complete research plan"""
        
        print("🔧 Step 5: Compiling Complete Plan...")
        
        complete_plan = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "research_topic": requirements.get('research_topic', ''),
                "target_audience": requirements.get('target_audience', ''),
                "depth_level": requirements.get('depth_level', ''),
                "estimated_total_length": "4000-6000 words",
                "estimated_completion_time": "2-3 hours research + 2-3 hours writing"
            },
            "title": outline.get('title', ''),
            "abstract": outline.get('abstract', ''),
            "research_questions": outline.get('research_questions', []),
            "scope_boundaries": outline.get('scope_boundaries', {}),
            "introduction_structure": intro_conclusion.get('introduction', {}),
            "main_sections": sections,
            "conclusion_structure": intro_conclusion.get('conclusion', {}),
            "methodology": methodology,
            "citation_requirements": {
                "style": "APA",
                "minimum_sources": 15,
                "source_types": ["Academic papers", "Industry reports", "Technical documentation"],
                "recency_requirement": "Prefer sources from last 3-5 years"
            },
            "quality_checkpoints": [
                "Verify all research questions are addressed",
                "Ensure logical flow between sections", 
                "Check citation completeness and accuracy",
                "Validate technical accuracy and depth",
                "Confirm audience appropriateness"
            ]
        }
        
        print("✅ Complete plan compiled")
        return complete_plan
    
    def _validate_and_refine_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Allow user to review and refine the research plan"""
        
        print("\n" + "=" * 60)
        print("📋 GENERATED RESEARCH PLAN PREVIEW")
        print("=" * 60)
        
        # Display plan summary
        print(f"Title: {plan.get('title', 'N/A')}")
        print(f"Target Audience: {plan['metadata'].get('target_audience', 'N/A')}")
        print(f"Estimated Length: {plan['metadata'].get('estimated_total_length', 'N/A')}")
        print(f"Estimated Time: {plan['metadata'].get('estimated_completion_time', 'N/A')}")
        
        print(f"\nResearch Questions:")
        for i, question in enumerate(plan.get('research_questions', []), 1):
            print(f"  {i}. {question}")
        
        print(f"\nMain Sections:")
        for i, section in enumerate(plan.get('main_sections', []), 1):
            print(f"  {i}. {section.get('title', 'N/A')}")
            subsections = section.get('subsections', [])
            for j, subsection in enumerate(subsections[:2], 1):  # Show first 2 subsections
                print(f"     {i}.{j} {subsection.get('title', 'N/A')}")
            if len(subsections) > 2:
                print(f"     ... and {len(subsections)-2} more subsections")
        
        print("=" * 60)
        
        # Allow modifications
        modify = input("\nWould you like to modify this research plan? (y/n): ").lower()
        
        if modify == 'y':
            return self._modify_plan(plan)
        else:
            return plan
    
    def _modify_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Allow user to modify specific aspects of the plan"""
        
        print("\nWhat would you like to modify?")
        print("1. Research title")
        print("2. Add/modify research questions")
        print("3. Adjust section focus")
        print("4. Change depth/complexity level")
        print("5. Other modifications")
        
        choice = input("Enter choice (1-5) or 'done': ").strip()
        
        if choice == '1':
            new_title = input("Enter new research title: ").strip()
            if new_title:
                plan['title'] = new_title
                print("✅ Title updated")
        
        elif choice == '2':
            print("Current research questions:")
            for i, q in enumerate(plan.get('research_questions', []), 1):
                print(f"  {i}. {q}")
            
            new_question = input("Add new research question (or press enter to skip): ").strip()
            if new_question:
                plan['research_questions'].append(new_question)
                print("✅ Research question added")
        
        elif choice == '3':
            print("Current sections:")
            for i, section in enumerate(plan.get('main_sections', []), 1):
                print(f"  {i}. {section.get('title', 'N/A')}")
            
            section_note = input("Add focus note for any section: ").strip()
            if section_note:
                # Add to metadata for researcher to consider
                if 'modification_notes' not in plan['metadata']:
                    plan['metadata']['modification_notes'] = []
                plan['metadata']['modification_notes'].append(f"Section focus: {section_note}")
                print("✅ Section note added")
        
        if choice.lower() != 'done':
            return self._modify_plan(plan)  # Allow multiple modifications
        
        return plan
    
    def _export_plan(self, plan: Dict[str, Any]):
        """Export the research plan to file"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"research_plan_{timestamp}.json"
        filepath = f"data/{filename}"
        
        # Ensure data directory exists
        import os
        os.makedirs("data", exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(plan, f, indent=2)
        
        print(f"📁 Research plan saved to: {filepath}")
        return filepath

# Convenience function
def generate_research_plan(requirements: Dict[str, Any]) -> Dict[str, Any]:
    """Standalone function to generate research plan"""
    planner = ResearchPlanGenerator()
    return planner.generate_research_plan(requirements)
