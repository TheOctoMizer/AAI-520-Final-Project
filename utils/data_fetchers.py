"""Data fetching utilities for financial information."""
import requests
import json
import time
from typing import Optional
from langchain_community.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain_community.tools import DuckDuckGoSearchResults, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from utils.config import ALPHA_VANTAGE_API_KEY, FETCH_DELAY_SECONDS


class FinancialDataFetcher:
    """Fetches financial data from various sources."""

    def __init__(self):
        """Initialize data fetching tools."""
        self.yahoo_news = YahooFinanceNewsTool()
        self.wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
        self.ddgo = DuckDuckGoSearchResults()

    def fetch_alpha_vantage_quote(self, ticker: str) -> str:
        """
        Fetch stock quote from Alpha Vantage.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Formatted quote data or empty string
        """
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": ticker,
                "apikey": ALPHA_VANTAGE_API_KEY
            }
            resp = requests.get(url, params=params, timeout=15)
            data = resp.json()
            quote = data.get("Global Quote") or {}

            if not quote:
                return ""

            return f"AlphaVantage Quote for {ticker}:\n{json.dumps(quote, indent=2)}"
        except Exception as e:
            print(f"[Error] AlphaVantage: {e}")
            return ""

    def fetch_yahoo_news(self, ticker: str) -> str:
        """
        Fetch recent news from Yahoo Finance.

        Args:
            ticker: Stock ticker symbol

        Returns:
            News content or empty string
        """
        try:
            res = self.yahoo_news.invoke(ticker)
            if isinstance(res, str) and len(res.strip()) > 50 and "No news found" not in res:
                return f"Yahoo Finance News for {ticker}:\n{res}"
        except Exception as e:
            print(f"[Error] YahooNewsTool: {e}")
        return ""

    def fetch_wikipedia_info(self, entity_name: str) -> str:
        """
        Fetch information from Wikipedia.

        Args:
            entity_name: Entity to search for

        Returns:
            Wikipedia content or empty string
        """
        try:
            res = self.wiki.run(entity_name)
            if isinstance(res, str) and len(res.strip()) > 50:
                return res[:4000]  # Limit length
        except Exception as e:
            print(f"[Error] Wikipedia: {e}")
        return ""

    def fetch_duckduckgo_search(self, query: str) -> str:
        """
        Fetch search results from DuckDuckGo.

        Args:
            query: Search query

        Returns:
            Search results or empty string
        """
        try:
            res = self.ddgo.run(query)
            if isinstance(res, str) and len(res.strip()) > 50:
                return res[:4000]  # Limit length
        except Exception as e:
            print(f"[Error] DuckDuckGo: {e}")
        return ""

    def fetch_entity_info(self, entity_name: str, entity_label: str) -> str:
        """
        Fetch information about an entity based on its type.

        Args:
            entity_name: Name of the entity
            entity_label: Type of entity (STOCK_SYMBOL, PERSON, etc.)

        Returns:
            Aggregated information about the entity
        """
        entity_label = entity_label.upper()
        text = ""

        # Stock symbols and companies: get financial data + news
        if entity_label in {"STOCK_SYMBOL", "ORGANIZATION", "COMPANY"}:
            text = self.fetch_alpha_vantage_quote(entity_name)
            text += "\n\n" + self.fetch_yahoo_news(entity_name)

        # People: get background information
        elif entity_label == "PERSON":
            text = self.fetch_wikipedia_info(entity_name)

        # Policies, government: search for recent news
        elif entity_label in {"POLICY", "GOVERNMENT", "EVENT"}:
            print(f"[Policy Search] Searching for '{entity_name}'")
            query = f"{entity_name} government budget OR regulation OR policy 2025 site:reuters.com OR site:bloomberg.com"
            text = self.fetch_duckduckgo_search(query)

        # Fallback: try Wikipedia/DuckDuckGo
        if not text or text.strip() == "":
            # Try Wikipedia first
            wiki_result = self.fetch_wikipedia_info(entity_name)
            if wiki_result:
                text = wiki_result
            else:
                # Then try DuckDuckGo
                text = self.fetch_duckduckgo_search(entity_name)

        return text.strip() or f"No relevant data found for {entity_name}"
