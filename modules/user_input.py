"""
Module 1: User Input and Clarification System
Intelligently gathers and clarifies research requirements
"""

import json
from typing import Dict, List, Any
from modules.llm_client import create_llm_client

class UserInputModule:
    """
    Handles interactive user input collection with intelligent clarification
    """
    
    def __init__(self, llm_client=None):
        self.llm_client = llm_client or create_llm_client()
        self.required_fields = {
            "research_topic": "Main research subject or question",
            "target_audience": "Who will read this research",
            "scope": "Breadth and boundaries of research",
            "depth_level": "How detailed should the analysis be",
            "specific_questions": "Particular aspects to focus on",
            "output_format": "Preferred presentation style"
        }
        self.collected_data = {}
    
    def collect_research_requirements(self) -> Dict[str, Any]:
        """
        Main entry point - collects all research requirements interactively
        Returns structured requirements ready for research planning
        """
        
        print("🔍 Open Deep Researcher - Input Collection")
        print("=" * 50)
        print("Let's gather your research requirements step by step.\n")
        
        # Step 1: Get initial topic
        self._collect_initial_topic()
        
        # Step 2: Intelligent clarification
        self._intelligent_clarification()
        
        # Step 3: Validate and finalize
        final_requirements = self._validate_and_finalize()
        
        # Step 4: Auto-progress check
        if self._ready_for_next_module(final_requirements):
            print("\n✅ Requirements complete! Ready for research planning.")
            return final_requirements
        else:
            print("\n⚠️ Some requirements still unclear. Let's refine them.")
            return self.collect_research_requirements()  # Recursive refinement
    
    def _collect_initial_topic(self):
        """Collect the basic research topic"""
        print("📝 Step 1: Research Topic")
        
        topic = input("What would you like to research? ")
        while not topic.strip():
            topic = input("Please enter a research topic: ")
        
        self.collected_data["research_topic"] = topic.strip()
        print(f"✅ Research Topic: {self.collected_data['research_topic']}\n")
    
    def _intelligent_clarification(self):
        """Use LLM to identify missing information and ask smart questions"""
        print("🤔 Step 2: Intelligent Clarification")
        print("Analyzing your topic to identify missing information...\n")
        
        # Generate clarification questions using LLM
        clarification_prompt = f"""
        Research Topic: "{self.collected_data['research_topic']}"
        
        As a research assistant, analyze this topic and identify what additional information is needed for a comprehensive research project. Consider:
        
        - Target audience (academic, business, general public, students)
        - Scope (broad overview, specific analysis, comparative study, historical perspective)
        - Depth level (introductory, intermediate, expert, comprehensive)
        - Specific focus areas or questions within the topic
        - Preferred output format (academic paper, business report, blog post, presentation)
        - Any time constraints or current relevance factors
        
        Generate 4-6 specific, clear questions to ask the user. Each question should:
        1. Be easy to understand
        2. Help narrow down the research focus
        3. Provide actionable information for research planning
        
        Format as a numbered list with clear, conversational questions.
        """
        
        questions_response = self.llm_client.generate(
            clarification_prompt, 
            task_type="research", 
            max_tokens=600,
            temperature=0.3  # More focused responses
        )
        
        if "Error:" in questions_response:
            # Fallback to manual questions if LLM fails
            self._manual_clarification()
            return
        
        print("Based on your topic, I have some clarifying questions:\n")
        print(questions_response)
        
        # Collect responses to generated questions
        self._collect_clarification_responses(questions_response)
    
    def _collect_clarification_responses(self, questions_text: str):
        """Collect user responses to the generated clarification questions"""
        
        print("\n" + "─" * 50)
        print("Please answer the questions above (you can skip any by typing 'skip'):\n")
        
        responses = {}
        question_count = questions_text.count('\n') + 1
        
        for i in range(1, min(question_count + 1, 7)):  # Max 6 questions
            response = input(f"Response to question {i}: ").strip()
            if response.lower() not in ['skip', 'pass', '']:
                responses[f"clarification_{i}"] = response
        
        self.collected_data.update(responses)
        
        # Generate structured fields from responses
        self._structure_responses()
    
    def _structure_responses(self):
        """Convert clarification responses into structured fields"""
        
        # Combine all user inputs for analysis
        all_responses = {
            "topic": self.collected_data["research_topic"],
            "responses": {k: v for k, v in self.collected_data.items() if k.startswith("clarification_")}
        }
        
        structuring_prompt = f"""
        Research Topic: {all_responses['topic']}
        User Responses: {json.dumps(all_responses['responses'], indent=2)}
        
        Based on this information, extract and structure the research requirements into these specific fields:
        
        1. target_audience: Who will read this (be specific)
        2. scope: Research boundaries and breadth
        3. depth_level: Level of detail needed
        4. specific_questions: Key questions to answer (list 2-4)
        5. output_format: How results should be presented
        6. research_approach: Suggested methodology
        
        Format as JSON with clear, actionable values for each field.
        If information is missing, use "Not specified" for that field.
        """
        
        structured_response = self.llm_client.generate(
            structuring_prompt,
            task_type="analysis",
            max_tokens=500,
            temperature=0.2
        )
        
        try:
            # Try to parse JSON response
            structured_data = json.loads(structured_response)
            self.collected_data.update(structured_data)
        except json.JSONDecodeError:
            # Fallback: extract manually
            self._manual_structuring()
    
    def _manual_clarification(self):
        """Fallback clarification when LLM is unavailable"""
        questions = [
            ("target_audience", "Who is your target audience? (students, professionals, general public, etc.)"),
            ("scope", "What's the scope of your research? (broad overview, specific analysis, comparison, etc.)"),
            ("depth_level", "How detailed should the research be? (basic, intermediate, comprehensive)"),
            ("specific_questions", "Any specific questions you want answered?"),
            ("output_format", "How would you like the results presented? (report, presentation, article, etc.)")
        ]
        
        for field, question in questions:
            response = input(f"{question}: ").strip()
            if response:
                self.collected_data[field] = response
    
    def _manual_structuring(self):
        """Fallback structuring when LLM parsing fails"""
        defaults = {
            "target_audience": "General audience",
            "scope": "Comprehensive overview",
            "depth_level": "Intermediate",
            "specific_questions": ["Key concepts", "Current developments", "Practical applications"],
            "output_format": "Research report",
            "research_approach": "Multi-source analysis"
        }
        
        for field, default_value in defaults.items():
            if field not in self.collected_data:
                self.collected_data[field] = default_value
    
    def _validate_and_finalize(self) -> Dict[str, Any]:
        """Show collected requirements and allow user to modify"""
        
        print("\n" + "=" * 50)
        print("📋 Collected Research Requirements")
        print("=" * 50)
        
        # Display collected requirements
        display_fields = {
            "research_topic": "Research Topic",
            "target_audience": "Target Audience", 
            "scope": "Research Scope",
            "depth_level": "Depth Level",
            "specific_questions": "Specific Questions",
            "output_format": "Output Format"
        }
        
        for field, label in display_fields.items():
            value = self.collected_data.get(field, "Not specified")
            if isinstance(value, list):
                value = ", ".join(value)
            print(f"{label:18}: {value}")
        
        print("=" * 50)
        
        # Allow modifications
        modify = input("\nWould you like to modify any requirements? (y/n): ").lower()
        
        if modify == 'y':
            self._modify_requirements()
        
        return self.collected_data
    
    def _modify_requirements(self):
        """Allow user to modify specific requirements"""
        
        modifiable_fields = {
            "1": ("research_topic", "Research Topic"),
            "2": ("target_audience", "Target Audience"),
            "3": ("scope", "Research Scope"), 
            "4": ("depth_level", "Depth Level"),
            "5": ("output_format", "Output Format")
        }
        
        print("\nWhich field would you like to modify?")
        for key, (field, label) in modifiable_fields.items():
            print(f"{key}. {label}")
        
        choice = input("Enter number (or 'done' to finish): ").strip()
        
        if choice in modifiable_fields:
            field, label = modifiable_fields[choice]
            new_value = input(f"New {label}: ").strip()
            if new_value:
                self.collected_data[field] = new_value
                print(f"✅ Updated {label}")
        
        if choice.lower() != 'done':
            self._modify_requirements()  # Allow multiple modifications
    
    def _ready_for_next_module(self, requirements: Dict[str, Any]) -> bool:
        """Check if requirements are complete enough for research planning"""
        
        essential_fields = ["research_topic", "target_audience", "scope"]
        
        for field in essential_fields:
            if field not in requirements or not requirements[field] or requirements[field] == "Not specified":
                return False
        
        return True
    
    def export_requirements(self, filename: str = None) -> str:
        """Export requirements to JSON file"""
        
        if not filename:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"research_requirements_{timestamp}.json"
        
        filepath = f"data/{filename}"
        
        with open(filepath, 'w') as f:
            json.dump(self.collected_data, f, indent=2)
        
        print(f"📁 Requirements saved to: {filepath}")
        return filepath

# Convenience function for external use
def collect_user_requirements():
    """Standalone function to collect user requirements"""
    input_module = UserInputModule()
    return input_module.collect_research_requirements()
