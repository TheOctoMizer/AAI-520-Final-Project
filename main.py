"""
AAI-520 Final Project: Autonomous Investment Research Agent
Main entry point for the application
"""
import sys
from agents.research_agent import AutonomousResearchAgent


def print_banner():
    """Print application banner."""
    print("\n" + "="*80)
    print(" AAI-520 FINAL PROJECT")
    print(" Autonomous Investment Research Agent")
    print(" Powered by Agentic AI with Multi-Workflow Patterns")
    print("="*80 + "\n")


def print_menu():
    """Print main menu options."""
    print("\nChoose an option:")
    print("  1. Run Autonomous Research Agent (Full System)")
    print("  2. Demo: Prompt Chaining Workflow")
    print("  3. Demo: Routing Workflow")
    print("  4. Demo: Evaluator-Optimizer Workflow")
    print("  5. Demo: All Three Workflows")
    print("  6. Demo: Knowledge Graph Builder")
    print("  0. Exit")
    print()


def run_autonomous_agent():
    """Run the full autonomous research agent."""
    print("\n" + "="*80)
    print(" AUTONOMOUS RESEARCH AGENT")
    print("="*80)

    ticker = input("\nEnter stock ticker (e.g., AAPL, MSFT, TSLA): ").strip().upper()
    if not ticker:
        print("Invalid ticker. Aborting.")
        return

    context = input("Enter research context (or press Enter for default): ").strip()
    if not context:
        context = "General investment analysis"

    print(f"\nResearching {ticker}...")
    print("This will take a few minutes as the agent plans, researches, and reflects.\n")

    agent = AutonomousResearchAgent()
    result = agent.research_stock(ticker, context)

    # Display results
    print("\n" + "="*80)
    print(" RESEARCH SUMMARY")
    print("="*80)

    print(f"\nTicker: {result.ticker}")
    print(f"Execution Time: {result.execution_time_seconds:.1f} seconds")

    print(f"\n--- Research Plan ---")
    for i, step in enumerate(result.plan.research_steps, 1):
        print(f"  {i}. {step}")

    print(f"\nEstimated Complexity: {result.plan.estimated_complexity}")
    print(f"Data Sources Used: {', '.join(result.plan.data_sources_needed)}")

    if result.investment_analysis:
        print(f"\n--- Investment Analysis ---")
        print(f"Recommendation: {result.investment_analysis['recommendation']}")
        print(f"Target Price: ${result.investment_analysis['target_price']}")
        print(f"Quality Score: {result.investment_analysis['quality_score']:.1f}/100")
        print(f"Refinement Iterations: {result.investment_analysis['iterations']}")

    if result.news_analysis:
        print(f"\n--- News Analysis ---")
        print(f"Summary: {result.news_analysis['summary']}")
        print(f"Sentiment: {result.news_analysis['sentiment']}")
        print(f"Category: {result.news_analysis['category']}")

    print(f"\n--- Self-Reflection ---")
    print(f"Completeness: {result.reflection.completeness_score:.1f}/100")
    print(f"Confidence: {result.reflection.confidence_score:.1f}/100")
    print(f"Data Quality: {result.reflection.data_quality_score:.1f}/100")

    if result.reflection.gaps:
        print(f"\nIdentified Gaps:")
        for gap in result.reflection.gaps[:3]:
            print(f"  • {gap}")

    if result.reflection.improvement_recommendations:
        print(f"\nImprovement Recommendations:")
        for rec in result.reflection.improvement_recommendations[:3]:
            print(f"  • {rec}")

    print(f"\nOverall Assessment: {result.reflection.overall_assessment}")
    print("\n" + "="*80 + "\n")


def demo_prompt_chaining():
    """Demo the prompt chaining workflow."""
    from workflows.prompt_chaining import demonstrate_prompt_chaining

    print("\n" + "="*80)
    print(" WORKFLOW PATTERN 1: PROMPT CHAINING")
    print(" Pipeline: Ingest → Preprocess → Classify → Extract → Summarize")
    print("="*80 + "\n")

    demonstrate_prompt_chaining()


def demo_routing():
    """Demo the routing workflow."""
    from workflows.routing import demonstrate_routing

    print("\n" + "="*80)
    print(" WORKFLOW PATTERN 2: ROUTING")
    print(" Router → Specialist Agents (Earnings/News/Market)")
    print("="*80 + "\n")

    demonstrate_routing()


def demo_evaluator_optimizer():
    """Demo the evaluator-optimizer workflow."""
    from workflows.evaluator_optimizer import demonstrate_evaluator_optimizer

    print("\n" + "="*80)
    print(" WORKFLOW PATTERN 3: EVALUATOR-OPTIMIZER")
    print(" Generate → Evaluate → Refine (Iterative Self-Improvement)")
    print("="*80 + "\n")

    demonstrate_evaluator_optimizer()


def demo_all_workflows():
    """Demo all three workflow patterns."""
    from workflows.demo_all_workflows import demo_all_workflows

    demo_all_workflows()


def demo_knowledge_graph():
    """Demo the knowledge graph builder."""
    from utils.knowledge_graph import KnowledgeGraphBuilder

    print("\n" + "="*80)
    print(" KNOWLEDGE GRAPH BUILDER")
    print("="*80)

    ticker = input("\nEnter stock ticker to build graph from (e.g., AAPL): ").strip().upper()
    if not ticker:
        print("Invalid ticker. Using MSFT as default.")
        ticker = "MSFT"

    depth = input("Enter expansion depth (1-3, default 2): ").strip()
    try:
        depth = int(depth)
        if depth < 1 or depth > 3:
            depth = 2
    except ValueError:
        depth = 2

    print(f"\nBuilding knowledge graph for {ticker} (depth={depth})...")

    builder = KnowledgeGraphBuilder()
    graph = builder.expand_from_seed(ticker, depth=depth)

    print("\n" + builder.get_graph_summary())
    print("\n" + "="*80 + "\n")


def main():
    """Main application entry point."""
    print_banner()

    while True:
        print_menu()
        choice = input("Enter your choice (0-6): ").strip()

        if choice == "1":
            run_autonomous_agent()
        elif choice == "2":
            demo_prompt_chaining()
        elif choice == "3":
            demo_routing()
        elif choice == "4":
            demo_evaluator_optimizer()
        elif choice == "5":
            demo_all_workflows()
        elif choice == "6":
            demo_knowledge_graph()
        elif choice == "0":
            print("\nThank you for using the Autonomous Investment Research Agent!")
            print("="*80 + "\n")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please enter a number between 0 and 6.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
