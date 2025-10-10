"""
QA Tests for Prompt Chaining Workflow Pattern

Tests the sequential pipeline: Ingest → Preprocess → Classify → Extract → Summarize

Each test validates a specific aspect of the workflow and agent functionality.
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from workflows.prompt_chaining import (
    PromptChainWorkflow,
    NewsArticle,
    PreprocessedNews,
    NewsClassification,
    ExtractedEntities,
    NewsSummary
)
from tests.test_data import SAMPLE_EARNINGS_NEWS, SAMPLE_MARKET_NEWS


class TestPromptChaining:
    """Test suite for Prompt Chaining workflow."""

    def __init__(self):
        """Initialize test suite."""
        self.workflow = PromptChainWorkflow()
        self.test_results = []

    def test_step1_ingest(self):
        """
        TEST 1: Ingest Step
        Validates that raw news text is properly ingested and structured.
        """
        print("\n" + "="*80)
        print("TEST 1: Prompt Chaining - Step 1 (Ingest)")
        print("="*80)

        try:
            article = self.workflow.step1_ingest(
                SAMPLE_EARNINGS_NEWS,
                source="Test Source"
            )

            # Validation checks
            assert isinstance(article, NewsArticle), "Output should be NewsArticle type"
            assert article.title, "Title should not be empty"
            assert article.content, "Content should not be empty"
            assert article.source == "Test Source", "Source should match input"
            assert len(article.content) > 50, "Content should be substantial"

            print(f"✓ PASSED: Ingest step works correctly")
            print(f"  - Title: {article.title[:50]}...")
            print(f"  - Content length: {len(article.content)} chars")
            print(f"  - Source: {article.source}")

            self.test_results.append(("Ingest", True, None))
            return True

        except Exception as e:
            print(f"✗ FAILED: {e}")
            self.test_results.append(("Ingest", False, str(e)))
            return False

    def test_step2_preprocess(self):
        """
        TEST 2: Preprocess Step
        Validates content cleaning and normalization.
        """
        print("\n" + "="*80)
        print("TEST 2: Prompt Chaining - Step 2 (Preprocess)")
        print("="*80)

        try:
            article = self.workflow.step1_ingest(SAMPLE_EARNINGS_NEWS, "Test")
            preprocessed = self.workflow.step2_preprocess(article)

            # Validation checks
            assert isinstance(preprocessed, PreprocessedNews), "Output should be PreprocessedNews"
            assert preprocessed.cleaned_content, "Cleaned content should exist"
            assert preprocessed.word_count > 0, "Word count should be positive"
            assert isinstance(preprocessed.contains_financials, bool), "contains_financials should be bool"
            assert preprocessed.word_count == len(preprocessed.cleaned_content.split()), \
                "Word count should match actual words"

            print(f"✓ PASSED: Preprocess step works correctly")
            print(f"  - Word count: {preprocessed.word_count}")
            print(f"  - Contains financials: {preprocessed.contains_financials}")
            print(f"  - Cleaned content length: {len(preprocessed.cleaned_content)} chars")

            self.test_results.append(("Preprocess", True, None))
            return True

        except Exception as e:
            print(f"✗ FAILED: {e}")
            self.test_results.append(("Preprocess", False, str(e)))
            return False

    def test_step3_classify(self):
        """
        TEST 3: Classify Step
        Validates news classification by category and sentiment.
        """
        print("\n" + "="*80)
        print("TEST 3: Prompt Chaining - Step 3 (Classify)")
        print("="*80)

        try:
            article = self.workflow.step1_ingest(SAMPLE_EARNINGS_NEWS, "Test")
            preprocessed = self.workflow.step2_preprocess(article)
            classification = self.workflow.step3_classify(preprocessed)

            # Validation checks
            assert isinstance(classification, NewsClassification), "Output should be NewsClassification"
            assert classification.category in [
                "earnings", "market_analysis", "policy", "merger_acquisition", "general"
            ], f"Category should be valid, got: {classification.category}"
            assert classification.sentiment in ["positive", "negative", "neutral"], \
                f"Sentiment should be valid, got: {classification.sentiment}"
            assert 0 <= classification.relevance_score <= 1, "Relevance score should be 0-1"
            assert 0 <= classification.confidence <= 1, "Confidence should be 0-1"

            # For earnings news, should classify as earnings
            assert classification.category == "earnings", \
                f"Should classify earnings news as 'earnings', got: {classification.category}"

            print(f"✓ PASSED: Classify step works correctly")
            print(f"  - Category: {classification.category}")
            print(f"  - Sentiment: {classification.sentiment}")
            print(f"  - Relevance: {classification.relevance_score:.2f}")
            print(f"  - Confidence: {classification.confidence:.2f}")

            self.test_results.append(("Classify", True, None))
            return True

        except Exception as e:
            print(f"✗ FAILED: {e}")
            self.test_results.append(("Classify", False, str(e)))
            return False

    def test_step4_extract(self):
        """
        TEST 4: Extract Step
        Validates entity and key fact extraction.
        """
        print("\n" + "="*80)
        print("TEST 4: Prompt Chaining - Step 4 (Extract)")
        print("="*80)

        try:
            article = self.workflow.step1_ingest(SAMPLE_EARNINGS_NEWS, "Test")
            preprocessed = self.workflow.step2_preprocess(article)
            entities = self.workflow.step4_extract(preprocessed)

            # Validation checks
            assert isinstance(entities, ExtractedEntities), "Output should be ExtractedEntities"
            assert isinstance(entities.companies, list), "Companies should be a list"
            assert isinstance(entities.people, list), "People should be a list"
            assert isinstance(entities.financial_metrics, list), "Metrics should be a list"
            assert isinstance(entities.key_events, list), "Events should be a list"
            assert isinstance(entities.stock_symbols, list), "Stock symbols should be a list"

            # For earnings news, should extract Apple/AAPL
            assert len(entities.companies) > 0, "Should extract at least one company"
            assert any("apple" in c.lower() for c in entities.companies), \
                "Should extract Apple from earnings news"

            print(f"✓ PASSED: Extract step works correctly")
            print(f"  - Companies: {entities.companies}")
            print(f"  - People: {entities.people}")
            print(f"  - Financial Metrics: {len(entities.financial_metrics)} metrics")
            print(f"  - Key Events: {len(entities.key_events)} events")
            print(f"  - Stock Symbols: {entities.stock_symbols}")

            self.test_results.append(("Extract", True, None))
            return True

        except Exception as e:
            print(f"✗ FAILED: {e}")
            self.test_results.append(("Extract", False, str(e)))
            return False

    def test_step5_summarize(self):
        """
        TEST 5: Summarize Step
        Validates final summary generation with investment implications.
        """
        print("\n" + "="*80)
        print("TEST 5: Prompt Chaining - Step 5 (Summarize)")
        print("="*80)

        try:
            article = self.workflow.step1_ingest(SAMPLE_EARNINGS_NEWS, "Test")
            preprocessed = self.workflow.step2_preprocess(article)
            classification = self.workflow.step3_classify(preprocessed)
            entities = self.workflow.step4_extract(preprocessed)
            summary = self.workflow.step5_summarize(preprocessed, classification, entities)

            # Validation checks
            assert isinstance(summary, NewsSummary), "Output should be NewsSummary"
            assert summary.executive_summary, "Executive summary should not be empty"
            assert len(summary.key_points) > 0, "Should have at least one key point"
            assert summary.investment_implications, "Investment implications should not be empty"
            assert summary.entities == entities, "Should include original entities"
            assert summary.classification == classification, "Should include original classification"

            # Quality checks
            assert len(summary.executive_summary) < 500, "Executive summary should be concise"
            assert len(summary.key_points) <= 10, "Key points should be focused"

            print(f"✓ PASSED: Summarize step works correctly")
            print(f"  - Executive Summary: {summary.executive_summary[:100]}...")
            print(f"  - Key Points: {len(summary.key_points)}")
            print(f"  - Investment Implications: {summary.investment_implications[:100]}...")

            self.test_results.append(("Summarize", True, None))
            return True

        except Exception as e:
            print(f"✗ FAILED: {e}")
            self.test_results.append(("Summarize", False, str(e)))
            return False

    def test_end_to_end_pipeline(self):
        """
        TEST 6: End-to-End Pipeline
        Validates the complete prompt chaining workflow.
        """
        print("\n" + "="*80)
        print("TEST 6: Prompt Chaining - End-to-End Pipeline")
        print("="*80)

        try:
            # Run complete workflow
            summary = self.workflow.run(SAMPLE_EARNINGS_NEWS, source="Test Source")

            # Validation checks
            assert isinstance(summary, NewsSummary), "Output should be NewsSummary"
            assert summary.executive_summary, "Should have executive summary"
            assert len(summary.key_points) > 0, "Should have key points"
            assert summary.investment_implications, "Should have investment implications"
            assert summary.entities, "Should have extracted entities"
            assert summary.classification, "Should have classification"

            # Validate the chaining worked (each step's output fed into next)
            assert summary.entities.companies, "Entities should include companies"
            assert summary.classification.category, "Classification should have category"

            print(f"✓ PASSED: End-to-end pipeline works correctly")
            print(f"  - All 5 steps executed successfully")
            print(f"  - Category: {summary.classification.category}")
            print(f"  - Sentiment: {summary.classification.sentiment}")
            print(f"  - Companies extracted: {len(summary.entities.companies)}")
            print(f"  - Key points generated: {len(summary.key_points)}")

            self.test_results.append(("End-to-End Pipeline", True, None))
            return True

        except Exception as e:
            print(f"✗ FAILED: {e}")
            self.test_results.append(("End-to-End Pipeline", False, str(e)))
            return False

    def test_different_content_types(self):
        """
        TEST 7: Different Content Types
        Validates workflow handles different news types correctly.
        """
        print("\n" + "="*80)
        print("TEST 7: Prompt Chaining - Different Content Types")
        print("="*80)

        try:
            # Test earnings news
            earnings_summary = self.workflow.run(SAMPLE_EARNINGS_NEWS, "Test")
            assert earnings_summary.classification.category == "earnings", \
                "Should classify earnings news correctly"

            # Test market news
            market_summary = self.workflow.run(SAMPLE_MARKET_NEWS, "Test")
            assert market_summary.classification.category == "market_analysis", \
                "Should classify market news correctly"

            # Both should have different characteristics
            assert earnings_summary.entities.companies != market_summary.entities.companies or \
                   len(earnings_summary.entities.companies) != len(market_summary.entities.companies), \
                "Different news types should extract different entities"

            print(f"✓ PASSED: Workflow handles different content types")
            print(f"  - Earnings news → {earnings_summary.classification.category}")
            print(f"  - Market news → {market_summary.classification.category}")

            self.test_results.append(("Different Content Types", True, None))
            return True

        except Exception as e:
            print(f"✗ FAILED: {e}")
            self.test_results.append(("Different Content Types", False, str(e)))
            return False

    def run_all_tests(self):
        """Run all prompt chaining tests."""
        print("\n" + "="*80)
        print("RUNNING PROMPT CHAINING WORKFLOW TESTS")
        print("="*80)

        tests = [
            self.test_step1_ingest,
            self.test_step2_preprocess,
            self.test_step3_classify,
            self.test_step4_extract,
            self.test_step5_summarize,
            self.test_end_to_end_pipeline,
            self.test_different_content_types
        ]

        for test in tests:
            test()

        # Print summary
        print("\n" + "="*80)
        print("PROMPT CHAINING TEST SUMMARY")
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
    """Run prompt chaining tests."""
    test_suite = TestPromptChaining()
    success = test_suite.run_all_tests()

    if success:
        print("All Prompt Chaining tests passed! ✓")
        return 0
    else:
        print("Some tests failed. See details above.")
        return 1


if __name__ == "__main__":
    exit(main())
