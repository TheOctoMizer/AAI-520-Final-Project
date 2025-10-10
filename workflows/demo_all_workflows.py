"""
Comprehensive demonstration of all three workflow patterns.

This script demonstrates:
1. Prompt Chaining: News → Preprocess → Classify → Extract → Summarize
2. Routing: Content → Router → Specialist Analysis
3. Evaluator-Optimizer: Generate → Evaluate → Refine → Re-evaluate
"""
from workflows.prompt_chaining import PromptChainWorkflow
from workflows.routing import RoutingWorkflow
from workflows.evaluator_optimizer import EvaluatorOptimizerWorkflow


def demo_all_workflows():
    """Run demonstrations of all three workflow patterns."""

    print("\n" + "="*80)
    print(" AGENTIC AI WORKFLOW PATTERNS DEMONSTRATION")
    print(" AAI-520 Final Project - Autonomous Investment Research Agent")
    print("="*80)

    # =========================================================================
    # WORKFLOW 1: PROMPT CHAINING
    # =========================================================================
    print("\n\n" + "="*80)
    print(" WORKFLOW PATTERN 1: PROMPT CHAINING")
    print(" Pipeline: Ingest → Preprocess → Classify → Extract → Summarize")
    print("="*80)

    sample_news = """
    NVIDIA Q4 2024 Earnings Exceed Expectations on AI Chip Demand

    NVIDIA Corporation (NVDA) reported fiscal Q4 2024 results that significantly beat
    Wall Street expectations, driven by unprecedented demand for its AI accelerator chips.
    Revenue soared to $22.1 billion, up 265% year-over-year, crushing analyst estimates
    of $20.4 billion.

    CEO Jensen Huang highlighted explosive growth in the data center segment, which
    generated $18.4 billion in revenue, up 409% YoY. "We are witnessing a fundamental
    shift in computing," Huang stated. "Generative AI and accelerated computing are
    transforming every industry."

    Earnings per share came in at $5.16, well above the consensus of $4.64. The company
    announced a 10-for-1 stock split and increased its quarterly dividend by 150% to
    $0.04 per share (post-split).

    NVIDIA also unveiled its next-generation Blackwell GPU architecture, promising 2.5x
    performance improvement over current H100 chips. Major cloud providers including
    Microsoft, Amazon, and Google have already committed to Blackwell orders.

    Gross margins expanded to 76.0% from 63.3% in the prior year, reflecting strong
    pricing power. Looking ahead, NVIDIA guided Q1 2025 revenue to $24 billion, well
    above Street estimates of $22.1 billion.

    Shares surged 8% in after-hours trading, pushing market cap above $2 trillion.
    """

    chaining_workflow = PromptChainWorkflow()
    chaining_result = chaining_workflow.run(sample_news, source="Company Press Release")

    print("\n--- PROMPT CHAINING RESULTS ---")
    print(f"Executive Summary: {chaining_result.executive_summary}")
    print(f"\nClassification: {chaining_result.classification.category} "
          f"({chaining_result.classification.sentiment})")
    print(f"Companies Extracted: {', '.join(chaining_result.entities.companies)}")

    # =========================================================================
    # WORKFLOW 2: ROUTING
    # =========================================================================
    print("\n\n" + "="*80)
    print(" WORKFLOW PATTERN 2: ROUTING")
    print(" Router → Specialist Agents (Earnings/News/Market)")
    print("="*80)

    routing_workflow = RoutingWorkflow()

    test_content = [
        {
            "title": "AMD Reports Strong Data Center Growth",
            "content": """
            AMD reported Q3 earnings with revenue of $5.8B, up 18% YoY. Data center
            revenue jumped 80% to $1.6B driven by EPYC processor adoption. Gaming
            revenue declined 8% to $1.5B. EPS of $0.70 beat estimates of $0.68.
            CEO Lisa Su noted strong traction in AI inference workloads.
            """
        },
        {
            "title": "S&P 500 Technical Analysis Shows Bullish Setup",
            "content": """
            The S&P 500 index broke above resistance at 4,600, showing strong bullish
            momentum. RSI at 62 indicates room to run. Volume on the breakout was
            above 20-day average, confirming the move. Next resistance at 4,750.
            Breadth indicators positive with 75% of stocks above 50-day MA.
            """
        }
    ]

    routing_results = routing_workflow.batch_process(test_content)

    print("\n--- ROUTING RESULTS ---")
    for i, result in enumerate(routing_results):
        print(f"\nContent {i+1}: {test_content[i]['title']}")
        print(f"  Routed to: {result['routing_decision'].route}")
        print(f"  Confidence: {result['routing_decision'].confidence:.2f}")

    # =========================================================================
    # WORKFLOW 3: EVALUATOR-OPTIMIZER
    # =========================================================================
    print("\n\n" + "="*80)
    print(" WORKFLOW PATTERN 3: EVALUATOR-OPTIMIZER")
    print(" Generate → Evaluate → Refine (Iterative Self-Improvement)")
    print("="*80)

    company_data = """
    Amazon.com Inc. (AMZN)

    Q4 2024 Results:
    - Revenue: $170.0B (+14% YoY)
    - AWS Revenue: $24.2B (+13% YoY)
    - Operating Income: $13.2B
    - EPS: $1.00 (beat $0.80 estimate)
    - Free Cash Flow: $36.8B (trailing 12 months)

    Key Metrics:
    - Amazon Prime members: 200M+ globally
    - AWS operating margin: 30%
    - Advertising revenue: $14.7B (+27% YoY)
    - International revenue growth: 11%

    Recent Developments:
    - Expanding AWS AI services (Bedrock, Q)
    - Same-day delivery expanding to 100+ metros
    - Healthcare initiatives with One Medical
    - Cost-cutting program saved $10B annually

    Market Position:
    - Current Price: $178
    - P/E Ratio: 52
    - Cloud market share: 32% (leader)
    - E-commerce market share: 38% in US
    """

    eo_workflow = EvaluatorOptimizerWorkflow(max_iterations=2)
    eo_result = eo_workflow.run("AMZN", company_data, verbose=True)

    print("\n--- EVALUATOR-OPTIMIZER RESULTS ---")
    print(f"Final Recommendation: {eo_result['final_analysis'].recommendation}")
    print(f"Target Price: ${eo_result['final_analysis'].target_price}")
    print(f"Quality Score: {eo_result['final_evaluation'].overall_score:.1f}/100")
    print(f"Iterations Performed: {eo_result['iterations_performed']}")
    print(f"Threshold Met: {eo_result['quality_threshold_met']}")

    print("\nScore Progression:")
    for item in eo_result["iteration_history"]:
        score = item["evaluation"].overall_score
        print(f"  Iteration {item['iteration']}: {score:.1f}/100")

    # =========================================================================
    # SUMMARY
    # =========================================================================
    print("\n\n" + "="*80)
    print(" DEMONSTRATION COMPLETE")
    print("="*80)
    print("\nAll three workflow patterns successfully demonstrated:")
    print("  ✓ Prompt Chaining - Sequential processing pipeline")
    print("  ✓ Routing - Intelligent task distribution to specialists")
    print("  ✓ Evaluator-Optimizer - Iterative self-improvement")
    print("\nThese patterns form the foundation of agentic AI systems.")
    print("="*80 + "\n")

    return {
        "chaining_result": chaining_result,
        "routing_results": routing_results,
        "evaluator_optimizer_result": eo_result
    }


if __name__ == "__main__":
    results = demo_all_workflows()
