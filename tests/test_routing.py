"""
QA Tests for Routing Workflow Pattern

Tests intelligent content routing to specialist agents (Earnings/News/Market).

Each test validates routing decisions and specialist analysis quality.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from workflows.routing import (
    RoutingWorkflow,
    ContentRouter,
    EarningsAnalyst,
    NewsAnalyst,
    MarketAnalyst,
    RoutingDecision,
    EarningsAnalysis,
    NewsAnalysis,
    MarketAnalysis
)
from tests.test_data import (
    SAMPLE_EARNINGS_NEWS,
    SAMPLE_MARKET_NEWS,
    SAMPLE_POLICY_NEWS
)


class TestRouting:
    """Test suite for Routing workflow."""

    def __init__(self):
        """Initialize test suite."""
        self.workflow = RoutingWorkflow()
        self.router = ContentRouter()
        self.test_results = []

    def test_router_earnings_content(self):
        """
        TEST 1: Router - Earnings Content
        Validates router correctly identifies earnings-related content.
        """
        print("\n" + "="*80)
        print("TEST 1: Routing - Earnings Content Recognition")
        print("="*80)

        try:
            decision = self.router.route(
                SAMPLE_EARNINGS_NEWS,
                title="Apple Reports Q4 Earnings"
            )

            # Validation checks
            assert isinstance(decision, RoutingDecision), "Should return RoutingDecision"
            assert decision.route == "earnings", \
                f"Should route earnings content to earnings analyst, got: {decision.route}"
            assert 0 <= decision.confidence <= 1, "Confidence should be 0-1"
            assert decision.reasoning, "Should provide reasoning"
            assert decision.confidence >= 0.7, \
                f"Should be highly confident for clear earnings content, got: {decision.confidence}"

            print(f"✓ PASSED: Router correctly identifies earnings content")
            print(f"  - Route: {decision.route}")
            print(f"  - Confidence: {decision.confidence:.2f}")
            print(f"  - Reasoning: {decision.reasoning[:100]}...")

            self.test_results.append(("Router - Earnings", True, None))
            return True

        except Exception as e:
            print(f"✗ FAILED: {e}")
            self.test_results.append(("Router - Earnings", False, str(e)))
            return False

    def test_router_market_content(self):
        """
        TEST 2: Router - Market Content
        Validates router correctly identifies market analysis content.
        """
        print("\n" + "="*80)
        print("TEST 2: Routing - Market Content Recognition")
        print("="*80)

        try:
            decision = self.router.route(
                SAMPLE_MARKET_NEWS,
                title="S&P 500 Reaches New High"
            )

            # Validation checks
            assert isinstance(decision, RoutingDecision), "Should return RoutingDecision"
            assert decision.route == "market", \
                f"Should route market content to market analyst, got: {decision.route}"
            assert decision.confidence >= 0.6, "Should be confident in routing decision"

            print(f"✓ PASSED: Router correctly identifies market content")
            print(f"  - Route: {decision.route}")
            print(f"  - Confidence: {decision.confidence:.2f}")
            print(f"  - Reasoning: {decision.reasoning[:100]}...")

            self.test_results.append(("Router - Market", True, None))
            return True

        except Exception as e:
            print(f"✗ FAILED: {e}")
            self.test_results.append(("Router - Market", False, str(e)))
            return False

    def test_router_news_content(self):
        """
        TEST 3: Router - News/Policy Content
        Validates router correctly identifies news/policy content.
        """
        print("\n" + "="*80)
        print("TEST 3: Routing - News/Policy Content Recognition")
        print("="*80)

        try:
            decision = self.router.route(
                SAMPLE_POLICY_NEWS,
                title="Fed Signals Rate Cuts"
            )

            # Validation checks
            assert isinstance(decision, RoutingDecision), "Should return RoutingDecision"
            assert decision.route == "news", \
                f"Should route policy news to news analyst, got: {decision.route}"
            assert decision.confidence >= 0.6, "Should be confident in routing decision"

            print(f"✓ PASSED: Router correctly identifies news content")
            print(f"  - Route: {decision.route}")
            print(f"  - Confidence: {decision.confidence:.2f}")
            print(f"  - Reasoning: {decision.reasoning[:100]}...")

            self.test_results.append(("Router - News", True, None))
            return True

        except Exception as e:
            print(f"✗ FAILED: {e}")
            self.test_results.append(("Router - News", False, str(e)))
            return False

    def test_earnings_analyst_quality(self):
        """
        TEST 4: Earnings Analyst Output Quality
        Validates earnings analyst produces comprehensive analysis.
        """
        print("\n" + "="*80)
        print("TEST 4: Earnings Analyst - Analysis Quality")
        print("="*80)

        try:
            analyst = EarningsAnalyst()
            analysis = analyst.analyze(SAMPLE_EARNINGS_NEWS)

            # Validation checks
            assert isinstance(analysis, EarningsAnalysis), "Should return EarningsAnalysis"
            assert analysis.revenue_analysis, "Should have revenue analysis"
            assert analysis.profitability_analysis, "Should have profitability analysis"
            assert analysis.growth_trends, "Should have growth trends"
            assert analysis.guidance_assessment, "Should have guidance assessment"
            assert len(analysis.key_metrics) > 0, "Should extract key metrics"
            assert analysis.recommendation, "Should provide recommendation"

            # Quality checks
            assert len(analysis.revenue_analysis) > 50, "Revenue analysis should be detailed"
            assert len(analysis.key_metrics) >= 2, "Should identify multiple key metrics"

            print(f"✓ PASSED: Earnings analyst produces quality analysis")
            print(f"  - Revenue analysis: {len(analysis.revenue_analysis)} chars")
            print(f"  - Key metrics: {len(analysis.key_metrics)}")
            print(f"  - Recommendation: {analysis.recommendation[:80]}...")

            self.test_results.append(("Earnings Analyst Quality", True, None))
            return True

        except Exception as e:
            print(f"✗ FAILED: {e}")
            self.test_results.append(("Earnings Analyst Quality", False, str(e)))
            return False

    def test_news_analyst_quality(self):
        """
        TEST 5: News Analyst Output Quality
        Validates news analyst produces comprehensive analysis.
        """
        print("\n" + "="*80)
        print("TEST 5: News Analyst - Analysis Quality")
        print("="*80)

        try:
            analyst = NewsAnalyst()
            analysis = analyst.analyze(SAMPLE_POLICY_NEWS)

            # Validation checks
            assert isinstance(analysis, NewsAnalysis), "Should return NewsAnalysis"
            assert analysis.event_summary, "Should have event summary"
            assert analysis.market_impact, "Should analyze market impact"
            assert analysis.stakeholder_analysis, "Should analyze stakeholders"
            assert analysis.timeline, "Should provide timeline"
            assert 0 <= analysis.credibility_score <= 1, "Credibility should be 0-1"
            assert len(analysis.actionable_insights) > 0, "Should provide insights"

            # Quality checks
            assert len(analysis.event_summary) > 50, "Event summary should be detailed"
            assert len(analysis.actionable_insights) >= 1, "Should have actionable insights"

            print(f"✓ PASSED: News analyst produces quality analysis")
            print(f"  - Event summary: {len(analysis.event_summary)} chars")
            print(f"  - Credibility score: {analysis.credibility_score:.2f}")
            print(f"  - Actionable insights: {len(analysis.actionable_insights)}")

            self.test_results.append(("News Analyst Quality", True, None))
            return True

        except Exception as e:
            print(f"✗ FAILED: {e}")
            self.test_results.append(("News Analyst Quality", False, str(e)))
            return False

    def test_market_analyst_quality(self):
        """
        TEST 6: Market Analyst Output Quality
        Validates market analyst produces comprehensive analysis.
        """
        print("\n" + "="*80)
        print("TEST 6: Market Analyst - Analysis Quality")
        print("="*80)

        try:
            analyst = MarketAnalyst()
            analysis = analyst.analyze(SAMPLE_MARKET_NEWS)

            # Validation checks
            assert isinstance(analysis, MarketAnalysis), "Should return MarketAnalysis"
            assert analysis.trend_analysis, "Should have trend analysis"
            assert analysis.technical_indicators, "Should analyze technical indicators"
            assert analysis.sentiment_assessment, "Should assess sentiment"
            assert len(analysis.risk_factors) > 0, "Should identify risk factors"
            assert len(analysis.opportunities) > 0, "Should identify opportunities"
            assert analysis.outlook, "Should provide outlook"

            # Quality checks
            assert len(analysis.trend_analysis) > 50, "Trend analysis should be detailed"
            assert len(analysis.risk_factors) >= 1, "Should identify risks"
            assert len(analysis.opportunities) >= 1, "Should identify opportunities"

            print(f"✓ PASSED: Market analyst produces quality analysis")
            print(f"  - Trend analysis: {len(analysis.trend_analysis)} chars")
            print(f"  - Risk factors: {len(analysis.risk_factors)}")
            print(f"  - Opportunities: {len(analysis.opportunities)}")

            self.test_results.append(("Market Analyst Quality", True, None))
            return True

        except Exception as e:
            print(f"✗ FAILED: {e}")
            self.test_results.append(("Market Analyst Quality", False, str(e)))
            return False

    def test_end_to_end_routing(self):
        """
        TEST 7: End-to-End Routing Workflow
        Validates complete routing workflow (route + analyze).
        """
        print("\n" + "="*80)
        print("TEST 7: Routing - End-to-End Workflow")
        print("="*80)

        try:
            result = self.workflow.process(
                SAMPLE_EARNINGS_NEWS,
                title="Apple Q4 Earnings"
            )

            # Validation checks
            assert "routing_decision" in result, "Should have routing decision"
            assert "analysis_type" in result, "Should have analysis type"
            assert "analysis" in result, "Should have analysis"

            decision = result["routing_decision"]
            assert decision.route == "earnings", "Should route to earnings analyst"

            # Verify analysis is appropriate type
            analysis = result["analysis"]
            if decision.route == "earnings":
                assert isinstance(analysis, EarningsAnalysis), \
                    "Earnings route should produce EarningsAnalysis"

            print(f"✓ PASSED: End-to-end routing workflow works")
            print(f"  - Routed to: {decision.route}")
            print(f"  - Analysis type: {result['analysis_type']}")
            print(f"  - Confidence: {decision.confidence:.2f}")

            self.test_results.append(("End-to-End Routing", True, None))
            return True

        except Exception as e:
            print(f"✗ FAILED: {e}")
            self.test_results.append(("End-to-End Routing", False, str(e)))
            return False

    def test_batch_routing(self):
        """
        TEST 8: Batch Content Routing
        Validates workflow handles multiple content items correctly.
        """
        print("\n" + "="*80)
        print("TEST 8: Routing - Batch Processing")
        print("="*80)

        try:
            content_items = [
                {"title": "Earnings", "content": SAMPLE_EARNINGS_NEWS},
                {"title": "Market", "content": SAMPLE_MARKET_NEWS},
                {"title": "Policy", "content": SAMPLE_POLICY_NEWS}
            ]

            results = self.workflow.batch_process(content_items)

            # Validation checks
            assert len(results) == 3, "Should process all 3 items"

            # Verify different routing
            routes = [r["routing_decision"].route for r in results]
            assert "earnings" in routes, "Should route earnings content"
            assert "market" in routes, "Should route market content"
            assert "news" in routes, "Should route news content"

            # Each should have proper analysis
            for result in results:
                assert "analysis" in result, "Each should have analysis"
                assert "routing_decision" in result, "Each should have routing decision"

            print(f"✓ PASSED: Batch routing works correctly")
            print(f"  - Processed {len(results)} items")
            print(f"  - Routes: {', '.join(routes)}")
            print(f"  - All routed to appropriate specialists")

            self.test_results.append(("Batch Routing", True, None))
            return True

        except Exception as e:
            print(f"✗ FAILED: {e}")
            self.test_results.append(("Batch Routing", False, str(e)))
            return False

    def run_all_tests(self):
        """Run all routing tests."""
        print("\n" + "="*80)
        print("RUNNING ROUTING WORKFLOW TESTS")
        print("="*80)

        tests = [
            self.test_router_earnings_content,
            self.test_router_market_content,
            self.test_router_news_content,
            self.test_earnings_analyst_quality,
            self.test_news_analyst_quality,
            self.test_market_analyst_quality,
            self.test_end_to_end_routing,
            self.test_batch_routing
        ]

        for test in tests:
            test()

        # Print summary
        print("\n" + "="*80)
        print("ROUTING TEST SUMMARY")
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
    """Run routing tests."""
    test_suite = TestRouting()
    success = test_suite.run_all_tests()

    if success:
        print("All Routing tests passed! ✓")
        return 0
    else:
        print("Some tests failed. See details above.")
        return 1


if __name__ == "__main__":
    exit(main())
