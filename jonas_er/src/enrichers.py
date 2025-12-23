"""
Enrichment module for Jonas-ER

Provides modular enrichers that transform raw features into high-confidence
identifiers using external data sources (e.g., Google Maps API).
Implements feature-triggered execution to avoid unnecessary API calls.
"""

import os


class BaseEnricher:
    """
    Base class for all enrichers.
    
    An enricher takes a dictionary of features and returns additional
    attributes discovered via external search or transformation.
    """
    
    def enrich(self, features: dict) -> dict:
        """
        Enrich features by querying external sources.
        
        Args:
            features: Dictionary of extracted features (e.g., {"PERSON": "John", "GPE": "Seattle"})
            
        Returns:
            Dictionary of new attributes discovered (e.g., {"MAPS_PLACE_ID": "ChIJ..."})
        """
        raise NotImplementedError("Subclasses must implement enrich()")


class GoogleMapsEnricher(BaseEnricher):
    """
    Enricher that uses Google Maps API to convert fuzzy location+name pairs
    into high-confidence Place IDs.
    
    Requirements:
        - Needs a name (PERSON or ORG) and a location (GPE)
        - Returns: MAPS_PLACE_ID, FORMATTED_ADDRESS, LAT_LNG
    """
    
    def __init__(self, api_key=None):
        """
        Initialize Google Maps enricher.
        
        Args:
            api_key: Google Maps API key. If None, reads from GMAPS_API_KEY environment variable.
        """
        # In a real application, use: self.client = googlemaps.Client(key=api_key)
        self.api_key = api_key or os.getenv("GMAPS_API_KEY")
    
    def enrich(self, features: dict) -> dict:
        """
        Search Google Maps for a place based on name and location.
        
        Args:
            features: Dictionary containing ORG/PERSON and GPE keys
            
        Returns:
            Dictionary with MAPS_PLACE_ID, FORMATTED_ADDRESS, and LAT_LNG if found,
            empty dict otherwise.
        """
        # Requirement: Needs a name (PERSON or ORG) and a location (GPE)
        name = features.get('ORG') or features.get('PERSON')
        location = features.get('GPE')
        
        if not (name and location):
            return {}
        
        print(f"DEBUG: Searching Google Maps for '{name}' in '{location}'...")
        
        # Placeholder for real API call:
        # result = self.client.places(f"{name} in {location}")
        # if result.get('status') == 'OK':
        #     place = result['results'][0]
        #     return {
        #         "MAPS_PLACE_ID": place['place_id'],
        #         "FORMATTED_ADDRESS": place['formatted_address'],
        #         "LAT_LNG": f"{place['geometry']['location']['lat']},{place['geometry']['location']['lng']}"
        #     }
        
        # Mock result for demonstration:
        return {
            "MAPS_PLACE_ID": f"ChIJ-{name.replace(' ', '_')}-ID",
            "FORMATTED_ADDRESS": f"{name}, {location}, USA",
            "LAT_LNG": "34.0522,-118.2437"
        }
