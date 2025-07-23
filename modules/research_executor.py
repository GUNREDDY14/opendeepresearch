"""
Module 3: Research Execution with Supervisor Node - FIXED VERSION
Actually working web scraping and content extraction
"""

import json
import os
import time
import requests
from datetime import datetime
from typing import Dict, List, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import sqlite3
from modules.llm_client import create_llm_client

class SupervisorNode:
    """
    Fixed supervisor that actually works
    """
    
    def __init__(self, llm_client=None):
        self.llm_client = llm_client or create_llm_client()
    
    def decide_research_strategy(self, section: Dict[str, Any]) -> Dict[str, Any]:
        """Simplified strategy that actually works"""
        
        section_title = section.get('title', 'Unknown Section')
        print(f"🧠 Supervisor analyzing: {section_title}")
        
        # Simple but working strategy
        strategy = {
            "check_internal_first": True,
            "web_searches_needed": ["general", "academic"],
            "minimum_sources": 3,
            "search_terms": self._extract_search_terms(section_title),
            "parallel_execution": False  # Sequential to avoid issues
        }
        
        print(f"✅ Strategy: Search for {strategy['search_terms']}")
        return strategy
    
    def _extract_search_terms(self, section_title: str) -> List[str]:
        """Extract meaningful search terms from section title"""
        
        # Simple keyword extraction
        words = section_title.lower().split()
        
        # Remove common words
        stop_words = {'and', 'the', 'of', 'in', 'for', 'with', 'on', 'at', 'by', 'from'}
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Add the full section title as first search term
        search_terms = [section_title]
        
        # Add individual keywords
        search_terms.extend(keywords[:3])  # Max 3 additional terms
        
        return search_terms
    
    def search_internal_sources(self, search_terms: List[str]) -> List[Dict[str, Any]]:
        """Search internal sources - simplified"""
        
        print("📁 Searching internal sources...")
        results = []
        
        # Check if we have any local files
        search_dirs = ["./data", "./documents", "./research"]
        
        for directory in search_dirs:
            if os.path.exists(directory):
                for root, dirs, files in os.walk(directory):
                    for file in files:
                        if file.endswith(('.txt', '.md', '.json')):
                            file_path = os.path.join(root, file)
                            results.append({
                                "source": "filesystem",
                                "title": file,
                                "content": f"Local file: {file_path}",
                                "url": file_path,
                                "type": "internal"
                            })
        
        print(f"📁 Found {len(results)} internal results")
        return results
    
    def search_web_sources(self, search_terms: List[str]) -> List[Dict[str, Any]]:
        """Actually working web search"""
        
        print("🌐 Searching web sources...")
        results = []
        
        for term in search_terms[:2]:  # Limit to 2 terms
            print(f"  Searching for: {term}")
            
            # Use a simple but working approach
            search_results = self._simple_web_search(term)
            results.extend(search_results)
            
            time.sleep(2)  # Be respectful to servers
        
        print(f"🌐 Found {len(results)} web results")
        return results
    
    def _simple_web_search(self, query: str) -> List[Dict[str, Any]]:
        """Simple working web search using Wikipedia API"""
        
        results = []
        
        try:
            # Use Wikipedia API - more reliable than scraping
            wiki_url = "https://en.wikipedia.org/api/rest_v1/page/summary/"
            search_url = f"https://en.wikipedia.org/w/api.php"
            
            # First, search for pages
            search_params = {
                'action': 'query',
                'format': 'json',
                'list': 'search',
                'srsearch': query,
                'srlimit': 3
            }
            
            response = requests.get(search_url, params=search_params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'query' in data and 'search' in data['query']:
                    for result in data['query']['search']:
                        title = result.get('title', '')
                        snippet = result.get('snippet', '').replace('<span class="searchmatch">', '').replace('</span>', '')
                        
                        # Get full summary for this page
                        try:
                            summary_response = requests.get(f"{wiki_url}{title.replace(' ', '_')}", timeout=5)
                            if summary_response.status_code == 200:
                                summary_data = summary_response.json()
                                content = summary_data.get('extract', snippet)
                            else:
                                content = snippet
                        except:
                            content = snippet
                        
                        if title and content and len(content) > 50:
                            results.append({
                                "source": "wikipedia",
                                "title": title,
                                "content": content,
                                "url": f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
                                "snippet": snippet,
                                "type": "external"
                            })
            
            # Also try a simple Google-like search using DuckDuckGo Instant Answer API
            try:
                ddg_url = f"https://api.duckduckgo.com/?q={query}&format=json&no_redirect=1&skip_disambig=1"
                ddg_response = requests.get(ddg_url, timeout=5)
                
                if ddg_response.status_code == 200:
                    ddg_data = ddg_response.json()
                    
                    # Get abstract if available
                    if ddg_data.get('Abstract'):
                        results.append({
                            "source": "duckduckgo",
                            "title": f"DuckDuckGo: {query}",
                            "content": ddg_data['Abstract'],
                            "url": ddg_data.get('AbstractURL', ''),
                            "snippet": ddg_data['Abstract'][:200] + "...",
                            "type": "external"
                        })
                    
                    # Get related topics
                    for topic in ddg_data.get('RelatedTopics', [])[:2]:
                        if isinstance(topic, dict) and topic.get('Text'):
                            results.append({
                                "source": "duckduckgo_related",
                                "title": f"Related: {topic.get('Text', '')[:50]}...",
                                "content": topic.get('Text', ''),
                                "url": topic.get('FirstURL', ''),
                                "snippet": topic.get('Text', '')[:200] + "...",
                                "type": "external"
                            })
            
            except Exception as e:
                print(f"    ⚠️ DuckDuckGo search failed: {e}")
        
        except Exception as e:
            print(f"    ⚠️ Wikipedia search failed: {e}")
        
        return results


class ResearchExecutor:
    """
    Fixed research executor that actually works
    """
    
    def __init__(self, llm_client=None):
        self.llm_client = llm_client or create_llm_client()
        self.supervisor = SupervisorNode(llm_client)
    
    def execute_research_plan(self, research_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute research plan - fixed version"""
        
        print("🚀 Research Execution Engine - FIXED VERSION")
        print("=" * 60)
        print(f"Executing: {research_plan.get('title', 'Unknown')}")
        print()
        
        research_data = {
            "metadata": {
                "execution_started": datetime.now().isoformat(),
                "plan_title": research_plan.get('title', ''),
                "total_sections": len(research_plan.get('main_sections', []))
            },
            "sections_data": {},
            "summary": {
                "total_sources": 0,
                "internal_sources": 0,
                "external_sources": 0
            }
        }
        
        # Execute research for each section
        main_sections = research_plan.get('main_sections', [])
        
        for i, section in enumerate(main_sections, 1):
            section_title = section.get('title', f'Section_{i}')
            print(f"📋 Section {i}/{len(main_sections)}: {section_title}")
            
            # Get strategy
            strategy = self.supervisor.decide_research_strategy(section)
            
            # Execute research
            section_data = self._execute_section_research(section, strategy)
            
            # Store results
            research_data['sections_data'][section_title] = section_data
            
            # Update summary
            research_data['summary']['total_sources'] += len(section_data['all_sources'])
            research_data['summary']['internal_sources'] += len(section_data['internal_sources'])
            research_data['summary']['external_sources'] += len(section_data['external_sources'])
            
            print(f"✅ Section {i} complete: {len(section_data['all_sources'])} sources found")
            print()
        
        # Finalize
        research_data['metadata']['execution_completed'] = datetime.now().isoformat()
        
        # Save data
        self._save_research_data(research_data)
        
        print("🎉 Research execution completed successfully!")
        print(f"📊 Total: {research_data['summary']['total_sources']} sources across {len(main_sections)} sections")
        
        return research_data
    
    def _execute_section_research(self, section: Dict[str, Any], strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Execute research for one section - actually working"""
        
        section_data = {
            "section_title": section.get('title', ''),
            "strategy": strategy,
            "internal_sources": [],
            "external_sources": [],
            "all_sources": [],
            "processed_content": []
        }
        
        search_terms = strategy['search_terms']
        
        # Step 1: Internal sources
        if strategy.get('check_internal_first', True):
            internal_results = self.supervisor.search_internal_sources(search_terms)
            section_data['internal_sources'] = internal_results
        
        # Step 2: External sources
        external_results = self.supervisor.search_web_sources(search_terms)
        section_data['external_sources'] = external_results
        
        # Step 3: Combine and process
        all_sources = section_data['internal_sources'] + section_data['external_sources']
        section_data['all_sources'] = all_sources
        
        # Step 4: Process content with LLM
        if all_sources:
            processed_content = self._process_sources_with_llm(all_sources, section)
            section_data['processed_content'] = processed_content
        
        return section_data
    
    def _process_sources_with_llm(self, sources: List[Dict[str, Any]], section: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Process sources with LLM - actually working version"""
        
        print("  🤖 Processing content with AI...")
        
        processed = []
        
        # Process sources in small batches
        for i, source in enumerate(sources[:5]):  # Limit to 5 sources
            try:
                content = source.get('content', '')
                
                if len(content) < 50:  # Skip sources with too little content
                    continue
                
                # Create a simple, working prompt
                prompt = f"""
                Research Section: {section.get('title', '')}
                
                Source Title: {source.get('title', 'Unknown')}
                Source Content: {content[:800]}
                
                Summarize the key points from this source that are relevant to the research section.
                Provide 2-3 main insights in simple bullet points.
                
                Format:
                • Key insight 1
                • Key insight 2  
                • Key insight 3 (if applicable)
                """
                
                response = self.llm_client.generate(
                    prompt,
                    task_type="analysis", 
                    max_tokens=300,
                    temperature=0.3
                )
                
                if response and not response.startswith("Error:") and len(response) > 20:
                    processed.append({
                        "source_title": source.get('title', 'Unknown'),
                        "source_url": source.get('url', ''),
                        "source_type": source.get('source', 'unknown'),
                        "key_insights": response.strip(),
                        "original_content": content[:200] + "..." if len(content) > 200 else content
                    })
                    print(f"    ✅ Processed source {i+1}: {source.get('title', 'Unknown')[:50]}...")
                else:
                    print(f"    ⚠️ Failed to process source {i+1}")
                
                time.sleep(1)  # Small delay between LLM calls
                
            except Exception as e:
                print(f"    ❌ Error processing source {i+1}: {e}")
                continue
        
        print(f"  🤖 Successfully processed {len(processed)} sources")
        return processed
    
    def _save_research_data(self, research_data: Dict[str, Any]):
        """Save research data"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"research_data_fixed_{timestamp}.json"
        filepath = f"data/{filename}"
        
        os.makedirs("data", exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(research_data, f, indent=2)
        
        print(f"💾 Research data saved to: {filepath}")
        return filepath


# Fixed convenience function
def execute_research(research_plan: Dict[str, Any]) -> Dict[str, Any]:
    """Execute research plan - fixed version"""
    executor = ResearchExecutor()
    return executor.execute_research_plan(research_plan)
