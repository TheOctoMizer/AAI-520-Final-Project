"""Configuration module for the autonomous research agent."""
import os

# LLM Configuration
LMSTUDIO_URL = "http://localhost:1234/v1"
LLM_NAME = "gemma-3-27b-it-qat"  # Match the actual model ID from LM Studio
ENTITY_EXTRACTOR = "gemma-3-27b-it-qat"  # Use same model for extraction
EXTRACTION_TEMPERATURE = 0

# API Keys
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Data Fetching
FETCH_DELAY_SECONDS = 1.5

# Database
SQLITE_DB_PATH = "kg_store.db"
MEMORY_DB_PATH = "agent_memory.db"

# Financial Entity Labels
FINANCIAL_ENTITY_LABELS = {
    "ORGANIZATION", "PERSON", "PRODUCT", "EVENT",
    "STOCK_SYMBOL", "POLICY", "GOVERNMENT", "COMPANY"
}
