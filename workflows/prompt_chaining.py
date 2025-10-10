"""
Prompt Chaining Workflow Pattern
Pipeline: Ingest News → Preprocess → Classify → Extract → Summarize

This workflow demonstrates sequential processing where each step's output
feeds into the next step's input.
"""
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from utils.llm_factory import create_chat_llm


class NewsArticle(BaseModel):
    """Raw news article model."""
    title: str
    content: str
    source: str
    timestamp: Optional[str] = None


class PreprocessedNews(BaseModel):
    """Cleaned and normalized news article."""
    title: str
    cleaned_content: str
    source: str
    word_count: int
    contains_financials: bool


class NewsClassification(BaseModel):
    """Classification result for news article."""
    category: str = Field(description="Category: earnings, market_analysis, policy, merger_acquisition, general")
    sentiment: str = Field(description="Sentiment: positive, negative, neutral")
    relevance_score: float = Field(description="Relevance score 0-1")
    confidence: float = Field(description="Classification confidence 0-1")


class ExtractedEntities(BaseModel):
    """Extracted entities and key facts from news."""
    companies: List[str] = Field(description="Company names mentioned")
    people: List[str] = Field(description="Key people mentioned")
    financial_metrics: List[str] = Field(description="Financial metrics (revenue, EPS, etc.)")
    key_events: List[str] = Field(description="Important events or announcements")
    stock_symbols: List[str] = Field(description="Stock ticker symbols")


class NewsSummary(BaseModel):
    """Final summarized output."""
    executive_summary: str = Field(description="2-3 sentence summary")
    key_points: List[str] = Field(description="Bullet points of key takeaways")
    investment_implications: str = Field(description="What this means for investors")
    entities: ExtractedEntities
    classification: NewsClassification


class PromptChainWorkflow:
    """
    Implements the Prompt Chaining workflow pattern for news analysis.

    Each step in the chain processes the output from the previous step,
    demonstrating how complex tasks can be broken down into sequential
    specialized subtasks.
    """

    def __init__(self, llm: Optional[ChatOpenAI] = None):
        """Initialize the workflow with an LLM instance."""
        self.llm = llm or create_chat_llm(temperature=0.3)

    def step1_ingest(self, raw_text: str, source: str = "Unknown") -> NewsArticle:
        """
        Step 1: Ingest raw news data.

        Args:
            raw_text: Raw news content
            source: Source of the news

        Returns:
            NewsArticle object
        """
        # Simple parsing - in real world, this might scrape from APIs
        lines = raw_text.strip().split('\n')
        title = lines[0] if lines else "Untitled"
        content = '\n'.join(lines[1:]) if len(lines) > 1 else raw_text

        return NewsArticle(
            title=title,
            content=content,
            source=source
        )

    def step2_preprocess(self, article: NewsArticle) -> PreprocessedNews:
        """
        Step 2: Clean and preprocess the news article.

        Args:
            article: Raw news article

        Returns:
            PreprocessedNews object with cleaned content
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a text preprocessing expert. Clean and normalize the following news article. "
                      "Remove ads, boilerplate, redundant info. Keep only substantive content."),
            ("user", "Title: {title}\n\nContent: {content}")
        ])

        chain = prompt | self.llm
        response = chain.invoke({
            "title": article.title,
            "content": article.content
        })

        cleaned_content = response.content
        word_count = len(cleaned_content.split())
        contains_financials = any(term in cleaned_content.lower()
                                 for term in ['revenue', 'earnings', 'eps', 'profit', 'loss', 'quarter'])

        return PreprocessedNews(
            title=article.title,
            cleaned_content=cleaned_content,
            source=article.source,
            word_count=word_count,
            contains_financials=contains_financials
        )

    def step3_classify(self, preprocessed: PreprocessedNews) -> NewsClassification:
        """
        Step 3: Classify the news article by category and sentiment.

        Args:
            preprocessed: Preprocessed news article

        Returns:
            NewsClassification with category, sentiment, and scores
        """
        structured_llm = self.llm.with_structured_output(NewsClassification)

        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a financial news classifier. Analyze the article and classify it.

Categories:
- earnings: Quarterly/annual earnings reports
- market_analysis: Market trends, sector analysis
- policy: Government policy, regulation, central bank
- merger_acquisition: M&A, partnerships, deals
- general: Other business news

Sentiment: positive, negative, or neutral
Relevance: How relevant to investors (0-1)
Confidence: Your confidence in this classification (0-1)"""),
            ("user", "Title: {title}\n\nContent: {content}")
        ])

        chain = prompt | structured_llm
        return chain.invoke({
            "title": preprocessed.title,
            "content": preprocessed.cleaned_content
        })

    def step4_extract(self, preprocessed: PreprocessedNews) -> ExtractedEntities:
        """
        Step 4: Extract key entities and facts from the article.

        Args:
            preprocessed: Preprocessed news article

        Returns:
            ExtractedEntities with companies, people, metrics, events
        """
        structured_llm = self.llm.with_structured_output(ExtractedEntities)

        prompt = ChatPromptTemplate.from_messages([
            ("system", """Extract key entities from this financial news article.

Focus on:
- Company names and stock symbols
- Key executives, analysts, officials
- Financial metrics (revenue, EPS, growth %, margins, etc.)
- Important events or announcements

Be precise and extract only what's explicitly mentioned."""),
            ("user", "{content}")
        ])

        chain = prompt | structured_llm
        return chain.invoke({"content": preprocessed.cleaned_content})

    def step5_summarize(
        self,
        preprocessed: PreprocessedNews,
        classification: NewsClassification,
        entities: ExtractedEntities
    ) -> NewsSummary:
        """
        Step 5: Generate final summary with investment implications.

        Args:
            preprocessed: Preprocessed news
            classification: Classification results
            entities: Extracted entities

        Returns:
            NewsSummary with executive summary and key insights
        """
        structured_llm = self.llm.with_structured_output(NewsSummary)

        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a financial analyst. Create a concise summary for investors.

Include:
- Executive summary (2-3 sentences)
- Key points as bullet list
- Investment implications (what this means for investors)

Be clear, actionable, and focused on financial impact."""),
            ("user", """Article: {title}

Content: {content}

Category: {category}
Sentiment: {sentiment}

Extracted Entities:
Companies: {companies}
People: {people}
Financial Metrics: {metrics}
Key Events: {events}

Create a comprehensive summary.""")
        ])

        chain = prompt | structured_llm
        result = chain.invoke({
            "title": preprocessed.title,
            "content": preprocessed.cleaned_content,
            "category": classification.category,
            "sentiment": classification.sentiment,
            "companies": ", ".join(entities.companies) if entities.companies else "None",
            "people": ", ".join(entities.people) if entities.people else "None",
            "metrics": ", ".join(entities.financial_metrics) if entities.financial_metrics else "None",
            "events": ", ".join(entities.key_events) if entities.key_events else "None"
        })

        # Attach entities and classification to summary
        result.entities = entities
        result.classification = classification

        return result

    def run(self, raw_text: str, source: str = "Unknown") -> NewsSummary:
        """
        Execute the complete prompt chaining workflow.

        Pipeline: Ingest → Preprocess → Classify → Extract → Summarize

        Args:
            raw_text: Raw news text
            source: News source

        Returns:
            NewsSummary with complete analysis
        """
        print("\n=== PROMPT CHAINING WORKFLOW ===")

        # Step 1: Ingest
        print("\n[1/5] Ingesting raw news...")
        article = self.step1_ingest(raw_text, source)
        print(f"✓ Ingested: {article.title[:50]}...")

        # Step 2: Preprocess
        print("\n[2/5] Preprocessing content...")
        preprocessed = self.step2_preprocess(article)
        print(f"✓ Preprocessed: {preprocessed.word_count} words, "
              f"Contains financials: {preprocessed.contains_financials}")

        # Step 3: Classify
        print("\n[3/5] Classifying news...")
        classification = self.step3_classify(preprocessed)
        print(f"✓ Classified: {classification.category} | {classification.sentiment} "
              f"(confidence: {classification.confidence:.2f})")

        # Step 4: Extract
        print("\n[4/5] Extracting entities...")
        entities = self.step4_extract(preprocessed)
        print(f"✓ Extracted: {len(entities.companies)} companies, "
              f"{len(entities.financial_metrics)} metrics")

        # Step 5: Summarize
        print("\n[5/5] Generating summary...")
        summary = self.step5_summarize(preprocessed, classification, entities)
        print(f"✓ Summary complete: {len(summary.key_points)} key points")

        print("\n=== WORKFLOW COMPLETE ===\n")
        return summary


def demonstrate_prompt_chaining():
    """Demonstration of the prompt chaining workflow."""

    sample_news = """
    Microsoft Reports Strong Q4 Earnings, Cloud Revenue Surges 25%

    Microsoft Corporation (MSFT) announced its fiscal Q4 2024 results today, beating analyst
    expectations with revenue of $61.9 billion, up 15% year-over-year. CEO Satya Nadella
    highlighted the company's AI investments, noting that Azure cloud services grew 25%
    driven by demand for AI infrastructure.

    Earnings per share came in at $2.95, compared to consensus estimates of $2.85. The
    Intelligent Cloud segment generated $28.5 billion in revenue, while Productivity and
    Business Processes reached $19.6 billion.

    "We are seeing unprecedented demand for AI capabilities across our cloud platform,"
    Nadella stated during the earnings call. The company also announced a 10% increase
    in its quarterly dividend to $0.75 per share.

    Shares rose 4% in after-hours trading following the announcement.
    """

    workflow = PromptChainWorkflow()
    summary = workflow.run(sample_news, source="Company Press Release")

    print("\n=== FINAL SUMMARY ===")
    print(f"\nExecutive Summary:\n{summary.executive_summary}")
    print(f"\nKey Points:")
    for i, point in enumerate(summary.key_points, 1):
        print(f"  {i}. {point}")
    print(f"\nInvestment Implications:\n{summary.investment_implications}")
    print(f"\nCategory: {summary.classification.category}")
    print(f"Sentiment: {summary.classification.sentiment}")
    print(f"Companies: {', '.join(summary.entities.companies)}")

    return summary


if __name__ == "__main__":
    demonstrate_prompt_chaining()
