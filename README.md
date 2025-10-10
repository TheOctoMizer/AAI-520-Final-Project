# AAI-520 Final Project: Autonomous Investment Research Agent

A real-world financial analysis system powered by agentic AI, demonstrating autonomous reasoning, planning, and self-improvement through multiple specialized LLM agents.

## Project Overview

This project implements an autonomous investment research system that goes beyond traditional scripted pipelines. The system features:

- **Autonomous Agent**: Plans research, executes dynamically, reflects on quality, and learns across runs
- **Multiple Workflow Patterns**: Prompt chaining, intelligent routing, and evaluator-optimizer patterns
- **Knowledge Graph Integration**: Entity extraction and relationship mapping for comprehensive market understanding
- **Self-Improvement**: Iterative refinement based on quality evaluation and feedback

## Architecture

```
Autonomous Research Agent
├── Research Planning (autonomous task decomposition)
├── Dynamic Tool Selection
│   ├── Knowledge Graph Builder (entity extraction & expansion)
│   ├── Financial Data Fetchers (Alpha Vantage, Yahoo Finance)
│   ├── News Analyzers (Wikipedia, DuckDuckGo)
│   └── Workflow Orchestration
├── Three Workflow Patterns
│   ├── Prompt Chaining: News → Preprocess → Classify → Extract → Summarize
│   ├── Routing: Content → Router → Specialist Analysts
│   └── Evaluator-Optimizer: Generate → Evaluate → Refine
└── Self-Reflection & Learning (cross-run memory)
```

## Project Structure

```
AAI-520-Final-Project/
├── agents/
│   ├── __init__.py
│   └── research_agent.py          # Main autonomous agent
├── workflows/
│   ├── __init__.py
│   ├── prompt_chaining.py         # Workflow Pattern 1
│   ├── routing.py                 # Workflow Pattern 2
│   ├── evaluator_optimizer.py    # Workflow Pattern 3
│   └── demo_all_workflows.py      # Demonstration script
├── utils/
│   ├── __init__.py
│   ├── config.py                  # Configuration settings
│   ├── llm_factory.py             # LLM instance creation
│   ├── data_models.py             # Pydantic models
│   ├── data_fetchers.py           # Financial data sources
│   └── knowledge_graph.py         # Graph construction
├── memory/
│   └── __init__.py
├── main.py                        # Main entry point
├── pyproject.toml                 # Dependencies
└── README.md
```

## Requirements Met

### Agent Functions (33.8%)

✅ **Plans Research Steps**: Agent autonomously creates research plans with ordered steps, data source requirements, and key questions

✅ **Uses Tools Dynamically**: Selects and applies appropriate tools based on the research plan:
- Alpha Vantage API for stock quotes
- Yahoo Finance for news
- Wikipedia & DuckDuckGo for background research
- Knowledge graph expansion for entity relationships
- Multiple LLM-based analyzers

✅ **Self-Reflects on Quality**: Evaluates its own output across multiple dimensions:
- Completeness score
- Confidence score
- Data quality assessment
- Identifies strengths, gaps, and reliability concerns

✅ **Learns Across Runs**: Maintains a memory file that stores:
- Improvement recommendations from past runs
- Gaps to avoid
- Quality assessments
- Feeds learnings into future research planning

### Workflow Patterns (33.8%)

✅ **Prompt Chaining**: Sequential pipeline for news analysis
- Step 1: Ingest raw news data
- Step 2: Preprocess and clean content
- Step 3: Classify by category and sentiment
- Step 4: Extract entities and key facts
- Step 5: Summarize with investment implications

✅ **Routing**: Intelligent content distribution to specialists
- Router analyzes content type
- Routes to appropriate specialist:
  - Earnings Analyst (financial reports, metrics)
  - News Analyst (events, announcements, impacts)
  - Market Analyst (trends, technical signals)
- Each specialist provides domain-specific analysis

✅ **Evaluator-Optimizer**: Iterative self-improvement
- Generate initial investment analysis
- Evaluate quality (completeness, accuracy, actionability)
- Refine based on specific feedback
- Re-evaluate until quality threshold met
- Multiple iterations with score progression tracking

## Installation

### Prerequisites

- Python 3.12+
- LM Studio running locally (or modify config for OpenAI API)
- Alpha Vantage API key

### Setup

1. **Clone the repository**
```bash
cd AAI-520-Final-Project
git checkout feature/autonomous-research
```

2. **Install dependencies**
```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

3. **Set up environment variables**
```bash
export ALPHA_VANTAGE_KEY="your_api_key_here"
```

4. **Configure LM Studio** (if using local models)
- Start LM Studio server on port 1234
- Load models:
  - Chat model: `gemma-3-27b-it` (or similar)
  - Extraction model: `qwen/qwen3-next-80b` (or similar)

## Usage

### Quick Start: Run All Demonstrations

```bash
python workflows/demo_all_workflows.py
```

This demonstrates all three workflow patterns with sample data.

### Run Autonomous Research Agent

```bash
python agents/research_agent.py
```

Or use programmatically:

```python
from agents.research_agent import AutonomousResearchAgent

agent = AutonomousResearchAgent()

result = agent.research_stock(
    ticker="AAPL",
    user_context="Long-term growth analysis"
)

print(f"Recommendation: {result.investment_analysis['recommendation']}")
print(f"Quality Score: {result.reflection.completeness_score:.1f}/100")
```

### Individual Workflow Patterns

**Prompt Chaining:**
```python
from workflows.prompt_chaining import PromptChainWorkflow

workflow = PromptChainWorkflow()
summary = workflow.run(news_text, source="Reuters")
```

**Routing:**
```python
from workflows.routing import RoutingWorkflow

workflow = RoutingWorkflow()
result = workflow.process(content, title="Market Update")
```

**Evaluator-Optimizer:**
```python
from workflows.evaluator_optimizer import EvaluatorOptimizerWorkflow

workflow = EvaluatorOptimizerWorkflow(max_iterations=3)
result = workflow.run(ticker="MSFT", company_data=data)
```

### Knowledge Graph

```python
from utils.knowledge_graph import KnowledgeGraphBuilder

builder = KnowledgeGraphBuilder()
graph = builder.expand_from_seed("TSLA", depth=2)
print(builder.get_graph_summary())
```

## Key Features

### 1. Autonomous Planning

The agent creates comprehensive research plans:
```python
ResearchPlan:
  - research_steps: ["Fetch financial data", "Analyze news sentiment", ...]
  - data_sources_needed: ["Alpha Vantage", "Yahoo Finance", ...]
  - key_questions: ["What are the growth drivers?", ...]
  - estimated_complexity: "medium"
```

### 2. Dynamic Tool Selection

Based on the plan, the agent automatically:
- Builds knowledge graphs when entity relationships are needed
- Fetches news when sentiment analysis is required
- Routes to specialists for domain-specific analysis
- Applies evaluator-optimizer for comprehensive reports

### 3. Self-Reflection

After each research run:
```python
ResearchReflection:
  - completeness_score: 85.0
  - confidence_score: 78.0
  - gaps: ["Missing competitor analysis", "No technical indicators"]
  - improvement_recommendations: ["Include sector comparison", ...]
```

### 4. Cross-Run Learning

Learnings are stored in `agent_memory.txt` and fed into future planning:
```
Run: High quality analysis with good data coverage
Improvements to apply:
- Include more forward-looking metrics
- Compare against sector benchmarks
Gaps to avoid:
- Missing regulatory context
```

## Configuration

Edit `utils/config.py` to customize:

```python
# LLM Configuration
LMSTUDIO_URL = "http://localhost:1234/v1"
LLM_NAME = "gemma-3-27b-it"

# API Keys
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_KEY')

# Parameters
FETCH_DELAY_SECONDS = 1.5  # Rate limiting
```

## Data Sources

- **Alpha Vantage**: Real-time stock quotes and fundamentals
- **Yahoo Finance**: Recent news and market data
- **Wikipedia**: Company background and executive info
- **DuckDuckGo**: Policy news and current events

## Technical Highlights

### Structured Outputs with Pydantic

All workflows use Pydantic models for type-safe, validated outputs:
```python
class NewsClassification(BaseModel):
    category: str = Field(description="earnings, market_analysis, policy, ...")
    sentiment: str = Field(description="positive, negative, neutral")
    relevance_score: float = Field(description="0-1")
```

### LangChain Integration

- `ChatOpenAI` for LLM calls
- `with_structured_output()` for typed responses
- `ChatPromptTemplate` for prompt management
- Community tools (Yahoo Finance, Wikipedia, DuckDuckGo)

### NetworkX Knowledge Graphs

- Entities as nodes with labels and confidence
- Relationships as edges with context
- Multi-layer expansion from seed entities
- Graph analytics (degree centrality, clustering)

## Demonstrations

Each workflow includes a standalone demonstration:

```bash
# Prompt Chaining demo
python -c "from workflows.prompt_chaining import demonstrate_prompt_chaining; demonstrate_prompt_chaining()"

# Routing demo
python -c "from workflows.routing import demonstrate_routing; demonstrate_routing()"

# Evaluator-Optimizer demo
python -c "from workflows.evaluator_optimizer import demonstrate_evaluator_optimizer; demonstrate_evaluator_optimizer()"

# Full autonomous agent demo
python -c "from agents.research_agent import demonstrate_autonomous_agent; demonstrate_autonomous_agent()"
```

## Testing & Validation

The system demonstrates:

1. **Workflow Patterns**: Each pattern runs independently with example data
2. **Agent Autonomy**: Plans, executes, reflects without human intervention
3. **Quality Improvement**: Scores increase across evaluator-optimizer iterations
4. **Learning**: Memory file shows accumulated learnings
5. **Integration**: All components work together in autonomous agent

## Future Enhancements

- Database persistence for knowledge graphs (SQLite/ChromaDB)
- Web interface for interactive research
- Real-time market data streaming
- Backtesting framework for recommendations
- Multi-agent collaboration (research team simulation)
- RAG integration for document analysis

## Project Requirements Checklist

### Agent Functions (4/4)
- [x] Plans research steps autonomously
- [x] Uses tools dynamically (APIs, datasets, retrieval)
- [x] Self-reflects to assess output quality
- [x] Learns across runs (memory/notes)

### Workflow Patterns (3/3)
- [x] Prompt Chaining: Ingest → Preprocess → Classify → Extract → Summarize
- [x] Routing: Content → Router → Specialist Analyzers
- [x] Evaluator-Optimizer: Generate → Evaluate → Refine

### Technical Implementation
- [x] LangChain integration
- [x] Pydantic structured outputs
- [x] Multiple data sources (APIs, search, knowledge bases)
- [x] Graph-based entity modeling
- [x] Modular, maintainable architecture
- [x] Comprehensive documentation

## Implementation Details

For detailed implementation information, code metrics, and requirements coverage, see [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md).

This document provides:
- Complete requirements coverage mapping
- Code metrics and file structure
- Technical implementation details
- Testing framework overview
- Deliverables checklist

## Team Members

[Your team members here]

## License

Academic project for AAI-520 course.

## Acknowledgments

- LangChain for agent framework
- Alpha Vantage for financial data API
- Yahoo Finance for news data
- NetworkX for graph algorithms
