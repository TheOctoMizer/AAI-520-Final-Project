# AAI-520 Final Project: Autonomous Investment Research Agent

A real-world financial analysis system powered by agentic AI, demonstrating autonomous reasoning, planning, and self-improvement through multiple specialized LLM agents.

## Project Overview

This project implements an autonomous investment research system that goes beyond traditional scripted pipelines. The system features:

- **Autonomous Agent**: Plans research, executes dynamically, reflects on quality, and learns across runs
- **Multiple Workflow Patterns**: Prompt chaining, intelligent routing, and evaluator-optimizer patterns
- **Knowledge Graph Integration**: Entity extraction and relationship mapping with LLM-powered summarization
- **Self-Improvement**: Iterative refinement based on quality evaluation and feedback

## Architecture

```
Autonomous Research Agent
├── Research Planning (autonomous task decomposition)
├── Dynamic Tool Selection
│   ├── Knowledge Graph Builder (entity extraction & LLM summarization)
│   ├── Financial Data Fetchers (Alpha Vantage, Yahoo Finance)
│   ├── News Analyzers (Wikipedia, DuckDuckGo)
│   └── Workflow Orchestration
├── Three Workflow Patterns
│   ├── Prompt Chaining: News → Preprocess → Classify → Extract → Summarize
│   ├── Routing: Content → Router → Specialist Analysts
│   └── Evaluator-Optimizer: Generate → Evaluate → Refine
└── Self-Reflection & Learning (cross-run memory)
```

## Submission Files

```
AAI-520-Final-Project/
├── autonomous_research_agent.ipynb  # Complete implementation in single notebook
└── README.md                        # This file
```

**All code is consolidated into the Jupyter notebook** - agents, workflows, utilities, and demonstrations are included in a single, self-contained file.

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
- LM Studio running locally
- Alpha Vantage API key
- Jupyter Notebook

### LLM Configuration

The notebook is configured to use:

```python
# Main chat model
LLM_NAME = "gemma-3-27b-it"

# Entity extraction model
ENTITY_EXTRACTOR = "qwen/qwen3-next-80b"

# LM Studio connection
LMSTUDIO_URL = "http://localhost:1234/v1"
```

### Setup

1. **Install LM Studio**
   - Download from https://lmstudio.ai/
   - Load the required models:
     - `gemma-3-27b-it` (main chat model)
     - `qwen/qwen3-next-80b` (entity extraction)
   - Start the local server on port 1234

2. **Set API Key**
   ```bash
   export ALPHA_VANTAGE_KEY="your_api_key_here"
   ```
   Or set it directly in the notebook configuration cell.

3. **Install Python Dependencies**
   ```bash
   pip install jupyter langchain langchain-openai langchain-community \
               yfinance wikipedia duckduckgo-search networkx pydantic requests
   ```

4. **Run the Notebook**
   ```bash
   jupyter notebook autonomous_research_agent.ipynb
   ```

   Or using Jupyter Lab:
   ```bash
   jupyter lab autonomous_research_agent.ipynb
   ```

   **Notebook location**: `autonomous_research_agent.ipynb`

## Usage

### Running the Complete Agent

The notebook includes a demonstration cell that runs the complete autonomous research workflow:

```python
# Change the ticker and context as needed
ticker = "AAPL"
context = "Looking for long-term growth potential in tech sector"

# Run autonomous research
result = agent.research_stock(ticker=ticker, user_context=context)
```

The agent will:
1. **Plan** the research with autonomous step decomposition
2. **Execute** using dynamic tool selection:
   - Build knowledge graph
   - Fetch news and analyze
   - Route to specialist analysts
   - Generate investment analysis with iterative refinement
3. **Reflect** on the quality of its research
4. **Learn** by storing insights for future runs

### Individual Workflow Demonstrations

Each workflow pattern has its own demonstration cell in the notebook:

**Prompt Chaining Demo**: Process news articles through the sequential pipeline

**Routing Demo**: Distribute different content types to appropriate specialists

**Evaluator-Optimizer Demo**: Generate and iteratively refine investment analysis

### Knowledge Graph with LLM Summarization

The notebook includes an enhanced knowledge graph builder with LLM-powered summarization:

```python
builder = KnowledgeGraphBuilder()

# Expand graph with configurable depth
graph = builder.expand_from_seed("TSLA", depth=2)

# Get standard structural summary
print(builder.get_graph_summary())

# NEW: Generate LLM-powered investment insights
llm_insights = builder.generate_llm_summary(focus_entity="TSLA")
print(llm_insights)
```

**Depth levels** (inspired by chyavan's graph exploration):
- `depth=1`: Direct connections (immediate relationships)
- `depth=2`: Second-degree connections (connections of connections) - default
- `depth=3`: Extended network (third-degree connections)

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

### 5. LLM-Powered Knowledge Graph Summarization (NEW)

Enhanced knowledge graph builder with intelligent narrative summarization:

**What it analyzes:**
- Network centrality (who are the key players?)
- Relationship patterns (what connections matter?)
- Investment implications (what does the structure reveal?)
- Entity significance (why does this entity matter?)

This goes beyond simple node/edge listings to provide actionable investment insights.

## Data Sources

- **Alpha Vantage**: Real-time stock quotes and fundamentals
- **Yahoo Finance**: Recent news and market data
- **Wikipedia**: Company background and executive info
- **DuckDuckGo**: Policy news and current events

## Technical Highlights

### Pydantic Data Models

All workflow outputs use structured Pydantic models for type safety and validation:
- NewsArticle, PreprocessedNews, NewsClassification
- ExtractedEntities, NewsSummary
- RoutingDecision, EarningsAnalysis, NewsAnalysis, MarketAnalysis
- InvestmentAnalysis, QualityEvaluation
- ResearchPlan, ResearchReflection, ResearchResult

### LangChain Integration

- ChatOpenAI for LLM interactions
- Structured outputs with `.with_structured_output()`
- ChatPromptTemplate for consistent prompting
- Community tools (Yahoo Finance, Wikipedia, DuckDuckGo)

### NetworkX Graph Analysis

- Entity relationship mapping
- Degree centrality for hub identification
- Graph traversal and expansion
- LLM-powered graph interpretation

### Workflow Orchestration

Three distinct agentic patterns:
1. **Sequential**: Pipeline with state passing between steps
2. **Parallel**: Intelligent routing to specialized agents
3. **Iterative**: Quality-driven refinement loop

## Novel Contributions

1. **LLM-Powered Graph Summarization**
   - First-of-its-kind narrative insights from graph structure
   - Investment-focused analysis using NetworkX centrality
   - Depth-aware prompting for context

2. **Integration from Chyavan's Work**
   - Layer-based depth exploration (depth 1-3)
   - Financial entity taxonomy (8 categories)
   - Category-aware data fetching

3. **Complete Autonomous Loop**
   - Self-contained planning → execution → reflection → learning cycle
   - Cross-run memory and improvement
   - Quality-driven iterative refinement

## License

Academic project for AAI-520 course.

## Authors

Marco Gonzalez  mantonio@sandiego.edu
Chyavan Shenoy  cshenoy@sandiego.edu
Prakruti Rao    prao@sandiego.edu
