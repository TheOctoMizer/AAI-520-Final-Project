"""
Master Test Runner for AAI-520 Final Project

Runs all QA tests and generates a comprehensive report.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from tests.test_prompt_chaining import TestPromptChaining
from tests.test_routing import TestRouting
from tests.test_evaluator_optimizer import TestEvaluatorOptimizer
from tests.test_agent_functions import TestAgentFunctions


def print_header():
    """Print test suite header."""
    print("\n" + "="*100)
    print(" "*35 + "AAI-520 FINAL PROJECT")
    print(" "*25 + "AUTONOMOUS INVESTMENT RESEARCH AGENT")
    print(" "*35 + "COMPREHENSIVE QA TEST SUITE")
    print("="*100)


def print_section_header(title):
    """Print section header."""
    print("\n" + "="*100)
    print(f" {title}")
    print("="*100)


def run_all_tests():
    """Run all test suites and generate report."""
    print_header()

    all_results = {}

    # Test Suite 1: Prompt Chaining
    print_section_header("TEST SUITE 1: PROMPT CHAINING WORKFLOW PATTERN")
    print("Testing sequential pipeline: Ingest → Preprocess → Classify → Extract → Summarize")
    chaining_suite = TestPromptChaining()
    chaining_success = chaining_suite.run_all_tests()
    all_results["Prompt Chaining"] = (chaining_suite.test_results, chaining_success)

    # Test Suite 2: Routing
    print_section_header("TEST SUITE 2: ROUTING WORKFLOW PATTERN")
    print("Testing intelligent routing: Router → Specialist Agents (Earnings/News/Market)")
    routing_suite = TestRouting()
    routing_success = routing_suite.run_all_tests()
    all_results["Routing"] = (routing_suite.test_results, routing_success)

    # Test Suite 3: Evaluator-Optimizer
    print_section_header("TEST SUITE 3: EVALUATOR-OPTIMIZER WORKFLOW PATTERN")
    print("Testing iterative refinement: Generate → Evaluate → Refine")
    eo_suite = TestEvaluatorOptimizer()
    eo_success = eo_suite.run_all_tests()
    all_results["Evaluator-Optimizer"] = (eo_suite.test_results, eo_success)

    # Test Suite 4: Autonomous Agent Functions
    print_section_header("TEST SUITE 4: AUTONOMOUS AGENT FUNCTIONS")
    print("Testing agent capabilities: Plan, Tools, Reflect, Learn")
    agent_suite = TestAgentFunctions()
    agent_success = agent_suite.run_all_tests()
    all_results["Agent Functions"] = (agent_suite.test_results, agent_success)

    # Generate Final Report
    print_final_report(all_results)

    # Return overall success
    return all(success for _, success in all_results.values())


def print_final_report(all_results):
    """Print comprehensive final report."""
    print("\n" + "="*100)
    print(" "*40 + "FINAL TEST REPORT")
    print("="*100)

    total_passed = 0
    total_tests = 0

    print("\n" + "-"*100)
    print("PROJECT REQUIREMENTS VALIDATION")
    print("-"*100)

    # Workflow Patterns (33.8%)
    print("\n✓ WORKFLOW PATTERNS (33.8%)")
    print("  1. Prompt Chaining: Ingest → Preprocess → Classify → Extract → Summarize")
    chaining_results, chaining_success = all_results["Prompt Chaining"]
    print(f"     Status: {'✓ VALIDATED' if chaining_success else '✗ FAILED'}")
    print(f"     Tests: {sum(1 for _, s, _ in chaining_results if s)}/{len(chaining_results)} passed")

    print("\n  2. Routing: Content → Router → Specialist Analysts")
    routing_results, routing_success = all_results["Routing"]
    print(f"     Status: {'✓ VALIDATED' if routing_success else '✗ FAILED'}")
    print(f"     Tests: {sum(1 for _, s, _ in routing_results if s)}/{len(routing_results)} passed")

    print("\n  3. Evaluator-Optimizer: Generate → Evaluate → Refine")
    eo_results, eo_success = all_results["Evaluator-Optimizer"]
    print(f"     Status: {'✓ VALIDATED' if eo_success else '✗ FAILED'}")
    print(f"     Tests: {sum(1 for _, s, _ in eo_results if s)}/{len(eo_results)} passed")

    # Agent Functions (33.8%)
    print("\n✓ AGENT FUNCTIONS (33.8%)")
    agent_results, agent_success = all_results["Agent Functions"]

    print("  1. Plans Research Steps")
    plan_test = next((s for n, s, _ in agent_results if "Planning" in n), False)
    print(f"     Status: {'✓ VALIDATED' if plan_test else '✗ FAILED'}")

    print("  2. Uses Tools Dynamically")
    tools_test = next((s for n, s, _ in agent_results if "Dynamic Tool" in n), False)
    print(f"     Status: {'✓ VALIDATED' if tools_test else '✗ FAILED'}")

    print("  3. Self-Reflects on Quality")
    reflect_test = next((s for n, s, _ in agent_results if "Self-Reflection" in n), False)
    print(f"     Status: {'✓ VALIDATED' if reflect_test else '✗ FAILED'}")

    print("  4. Learns Across Runs")
    learn_test = next((s for n, s, _ in agent_results if "Learning" in n), False)
    print(f"     Status: {'✓ VALIDATED' if learn_test else '✗ FAILED'}")

    print(f"\n     Overall Agent Tests: {sum(1 for _, s, _ in agent_results if s)}/{len(agent_results)} passed")

    # Overall Statistics
    print("\n" + "-"*100)
    print("OVERALL TEST STATISTICS")
    print("-"*100)

    for suite_name, (results, success) in all_results.items():
        passed = sum(1 for _, s, _ in results if s)
        total = len(results)
        total_passed += passed
        total_tests += total

        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status} {suite_name:30s} {passed:2d}/{total:2d} tests ({passed/total*100:5.1f}%)")

    print("\n" + "-"*100)
    overall_pct = (total_passed / total_tests * 100) if total_tests > 0 else 0
    print(f"TOTAL: {total_passed}/{total_tests} tests passed ({overall_pct:.1f}%)")
    print("-"*100)

    # Final verdict
    print("\n" + "="*100)
    if all(success for _, success in all_results.values()):
        print(" "*25 + "✓ ALL REQUIREMENTS VALIDATED - PROJECT READY FOR SUBMISSION")
    else:
        print(" "*30 + "⚠ SOME TESTS FAILED - REVIEW REQUIRED")
    print("="*100 + "\n")


def main():
    """Main entry point."""
    try:
        success = run_all_tests()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user.")
        return 130
    except Exception as e:
        print(f"\n\nError running tests: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
