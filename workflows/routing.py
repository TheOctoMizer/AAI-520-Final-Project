"""
Routing Workflow Pattern
Routes content to specialized analyst agents based on content type.

This pattern demonstrates intelligent task routing where a coordinator
determines which specialist should handle each piece of content.
"""
from typing import Dict, List, Optional, Literal
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from utils.llm_factory import create_chat_llm


class RoutingDecision(BaseModel):
    """Router's decision on where to send content."""
    route: Literal["earnings", "news", "market"] = Field(
        description="Which specialist to route to: earnings, news, or market"
    )
    confidence: float = Field(description="Confidence in routing decision (0-1)")
    reasoning: str = Field(description="Brief explanation of routing choice")


class EarningsAnalysis(BaseModel):
    """Output from the earnings specialist."""
    revenue_analysis: str = Field(description="Analysis of revenue performance")
    profitability_analysis: str = Field(description="Analysis of profit margins and EPS")
    growth_trends: str = Field(description="YoY and QoQ growth trends")
    guidance_assessment: str = Field(description="Assessment of forward guidance")
    key_metrics: List[str] = Field(description="Key financial metrics extracted")
    recommendation: str = Field(description="Investment recommendation")


class NewsAnalysis(BaseModel):
    """Output from the news specialist."""
    event_summary: str = Field(description="Summary of the news event")
    market_impact: str = Field(description="Potential market impact analysis")
    stakeholder_analysis: str = Field(description="Who is affected and how")
    timeline: str = Field(description="Timeline of events or expected developments")
    credibility_score: float = Field(description="News source credibility (0-1)")
    actionable_insights: List[str] = Field(description="Actionable takeaways")


class MarketAnalysis(BaseModel):
    """Output from the market specialist."""
    trend_analysis: str = Field(description="Overall market/sector trend analysis")
    technical_indicators: str = Field(description="Key technical signals")
    sentiment_assessment: str = Field(description="Market sentiment evaluation")
    risk_factors: List[str] = Field(description="Identified risk factors")
    opportunities: List[str] = Field(description="Identified opportunities")
    outlook: str = Field(description="Short to medium term outlook")


class ContentRouter:
    """
    Routes incoming content to specialized analyst agents.

    The router examines content and intelligently decides which specialist
    (earnings, news, or market analyst) should handle it.
    """

    def __init__(self, llm: Optional[ChatOpenAI] = None):
        """Initialize the router with an LLM."""
        self.llm = llm or create_chat_llm(temperature=0.1)

    def route(self, content: str, title: str = "") -> RoutingDecision:
        """
        Determine which specialist should analyze this content.

        Args:
            content: The content to analyze
            title: Optional title/headline

        Returns:
            RoutingDecision indicating which specialist to use
        """
        structured_llm = self.llm.with_structured_output(RoutingDecision)

        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a content router for financial analysis. Route content to specialists:

**earnings**: Quarterly/annual earnings reports, financial statements, revenue/profit data
**news**: Breaking news, events, announcements, M&A, policy changes, management changes
**market**: Market trends, sector analysis, technical analysis, broad market commentary

Choose the MOST appropriate specialist based on the primary focus of the content.
Provide reasoning for your choice."""),
            ("user", "Title: {title}\n\nContent: {content}\n\nWhich specialist should analyze this?")
        ])

        chain = prompt | structured_llm
        return chain.invoke({"title": title, "content": content})


class EarningsAnalyst:
    """Specialist agent for earnings analysis."""

    def __init__(self, llm: Optional[ChatOpenAI] = None):
        """Initialize the earnings analyst."""
        self.llm = llm or create_chat_llm(temperature=0.2)

    def analyze(self, content: str) -> EarningsAnalysis:
        """
        Perform deep earnings analysis.

        Args:
            content: Earnings-related content

        Returns:
            EarningsAnalysis with detailed financial breakdown
        """
        structured_llm = self.llm.with_structured_output(EarningsAnalysis)

        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert earnings analyst. Analyze financial results thoroughly.

Focus on:
- Revenue growth and trends
- Profitability (margins, EPS, operating income)
- YoY and QoQ comparisons
- Forward guidance quality
- Key performance metrics
- Investment implications

Provide actionable recommendations for investors."""),
            ("user", "Analyze this earnings content:\n\n{content}")
        ])

        chain = prompt | structured_llm
        return chain.invoke({"content": content})


class NewsAnalyst:
    """Specialist agent for news analysis."""

    def __init__(self, llm: Optional[ChatOpenAI] = None):
        """Initialize the news analyst."""
        self.llm = llm or create_chat_llm(temperature=0.3)

    def analyze(self, content: str) -> NewsAnalysis:
        """
        Perform news impact analysis.

        Args:
            content: News content

        Returns:
            NewsAnalysis with event impact assessment
        """
        structured_llm = self.llm.with_structured_output(NewsAnalysis)

        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert news analyst specializing in financial news impact.

Analyze:
- What happened and why it matters
- Potential market impact (stocks, sectors affected)
- Stakeholder implications (companies, investors, regulators)
- Timeline of developments
- Source credibility
- Actionable insights for investors

Be objective and focus on investment implications."""),
            ("user", "Analyze this news:\n\n{content}")
        ])

        chain = prompt | structured_llm
        return chain.invoke({"content": content})


class MarketAnalyst:
    """Specialist agent for market analysis."""

    def __init__(self, llm: Optional[ChatOpenAI] = None):
        """Initialize the market analyst."""
        self.llm = llm or create_chat_llm(temperature=0.3)

    def analyze(self, content: str) -> MarketAnalysis:
        """
        Perform market trend analysis.

        Args:
            content: Market-related content

        Returns:
            MarketAnalysis with trend and sentiment assessment
        """
        structured_llm = self.llm.with_structured_output(MarketAnalysis)

        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert market analyst. Analyze market trends and conditions.

Evaluate:
- Overall market/sector trends
- Technical indicators and signals
- Market sentiment (bullish/bearish/neutral)
- Risk factors to watch
- Investment opportunities
- Short to medium term outlook

Provide balanced, data-driven analysis."""),
            ("user", "Analyze this market content:\n\n{content}")
        ])

        chain = prompt | structured_llm
        return chain.invoke({"content": content})


class RoutingWorkflow:
    """
    Complete routing workflow that coordinates content routing and analysis.

    This workflow demonstrates the routing pattern where content is
    intelligently directed to the most appropriate specialist agent.
    """

    def __init__(self, llm: Optional[ChatOpenAI] = None):
        """Initialize the routing workflow with all specialists."""
        self.router = ContentRouter(llm)
        self.earnings_analyst = EarningsAnalyst(llm)
        self.news_analyst = NewsAnalyst(llm)
        self.market_analyst = MarketAnalyst(llm)

    def process(self, content: str, title: str = "") -> Dict:
        """
        Route content to appropriate specialist and return analysis.

        Args:
            content: Content to analyze
            title: Optional title

        Returns:
            Dictionary with routing decision and specialist analysis
        """
        print("\n=== ROUTING WORKFLOW ===")

        # Step 1: Route the content
        print("\n[1/2] Routing content to specialist...")
        routing_decision = self.router.route(content, title)
        print(f"✓ Routed to: {routing_decision.route.upper()} analyst "
              f"(confidence: {routing_decision.confidence:.2f})")
        print(f"  Reasoning: {routing_decision.reasoning}")

        # Step 2: Analyze with appropriate specialist
        print(f"\n[2/2] {routing_decision.route.upper()} analyst processing...")

        if routing_decision.route == "earnings":
            analysis = self.earnings_analyst.analyze(content)
            analysis_type = "Earnings Analysis"
        elif routing_decision.route == "news":
            analysis = self.news_analyst.analyze(content)
            analysis_type = "News Analysis"
        else:  # market
            analysis = self.market_analyst.analyze(content)
            analysis_type = "Market Analysis"

        print(f"✓ {analysis_type} complete")
        print("\n=== WORKFLOW COMPLETE ===\n")

        return {
            "routing_decision": routing_decision,
            "analysis_type": analysis_type,
            "analysis": analysis
        }

    def batch_process(self, content_items: List[Dict[str, str]]) -> List[Dict]:
        """
        Process multiple content items, routing each appropriately.

        Args:
            content_items: List of dicts with 'content' and optional 'title'

        Returns:
            List of analysis results
        """
        results = []
        for i, item in enumerate(content_items, 1):
            print(f"\n{'='*60}")
            print(f"Processing item {i}/{len(content_items)}")
            print(f"{'='*60}")

            result = self.process(
                content=item.get("content", ""),
                title=item.get("title", "")
            )
            results.append(result)

        return results


def demonstrate_routing():
    """Demonstration of the routing workflow with different content types."""

    workflow = RoutingWorkflow()

    # Sample content of different types
    test_content = [
        {
            "title": "Apple Reports Q1 Earnings Beat",
            "content": """
            Apple Inc. reported fiscal Q1 results with revenue of $119.6 billion, up 2% YoY,
            beating estimates of $118.3 billion. iPhone revenue reached $69.7 billion, up 6%.
            Services revenue hit a record $23.1 billion. EPS came in at $2.18 vs $2.10 expected.
            Gross margin improved to 45.9% from 43.0% last year. CEO Tim Cook noted strong
            demand in emerging markets. The company announced a 4% dividend increase.
            """
        },
        {
            "title": "Fed Signals Potential Rate Cuts in 2024",
            "content": """
            Federal Reserve Chair Jerome Powell indicated the central bank may begin cutting
            interest rates later this year if inflation continues to moderate. Speaking at
            a press conference, Powell stated that recent economic data shows progress toward
            the 2% inflation target. Markets rallied on the dovish tone, with the S&P 500
            gaining 1.2%. Analysts now expect 2-3 rate cuts in 2024.
            """
        },
        {
            "title": "Tech Sector Shows Bullish Momentum",
            "content": """
            Technology stocks continued their uptrend with the Nasdaq composite gaining 15%
            YTD. Strong momentum in AI-related names is driving the rally. The tech sector
            RSI stands at 68, approaching overbought territory. Volume has been above average,
            confirming the trend. Support levels have held at the 50-day moving average.
            Sector rotation shows investors favoring growth over value.
            """
        }
    ]

    print("\n" + "="*60)
    print("ROUTING WORKFLOW DEMONSTRATION")
    print("Testing with 3 different content types")
    print("="*60)

    results = workflow.batch_process(test_content)

    # Display summary
    print("\n" + "="*60)
    print("ROUTING SUMMARY")
    print("="*60)
    for i, result in enumerate(results, 1):
        print(f"\nContent {i}: {test_content[i-1]['title']}")
        print(f"  → Routed to: {result['routing_decision'].route}")
        print(f"  → Analysis type: {result['analysis_type']}")

    return results


if __name__ == "__main__":
    demonstrate_routing()
