"""Knowledge graph construction and expansion utilities."""
import networkx as nx
import time
from typing import List, Dict, Optional, Set
from textwrap import dedent
from langchain_openai import ChatOpenAI
from utils.data_models import Entity, NERResponse
from utils.data_fetchers import FinancialDataFetcher
from utils.llm_factory import create_extraction_llm
from utils.config import FINANCIAL_ENTITY_LABELS, FETCH_DELAY_SECONDS


def is_relevant_entity(ent: Entity) -> bool:
    """
    Filter out irrelevant or low-quality entities.

    Args:
        ent: Entity to evaluate

    Returns:
        True if entity is relevant, False otherwise
    """
    # Check minimum length
    if not ent.text or len(ent.text.strip()) < 2:
        return False

    # Filter numeric values (prices, percentages)
    if ent.text.replace('.', '', 1).replace('%', '', 1).isdigit():
        return False

    # Check if entity type is relevant
    if ent.label.upper() not in FINANCIAL_ENTITY_LABELS:
        return False

    return True


class KnowledgeGraphBuilder:
    """
    Builds and expands a knowledge graph from financial entities.

    This integrates with the existing knowledge graph approach from
    langchain.ipynb but in a more modular, maintainable structure.
    """

    def __init__(
        self,
        llm: Optional[ChatOpenAI] = None,
        fetcher: Optional[FinancialDataFetcher] = None
    ):
        """
        Initialize the knowledge graph builder.

        Args:
            llm: Language model for entity extraction
            fetcher: Data fetcher for retrieving entity information
        """
        self.extraction_llm = llm or create_extraction_llm()
        self.fetcher = fetcher or FinancialDataFetcher()
        self.graph = nx.Graph()

        # Set up structured output for NER
        self.ner_model = self.extraction_llm.with_structured_output(NERResponse)

    def extract_entities(self, text: str) -> List[Entity]:
        """
        Extract named entities from text using NER.

        Args:
            text: Text to extract entities from

        Returns:
            List of relevant entities
        """
        try:
            prompt = dedent(f"""Extract named entities from the following financial text.

Focus on:
- Companies and organizations
- People (executives, analysts)
- Stock symbols
- Products and services
- Events
- Government/policy entities

Text:
{text[:8000]}

Extract all relevant entities:""")

            ner_result = self.ner_model.invoke(prompt)
            relevant_entities = [e for e in ner_result.entities if is_relevant_entity(e)]
            return relevant_entities

        except Exception as e:
            print(f"[Error] NER extraction failed: {e}")
            return []

    def add_entity_to_graph(
        self,
        entity: Entity,
        related_entities: List[Entity],
        context: Optional[str] = None
    ):
        """
        Add an entity and its relationships to the graph.

        Args:
            entity: Main entity to add
            related_entities: Entities related to the main entity
            context: Optional context snippet
        """
        # Add main entity node if not exists
        if not self.graph.has_node(entity.text):
            self.graph.add_node(
                entity.text,
                label=entity.label,
                confidence=entity.confidence
            )

        # Add related entities and edges
        for related in related_entities:
            if not self.graph.has_node(related.text):
                self.graph.add_node(
                    related.text,
                    label=related.label,
                    confidence=related.confidence
                )

            # Add edge if not exists
            if not self.graph.has_edge(entity.text, related.text):
                self.graph.add_edge(
                    entity.text,
                    related.text,
                    relation="mentioned_with",
                    context=(context or "")[:400]
                )

    def expand_from_seed(
        self,
        seed_entity: str,
        seed_label: str = "STOCK_SYMBOL",
        depth: int = 2,
        throttle: float = FETCH_DELAY_SECONDS
    ) -> nx.Graph:
        """
        Expand knowledge graph starting from a seed entity.

        Args:
            seed_entity: Starting entity (e.g., "MSFT")
            seed_label: Type of seed entity
            depth: How many layers to expand
            throttle: Delay between fetches in seconds

        Returns:
            Expanded NetworkX graph
        """
        visited: Set[str] = set()
        current_layer = [Entity(text=seed_entity, label=seed_label)]

        print(f"\n=== EXPANDING KNOWLEDGE GRAPH ===")
        print(f"Seed: {seed_entity} ({seed_label})")
        print(f"Depth: {depth} layers")

        for layer in range(1, depth + 1):
            print(f"\n--- Layer {layer}/{depth} ---")
            next_layer: List[Entity] = []

            for entity in current_layer:
                if entity.text in visited:
                    continue

                visited.add(entity.text)
                print(f"[L{layer}] Processing '{entity.text}' ({entity.label})")

                # Fetch information about this entity
                info = self.fetcher.fetch_entity_info(entity.text, entity.label)

                if not info.strip() or info.startswith("No relevant data"):
                    print(f"[L{layer}] No data found for '{entity.text}'")
                    continue

                # Extract entities from the fetched information
                print(f"[L{layer}] Extracting entities from data...")
                discovered_entities = self.extract_entities(info)
                print(f"[L{layer}] Found {len(discovered_entities)} entities")

                # Add to graph
                self.add_entity_to_graph(entity, discovered_entities, info)

                # Add undiscovered entities to next layer
                for discovered in discovered_entities:
                    if discovered.text not in visited:
                        next_layer.append(discovered)

                # Throttle to avoid rate limits
                time.sleep(throttle)

            current_layer = next_layer

            if not current_layer:
                print(f"\n[L{layer}] No new entities to explore. Stopping.")
                break

        print(f"\n=== GRAPH EXPANSION COMPLETE ===")
        print(f"Total nodes: {self.graph.number_of_nodes()}")
        print(f"Total edges: {self.graph.number_of_edges()}")

        return self.graph

    def get_graph_summary(self) -> str:
        """
        Generate a text summary of the graph.

        Returns:
            Human-readable graph summary
        """
        lines = [
            f"Knowledge Graph Summary:",
            f"  Nodes: {self.graph.number_of_nodes()}",
            f"  Edges: {self.graph.number_of_edges()}",
            f"\nEntities by Type:"
        ]

        # Count entities by type
        label_counts: Dict[str, int] = {}
        for node, data in self.graph.nodes(data=True):
            label = data.get('label', 'UNKNOWN')
            label_counts[label] = label_counts.get(label, 0) + 1

        for label, count in sorted(label_counts.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"  {label}: {count}")

        lines.append(f"\nTop Connected Entities:")
        # Get nodes sorted by degree (number of connections)
        node_degrees = [(node, self.graph.degree(node)) for node in self.graph.nodes()]
        node_degrees.sort(key=lambda x: x[1], reverse=True)

        for node, degree in node_degrees[:10]:
            label = self.graph.nodes[node].get('label', 'UNKNOWN')
            lines.append(f"  {node} ({label}): {degree} connections")

        return "\n".join(lines)

    def get_entity_context(self, entity_name: str) -> Dict:
        """
        Get detailed context for a specific entity from the graph.

        Args:
            entity_name: Name of the entity

        Returns:
            Dictionary with entity details and connections
        """
        if entity_name not in self.graph:
            return {"error": f"Entity '{entity_name}' not found in graph"}

        # Get node data
        node_data = self.graph.nodes[entity_name]

        # Get neighbors
        neighbors = list(self.graph.neighbors(entity_name))

        # Get edge contexts
        connections = []
        for neighbor in neighbors:
            edge_data = self.graph.get_edge_data(entity_name, neighbor)
            connections.append({
                "entity": neighbor,
                "label": self.graph.nodes[neighbor].get('label', 'UNKNOWN'),
                "relation": edge_data.get('relation', 'unknown'),
                "context": edge_data.get('context', '')[:200]
            })

        return {
            "entity": entity_name,
            "label": node_data.get('label', 'UNKNOWN'),
            "confidence": node_data.get('confidence'),
            "num_connections": len(neighbors),
            "connections": connections
        }
