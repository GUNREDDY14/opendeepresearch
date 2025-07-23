### CHECK THE OUTPUT IN .IPYNB notebooks


 ### Open Deep Researcher (ODR) System
A comprehensive, vendor-agnostic research automation system that leverages AI to conduct end-to-end research workflows, from topic clarification to professional report generation.

### Overview
The Open Deep Researcher (ODR) is a complete research automation pipeline designed to overcome vendor lock-in limitations by supporting any LLM provider that enables tool calling. The system runs entirely on local models using Ollama, ensuring zero API costs while maintaining professional-grade research capabilities.The ODR system follows a modular architecture with four distinct phases:

text
┌─────────────────────────────────────────────────────────────┐
│                   ODR System Workflow                       │
├─────────────────────────────────────────────────────────────┤
│  📋 Module 1: User Input & Clarification                   │
│     • Interactive requirement gathering                     │
│     • Intelligent gap identification                       │
│     • Automated progression control                        │
│                          ↓                                 │
│  📝 Module 2: Research Plan Generation                     │
│     • Structured plan creation                            │
│     • Section-based organization                          │
│     • Methodology definition                              │
│                          ↓                                 │
│  🔍 Module 3: Research Execution with Supervisor Node     │
│     • Intelligent source selection                        │
│     • Internal vs. external data routing                  │
│     • Parallel search execution                           │
│                          ↓                                 │
│  📄 Module 4: Report Generation                           │
│     • Professional Jupyter notebook output                │
│     • Proper citation management                          │
│     • Publication-ready formatting                        │
└─────────────────────────────────────────────────────────────┘
### Key Features
Vendor Independence
Universal LLM Client: Seamlessly works with Ollama, OpenAI, Anthropic, Google Gemini

Automatic Fallbacks: Graceful degradation when providers fail

Local-First Approach: Runs entirely on free local Ollama models

Cost-Effective: Zero ongoing API costs with local deployment

Intelligent Research Capabilities
Smart Supervisor Node: Decides between internal data sources and web search

Multi-Source Integration: Filesystem, MongoDB, SQL, and web APIs

Parallel Processing: Concurrent searches for maximum efficiency

Quality Filtering: Relevance scoring and source validation

### ## Quick Setup
Clone and Setup Environment

bash
git clone https://github.com/GUNREDDY14/opendeepresearch.git
cd opendeepresearch
python3 -m venv odr-env
source odr-env/bin/activate  # On Windows: odr-env\Scripts\activate
Install Dependencies

## bash
pip install -r requirements.txt
Setup Local AI Models

## bash
# Install Ollama
brew install ollama  # macOS
# Or download from https://ollama.ai for other platforms

# Start Ollama service
ollama serve

# Pull required models (in new terminal)
ollama pull llama3.2    # Primary research model
ollama pull codellama   # Technical content specialist
ollama pull mistral     # Fast response model
Verify Installation

bash
python test_config.py  # Test system configuration
🚀 Usage
Interactive Research Mode
bash
python odr_main.py
# Select option 1 for complete interactive workflow
This mode provides:

Guided topic clarification

Interactive plan review and modification

Real-time progress tracking

User validation at each phase

Quick Research Mode
bash
python odr_main.py
# Select option 2 and enter your research topic
Perfect for:

Rapid research tasks

Automated report generation

Batch processing multiple topics

Programmatic Usage
python
from odr_main import run_interactive_research, run_quick_research

# Complete interactive research
report = run_interactive_research()

# Quick research with specific parameters
report = run_quick_research("artificial intelligence in healthcare")

# Access generated notebook
notebook_cells = report.get('cells', [])
  
  
  ### Project Structure

opendeepresearch/
├── modules/                    # Core system modules
│   ├── user_input.py          # Module 1: Interactive requirement gathering
│   ├── research_planner.py    # Module 2: Structured plan generation
│   ├── research_executor.py   # Module 3: Intelligent data collection
│   ├── report_generator.py    # Module 4: Professional report creation
│   └── llm_client.py         # Universal LLM interface layer
├── config/                    # System configuration
│   └── api_keys.py           # Provider settings and API management
├── data/                     # Research data storage
│   ├── research_plans/       # Generated research plans
│   ├── research_data/        # Collected research information
│   └── cache/               # Performance optimization cache
├── outputs/                  # Generated reports and notebooks
├── tests/                   # Comprehensive test suite
│   ├── test_module1.py      # User input testing
│   ├── test_module2.py      # Plan generation testing
│   ├── test_module3.py      # Research execution testing
│   └── test_module4.py      # Report generation testing
├── odr_main.py             # Main system orchestrator
├── run_odr.py              # Simplified runner script
└── requirements.txt        # Python dependencies
🔧 Configuration
Environment Variables
Create a .env file in the project root:

text
# Ollama Configuration (Primary - Free)
OLLAMA_URL=http://localhost:11434
OLLAMA_PRIMARY_MODEL=llama3.2
OLLAMA_CODE_MODEL=codellama
OLLAMA_FAST_MODEL=mistral

# Optional: Cloud Provider API Keys
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
GOOGLE_API_KEY=your_google_key_here

# Research Configuration
MAX_SEARCH_RESULTS=10
DEFAULT_RESEARCH_DEPTH=intermediate
DEFAULT_CITATION_STYLE=APA
Model Selection Strategy
The system automatically selects optimal models for different tasks:

Research & Analysis: llama3.2 (comprehensive reasoning)

Technical Content: codellama (specialized domain knowledge)

Quick Tasks: mistral (speed-optimized responses)

🧪 Testing
Run comprehensive tests to verify system functionality:

bash
# Test individual modules
python test_module1.py  # User input and clarification
python test_module2.py  # Research plan generation
python test_module3.py  # Research execution and data gathering
python test_module4.py  # Report generation and formatting

# Test system configuration
python test_config.py   # Verify LLM connections and settings
