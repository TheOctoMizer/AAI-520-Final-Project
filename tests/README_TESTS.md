# Testing Guide - AAI-520 Final Project

Comprehensive QA testing framework for the Autonomous Investment Research Agent.

## Overview

This testing suite validates all project requirements:

### Workflow Patterns (33.8%)
- ✅ **Prompt Chaining**: Sequential news processing pipeline
- ✅ **Routing**: Intelligent content distribution to specialists
- ✅ **Evaluator-Optimizer**: Iterative self-improvement

### Agent Functions (33.8%)
- ✅ **Plans Research Steps**: Autonomous task decomposition
- ✅ **Uses Tools Dynamically**: Context-aware tool selection
- ✅ **Self-Reflects on Quality**: Critical self-assessment
- ✅ **Learns Across Runs**: Cross-run memory and improvement

## Test Files

### `test_prompt_chaining.py`
**Tests:** 7 tests covering the prompt chaining workflow

- `test_step1_ingest`: Validates raw news ingestion
- `test_step2_preprocess`: Validates content cleaning
- `test_step3_classify`: Validates news classification
- `test_step4_extract`: Validates entity extraction
- `test_step5_summarize`: Validates summary generation
- `test_end_to_end_pipeline`: Validates complete pipeline
- `test_different_content_types`: Validates handling different news types

**Run individually:**
```bash
python tests/test_prompt_chaining.py
```

### `test_routing.py`
**Tests:** 8 tests covering the routing workflow

- `test_router_earnings_content`: Validates earnings routing
- `test_router_market_content`: Validates market routing
- `test_router_news_content`: Validates news routing
- `test_earnings_analyst_quality`: Validates earnings analyst output
- `test_news_analyst_quality`: Validates news analyst output
- `test_market_analyst_quality`: Validates market analyst output
- `test_end_to_end_routing`: Validates complete routing workflow
- `test_batch_routing`: Validates batch processing

**Run individually:**
```bash
python tests/test_routing.py
```

### `test_evaluator_optimizer.py`
**Tests:** 7 tests covering the evaluator-optimizer workflow

- `test_analyzer_generation`: Validates initial analysis generation
- `test_evaluator_quality_assessment`: Validates quality evaluation
- `test_optimizer_refinement`: Validates analysis refinement
- `test_iterative_improvement`: Validates iterative improvement
- `test_quality_threshold_enforcement`: Validates threshold logic
- `test_feedback_incorporation`: Validates feedback addressing
- `test_different_companies`: Validates handling different companies

**Run individually:**
```bash
python tests/test_evaluator_optimizer.py
```

### `test_agent_functions.py`
**Tests:** 6 tests covering autonomous agent capabilities

- `test_agent_function1_planning`: Validates autonomous planning
- `test_agent_function2_dynamic_tools`: Validates dynamic tool selection
- `test_agent_function3_self_reflection`: Validates self-reflection
- `test_agent_function4_learning`: Validates cross-run learning
- `test_end_to_end_agent`: Validates complete agent workflow
- `test_agent_workflow_integration`: Validates workflow integration

**Run individually:**
```bash
python tests/test_agent_functions.py
```

### `run_all_tests.py`
**Master test runner** that executes all test suites and generates comprehensive report.

**Run all tests:**
```bash
python tests/run_all_tests.py
```

## Test Data

### `test_data.py`
Contains sample data for testing:

- `SAMPLE_EARNINGS_NEWS`: Apple earnings report
- `SAMPLE_MARKET_NEWS`: S&P 500 market update
- `SAMPLE_POLICY_NEWS`: Fed rate policy announcement
- `SAMPLE_COMPANY_DATA_TESLA`: Tesla financial data
- `SAMPLE_COMPANY_DATA_NVIDIA`: NVIDIA financial data

## Running Tests

### Quick Start

Run all tests with comprehensive reporting:
```bash
python tests/run_all_tests.py
```

### Individual Test Suites

Run specific test suite:
```bash
# Prompt Chaining tests
python tests/test_prompt_chaining.py

# Routing tests
python tests/test_routing.py

# Evaluator-Optimizer tests
python tests/test_evaluator_optimizer.py

# Agent Functions tests
python tests/test_agent_functions.py
```

### From Python

```python
from tests.test_prompt_chaining import TestPromptChaining

suite = TestPromptChaining()
success = suite.run_all_tests()
```

## Test Output

Each test produces detailed output:

```
================================================================================
TEST 1: Prompt Chaining - Step 1 (Ingest)
================================================================================
✓ PASSED: Ingest step works correctly
  - Title: Apple Reports Record Q4 2024 Earnings...
  - Content length: 645 chars
  - Source: Test Source
```

Final summary shows pass/fail for each requirement:

```
================================================================================
FINAL TEST REPORT
================================================================================

✓ WORKFLOW PATTERNS (33.8%)
  1. Prompt Chaining: Ingest → Preprocess → Classify → Extract → Summarize
     Status: ✓ VALIDATED
     Tests: 7/7 passed

  2. Routing: Content → Router → Specialist Analysts
     Status: ✓ VALIDATED
     Tests: 8/8 passed

  3. Evaluator-Optimizer: Generate → Evaluate → Refine
     Status: ✓ VALIDATED
     Tests: 7/7 passed

✓ AGENT FUNCTIONS (33.8%)
  1. Plans Research Steps
     Status: ✓ VALIDATED

  2. Uses Tools Dynamically
     Status: ✓ VALIDATED

  3. Self-Reflects on Quality
     Status: ✓ VALIDATED

  4. Learns Across Runs
     Status: ✓ VALIDATED

TOTAL: 28/28 tests passed (100.0%)
```

## Test Requirements

### Prerequisites
- Python 3.12+
- All project dependencies installed (`uv sync` or `pip install -e .`)
- LM Studio running locally (or OpenAI API configured)
- Environment variables set (ALPHA_VANTAGE_KEY)

### Note on API Tests
Some tests require API access and may:
- Take longer to run (LLM calls)
- Require valid API credentials
- Depend on external service availability

Tests are designed to be resilient and provide informative error messages.

## Validation Criteria

### Prompt Chaining Tests
- ✅ Each step produces correct output type
- ✅ Data flows sequentially through pipeline
- ✅ Classification accuracy for different content
- ✅ Entity extraction completeness
- ✅ Summary quality and conciseness

### Routing Tests
- ✅ Router correctly identifies content type
- ✅ High confidence in routing decisions
- ✅ Each specialist produces appropriate analysis
- ✅ Analysis quality meets standards
- ✅ Batch processing works correctly

### Evaluator-Optimizer Tests
- ✅ Initial analysis is comprehensive
- ✅ Evaluation scores are accurate
- ✅ Specific feedback is provided
- ✅ Refinement addresses feedback
- ✅ Quality improves across iterations
- ✅ Threshold logic works correctly

### Agent Function Tests
- ✅ Plans include detailed steps
- ✅ Tools are selected based on plan
- ✅ Multiple tools used dynamically
- ✅ Self-reflection is critical and honest
- ✅ Learnings persist across runs
- ✅ All workflows integrate correctly

## Troubleshooting

### Common Issues

**Import Errors:**
```bash
# Ensure you're running from project root
cd /path/to/AAI-520-Final-Project
python tests/run_all_tests.py
```

**API Errors:**
```bash
# Check environment variables
echo $ALPHA_VANTAGE_KEY

# Check LM Studio is running
curl http://localhost:1234/v1/models
```

**Timeout Errors:**
- Some tests may take 2-5 minutes due to LLM processing
- Increase timeout in test configuration if needed

**LLM Variance:**
- LLM outputs may vary between runs
- Tests use flexible validation (ranges, presence checks)
- Core functionality is tested, not exact outputs

## Test Coverage

Total test coverage:
- **28 individual tests** across 4 test suites
- **3 workflow patterns** fully tested
- **4 agent functions** fully validated
- **All project requirements** covered

## Contributing

When adding new features:

1. Add test data to `test_data.py` if needed
2. Create focused unit tests for new components
3. Update integration tests in `test_agent_functions.py`
4. Run full test suite to ensure no regressions
5. Update this README if adding new test files

## Continuous Validation

Recommended testing workflow:

1. **During Development**: Run relevant individual test file
2. **Before Commit**: Run `python tests/run_all_tests.py`
3. **Before Submission**: Full test run with report review

## Exit Codes

- `0`: All tests passed
- `1`: Some tests failed
- `130`: Tests interrupted by user

## Performance

Expected test execution time:
- Individual test suite: 2-5 minutes
- Full test suite: 10-20 minutes (depends on LLM speed)

## Contact

For questions about testing:
- Review test output for specific failure details
- Check test code for validation logic
- Ensure environment is properly configured
