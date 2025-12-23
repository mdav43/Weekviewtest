"""
Enrichment registry module for Jonas-ER

Implements feature-triggered enrichment pipeline that determines which
enrichers should run based on available features. This prevents unnecessary
API calls and provides intelligent routing of data through enrichment steps.
"""

from src.enrichers import BaseEnricher


class EnrichmentRegistry:
    """
    Registry that manages enrichers and determines which ones to apply
    based on available features.
    
    This acts as the "brain" that checks what features are present and
    decides which enrichers are compatible, implementing the principle
    of Feature-Triggered Execution.
    """
    
    def __init__(self):
        """Initialize empty registry."""
        self._rules = []  # List of (required_feature_set, enricher_instance) tuples
    
    def register(self, required_features: list, enricher: BaseEnricher):
        """
        Register an enricher with its feature requirements.
        
        Args:
            required_features: List of feature keys that must be present
                              (e.g., ["ORG", "GPE"] for Google Maps enricher)
            enricher: Instance of an enricher class
        """
        self._rules.append((set(required_features), enricher))
    
    def get_applicable_enrichers(self, current_features: dict):
        """
        Determine which enrichers can run given the current features.
        
        Args:
            current_features: Dictionary of currently available features
            
        Returns:
            List of enricher instances that have all their required features satisfied
        """
        available_keys = set(current_features.keys())
        return [
            enricher for reqs, enricher in self._rules
            if reqs.issubset(available_keys)
        ]
