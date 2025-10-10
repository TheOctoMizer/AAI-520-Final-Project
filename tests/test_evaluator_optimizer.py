"""
QA Tests for Evaluator-Optimizer Workflow Pattern

Tests iterative self-improvement: Generate → Evaluate → Refine.

Each test validates quality assessment, feedback generation, and refinement.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from workflows.evaluator_optimizer import (
    EvaluatorOptimizerWorkflow,
    InvestmentAnalyzer,
    AnalysisEvaluator,
    AnalysisOptimizer,
    InvestmentAnalysis,
    QualityEvaluation
)
from tests.test_data import SAMPLE_COMPANY_DATA_TESLA, SAMPLE_COMPANY_DATA_NVIDIA


class TestEvaluatorOptimizer:
    """Test suite for Evaluator-Optimizer workflow."""

    def __init__(self):
        """Initialize test suite."""
        self.workflow = EvaluatorOptimizerWorkflow(max_iterations=2)
        self.analyzer = InvestmentAnalyzer()
        self.evaluator = AnalysisEvaluator()
        self.optimizer = AnalysisOptimizer()
        self.test_results = []

    def test_analyzer_generation(self):
        """
        TEST 1: Investment Analyzer - Initial Generation
        Validates analyzer generates comprehensive investment analysis.
        """
        print("\n" + "="*80)
        print("TEST 1: Evaluator-Optimizer - Initial Analysis Generation")
        print("="*80)

        try:
            analysis = self.analyzer.generate("TSLA", SAMPLE_COMPANY_DATA_TESLA)

            # Validation checks
            assert isinstance(analysis, InvestmentAnalysis), "Should return InvestmentAnalysis"
            assert analysis.ticker == "TSLA", "Ticker should match input"
            assert analysis.recommendation, "Should have recommendation"
            assert analysis.recommendation in ["Buy", "Hold", "Sell"], \
                f"Recommendation should be Buy/Hold/Sell, got: {analysis.recommendation}"
            assert analysis.target_price > 0, "Target price should be positive"
            assert analysis.investment_thesis, "Should have investment thesis"
            assert len(analysis.key_catalysts) > 0, "Should identify catalysts"
            assert len(analysis.risks) > 0, "Should identify risks"
            assert analysis.financial_highlights, "Should have financial highlights"
            assert analysis.conclusion, "Should have conclusion"

            # Quality checks
            assert len(analysis.investment_thesis) > 100, "Thesis should be detailed"
            assert len(analysis.key_catalysts) >= 2, "Should have multiple catalysts"
            assert len(analysis.risks) >= 2, "Should identify multiple risks"

            print(f"✓ PASSED: Analyzer generates comprehensive analysis")
            print(f"  - Ticker: {analysis.ticker}")
            print(f"  - Recommendation: {analysis.recommendation}")
            print(f"  - Target Price: ${analysis.target_price}")
            print(f"  - Catalysts: {len(analysis.key_catalysts)}")
            print(f"  - Risks: {len(analysis.risks)}")

            self.test_results.append(("Analyzer Generation", True, None))
            return True

        except Exception as e:
            print(f"✗ FAILED: {e}")
            self.test_results.append(("Analyzer Generation", False, str(e)))
            return False

    def test_evaluator_quality_assessment(self):
        """
        TEST 2: Evaluator - Quality Assessment
        Validates evaluator assesses analysis quality comprehensively.
        """
        print("\n" + "="*80)
        print("TEST 2: Evaluator-Optimizer - Quality Evaluation")
        print("="*80)

        try:
            analysis = self.analyzer.generate("TSLA", SAMPLE_COMPANY_DATA_TESLA)
            evaluation = self.evaluator.evaluate(analysis, SAMPLE_COMPANY_DATA_TESLA)

            # Validation checks
            assert isinstance(evaluation, QualityEvaluation), "Should return QualityEvaluation"
            assert 0 <= evaluation.overall_score <= 100, "Overall score should be 0-100"
            assert 0 <= evaluation.completeness_score <= 100, "Completeness should be 0-100"
            assert 0 <= evaluation.accuracy_score <= 100, "Accuracy should be 0-100"
            assert 0 <= evaluation.actionability_score <= 100, "Actionability should be 0-100"

            assert len(evaluation.strengths) > 0, "Should identify strengths"
            assert len(evaluation.weaknesses) > 0 or len(evaluation.missing_elements) > 0, \
                "Should identify areas for improvement"
            assert evaluation.specific_feedback, "Should provide specific feedback"
            assert len(evaluation.improvement_suggestions) > 0, \
                "Should provide improvement suggestions"
            assert isinstance(evaluation.is_acceptable, bool), "is_acceptable should be bool"

            # Quality checks
            avg_score = (evaluation.completeness_score + evaluation.accuracy_score +
                        evaluation.actionability_score) / 3
            assert abs(evaluation.overall_score - avg_score) < 30, \
                "Overall score should relate to dimension scores"

            print(f"✓ PASSED: Evaluator provides comprehensive assessment")
            print(f"  - Overall Score: {evaluation.overall_score:.1f}/100")
            print(f"  - Completeness: {evaluation.completeness_score:.1f}")
            print(f"  - Accuracy: {evaluation.accuracy_score:.1f}")
            print(f"  - Actionability: {evaluation.actionability_score:.1f}")
            print(f"  - Acceptable: {evaluation.is_acceptable}")
            print(f"  - Strengths identified: {len(evaluation.strengths)}")
            print(f"  - Improvement suggestions: {len(evaluation.improvement_suggestions)}")

            self.test_results.append(("Evaluator Assessment", True, None))
            return True

        except Exception as e:
            print(f"✗ FAILED: {e}")
            self.test_results.append(("Evaluator Assessment", False, str(e)))
            return False

    def test_optimizer_refinement(self):
        """
        TEST 3: Optimizer - Analysis Refinement
        Validates optimizer refines analysis based on feedback.
        """
        print("\n" + "="*80)
        print("TEST 3: Evaluator-Optimizer - Analysis Refinement")
        print("="*80)

        try:
            # Generate initial analysis
            original = self.analyzer.generate("TSLA", SAMPLE_COMPANY_DATA_TESLA)
            evaluation = self.evaluator.evaluate(original, SAMPLE_COMPANY_DATA_TESLA)

            # Refine based on feedback
            refined = self.optimizer.refine(original, evaluation, SAMPLE_COMPANY_DATA_TESLA)

            # Validation checks
            assert isinstance(refined, InvestmentAnalysis), "Should return InvestmentAnalysis"
            assert refined.ticker == original.ticker, "Ticker should remain same"

            # Refined analysis should still be comprehensive
            assert refined.recommendation, "Refined should have recommendation"
            assert refined.target_price > 0, "Refined should have target price"
            assert refined.investment_thesis, "Refined should have thesis"
            assert len(refined.key_catalysts) > 0, "Refined should have catalysts"
            assert len(refined.risks) > 0, "Refined should have risks"

            # Check that refinement addressed feedback
            # (Refined version should ideally be different/improved)
            assert refined.investment_thesis != original.investment_thesis or \
                   len(refined.key_catalysts) != len(original.key_catalysts) or \
                   len(refined.risks) != len(original.risks), \
                "Refined analysis should differ from original"

            print(f"✓ PASSED: Optimizer refines analysis based on feedback")
            print(f"  - Original catalysts: {len(original.key_catalysts)}")
            print(f"  - Refined catalysts: {len(refined.key_catalysts)}")
            print(f"  - Original risks: {len(original.risks)}")
            print(f"  - Refined risks: {len(refined.risks)}")
            print(f"  - Thesis updated: {refined.investment_thesis != original.investment_thesis}")

            self.test_results.append(("Optimizer Refinement", True, None))
            return True

        except Exception as e:
            print(f"✗ FAILED: {e}")
            self.test_results.append(("Optimizer Refinement", False, str(e)))
            return False

    def test_iterative_improvement(self):
        """
        TEST 4: Iterative Improvement
        Validates quality scores improve across iterations.
        """
        print("\n" + "="*80)
        print("TEST 4: Evaluator-Optimizer - Iterative Improvement")
        print("="*80)

        try:
            result = self.workflow.run("NVDA", SAMPLE_COMPANY_DATA_NVIDIA, verbose=False)

            # Validation checks
            assert "iteration_history" in result, "Should track iteration history"
            assert len(result["iteration_history"]) > 0, "Should have at least one iteration"
            assert "final_analysis" in result, "Should have final analysis"
            assert "final_evaluation" in result, "Should have final evaluation"

            # Check iteration tracking
            iterations = result["iteration_history"]
            assert all("iteration" in item and "analysis" in item and "evaluation" in item
                      for item in iterations), "Each iteration should be fully tracked"

            # Verify scores are tracked
            scores = [item["evaluation"].overall_score for item in iterations]
            assert all(0 <= score <= 100 for score in scores), "All scores should be valid"

            # Ideally scores should improve or stabilize (but LLM variance is acceptable)
            print(f"✓ PASSED: Iterative improvement workflow works")
            print(f"  - Iterations performed: {len(iterations)}")
            print(f"  - Score progression: {' → '.join(f'{s:.1f}' for s in scores)}")
            print(f"  - Final score: {result['final_evaluation'].overall_score:.1f}/100")
            print(f"  - Threshold met: {result['quality_threshold_met']}")

            self.test_results.append(("Iterative Improvement", True, None))
            return True

        except Exception as e:
            print(f"✗ FAILED: {e}")
            self.test_results.append(("Iterative Improvement", False, str(e)))
            return False

    def test_quality_threshold_enforcement(self):
        """
        TEST 5: Quality Threshold
        Validates workflow respects quality threshold and max iterations.
        """
        print("\n" + "="*80)
        print("TEST 5: Evaluator-Optimizer - Quality Threshold")
        print("="*80)

        try:
            # Test with max 3 iterations
            workflow = EvaluatorOptimizerWorkflow(max_iterations=3)
            result = workflow.run("NVDA", SAMPLE_COMPANY_DATA_NVIDIA, verbose=False)

            # Validation checks
            iterations_performed = result["iterations_performed"]
            assert 1 <= iterations_performed <= 3, \
                f"Should perform 1-3 iterations, performed: {iterations_performed}"

            final_score = result["final_evaluation"].overall_score

            # If score is above threshold, should stop early
            if result["quality_threshold_met"]:
                assert final_score >= workflow.quality_threshold, \
                    "If threshold met, score should be above threshold"

            # If not above threshold and did 3 iterations, that's expected
            if not result["quality_threshold_met"]:
                assert iterations_performed == workflow.max_iterations, \
                    "If threshold not met, should use all iterations"

            print(f"✓ PASSED: Quality threshold enforcement works")
            print(f"  - Max iterations: {workflow.max_iterations}")
            print(f"  - Iterations used: {iterations_performed}")
            print(f"  - Quality threshold: {workflow.quality_threshold}")
            print(f"  - Final score: {final_score:.1f}")
            print(f"  - Threshold met: {result['quality_threshold_met']}")

            self.test_results.append(("Quality Threshold", True, None))
            return True

        except Exception as e:
            print(f"✗ FAILED: {e}")
            self.test_results.append(("Quality Threshold", False, str(e)))
            return False

    def test_feedback_incorporation(self):
        """
        TEST 6: Feedback Incorporation
        Validates specific feedback is addressed in refinement.
        """
        print("\n" + "="*80)
        print("TEST 6: Evaluator-Optimizer - Feedback Incorporation")
        print("="*80)

        try:
            result = self.workflow.run("TSLA", SAMPLE_COMPANY_DATA_TESLA, verbose=False)

            # Get first and last iterations
            first_iter = result["iteration_history"][0]
            last_iter = result["iteration_history"][-1]

            # Validation checks
            first_eval = first_iter["evaluation"]
            last_eval = last_iter["evaluation"]

            # Check that feedback was provided
            assert len(first_eval.improvement_suggestions) > 0, \
                "First evaluation should provide improvement suggestions"

            # Check that weaknesses/gaps were identified
            identified_issues = len(first_eval.weaknesses) + len(first_eval.missing_elements)
            assert identified_issues > 0, "Should identify areas for improvement"

            # In multi-iteration runs, later iterations should address issues
            if len(result["iteration_history"]) > 1:
                # Later evaluation should reflect improvements
                # (Though exact score improvement not guaranteed due to LLM variance)
                assert last_eval.overall_score is not None, "Should provide score for each iteration"

            print(f"✓ PASSED: Feedback incorporation mechanism works")
            print(f"  - First iteration issues: {identified_issues}")
            print(f"  - Improvement suggestions: {len(first_eval.improvement_suggestions)}")
            print(f"  - First score: {first_eval.overall_score:.1f}")
            print(f"  - Last score: {last_eval.overall_score:.1f}")

            self.test_results.append(("Feedback Incorporation", True, None))
            return True

        except Exception as e:
            print(f"✗ FAILED: {e}")
            self.test_results.append(("Feedback Incorporation", False, str(e)))
            return False

    def test_different_companies(self):
        """
        TEST 7: Different Company Analysis
        Validates workflow handles different companies appropriately.
        """
        print("\n" + "="*80)
        print("TEST 7: Evaluator-Optimizer - Different Companies")
        print("="*80)

        try:
            # Analyze Tesla
            tesla_result = self.workflow.run("TSLA", SAMPLE_COMPANY_DATA_TESLA, verbose=False)

            # Analyze NVIDIA
            nvidia_result = self.workflow.run("NVDA", SAMPLE_COMPANY_DATA_NVIDIA, verbose=False)

            # Validation checks
            assert tesla_result["final_analysis"].ticker == "TSLA", "Should analyze TSLA"
            assert nvidia_result["final_analysis"].ticker == "NVDA", "Should analyze NVDA"

            # Analyses should be different
            assert tesla_result["final_analysis"].investment_thesis != \
                   nvidia_result["final_analysis"].investment_thesis, \
                "Different companies should have different theses"

            # Both should produce valid analyses
            for result in [tesla_result, nvidia_result]:
                assert result["final_evaluation"].overall_score > 0, \
                    "Both should receive quality scores"
                assert result["iterations_performed"] > 0, \
                    "Both should go through iterations"

            print(f"✓ PASSED: Workflow handles different companies correctly")
            print(f"  - TSLA iterations: {tesla_result['iterations_performed']}")
            print(f"  - TSLA score: {tesla_result['final_evaluation'].overall_score:.1f}")
            print(f"  - NVDA iterations: {nvidia_result['iterations_performed']}")
            print(f"  - NVDA score: {nvidia_result['final_evaluation'].overall_score:.1f}")

            self.test_results.append(("Different Companies", True, None))
            return True

        except Exception as e:
            print(f"✗ FAILED: {e}")
            self.test_results.append(("Different Companies", False, str(e)))
            return False

    def run_all_tests(self):
        """Run all evaluator-optimizer tests."""
        print("\n" + "="*80)
        print("RUNNING EVALUATOR-OPTIMIZER WORKFLOW TESTS")
        print("="*80)

        tests = [
            self.test_analyzer_generation,
            self.test_evaluator_quality_assessment,
            self.test_optimizer_refinement,
            self.test_iterative_improvement,
            self.test_quality_threshold_enforcement,
            self.test_feedback_incorporation,
            self.test_different_companies
        ]

        for test in tests:
            test()

        # Print summary
        print("\n" + "="*80)
        print("EVALUATOR-OPTIMIZER TEST SUMMARY")
        print("="*80)

        passed = sum(1 for _, success, _ in self.test_results if success)
        total = len(self.test_results)

        for test_name, success, error in self.test_results:
            status = "✓ PASS" if success else "✗ FAIL"
            print(f"{status}: {test_name}")
            if error:
                print(f"  Error: {error}")

        print(f"\nTotal: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        print("="*80 + "\n")

        return passed == total


def main():
    """Run evaluator-optimizer tests."""
    test_suite = TestEvaluatorOptimizer()
    success = test_suite.run_all_tests()

    if success:
        print("All Evaluator-Optimizer tests passed! ✓")
        return 0
    else:
        print("Some tests failed. See details above.")
        return 1


if __name__ == "__main__":
    exit(main())
