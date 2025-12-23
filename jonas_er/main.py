"""
Jonas-ER Main Entry Point

Example usage of the Jonas-ER entity resolution system with enrichment pipeline.
Implements Extract -> Enrich -> Resolve workflow.
"""

from src.database import Database
from src.engine import ResolutionEngine
from src.extractors import FeatureExtractor
from src.enrichers import GoogleMapsEnricher
from src.registry import EnrichmentRegistry


def main():
    """
    Main entry point for Jonas-ER demonstration with enrichment pipeline.
    """
    print("🧠 Jonas-ER: Personal Entity Resolution Engine")
    print("=" * 50)
    
    # 1. Initialize components
    print("\n1. Initializing database...")
    db = Database()
    
    print("2. Loading NLP models...")
    extractor = FeatureExtractor()
    
    print("3. Initializing resolution engine...")
    engine = ResolutionEngine(db)
    
    print("4. Setting up enrichment registry...")
    registry = EnrichmentRegistry()
    
    # 5. Configure enrichers
    # Register Google Maps enricher - requires ORG and GPE features
    registry.register(["ORG", "GPE"], GoogleMapsEnricher())
    
    print("\n✅ System initialized successfully!")
    print("\n" + "=" * 50)
    print("Enrichment Pipeline Demo")
    print("=" * 50)
    
    # Define process_item function for the integrated pipeline
    def process_item(raw_text):
        """
        Process a single text item through the full pipeline:
        A. Extract features using NLP
        B. Triage and enrich with external sources
        C. Resolve to entity ID
        
        Args:
            raw_text: Raw text to process
            
        Returns:
            Entity ID (UUID string)
        """
        print(f"\n📝 Processing: '{raw_text}'")
        
        # A. Extract features
        features = extractor.extract_features(raw_text)
        print(f"   Extracted features: {features}")
        
        # B. Triage & Enrich
        enrichers = registry.get_applicable_enrichers(features)
        if enrichers:
            print(f"   Applying {len(enrichers)} enricher(s)...")
            for enricher in enrichers:
                new_data = enricher.enrich(features)
                features.update(new_data)  # "Sharpen" the features
            print(f"   Enriched features: {features}")
        else:
            print("   No applicable enrichers (missing required features)")
        
        # C. Resolve to entity
        entity_id = engine.resolve(features)
        print(f"   ✓ Resolved to Entity: {entity_id[:8]}...")
        
        return entity_id
    
    # Example: Same place, slightly different names
    print("\n🎯 Example: Testing entity resolution with enrichment")
    print("   These should resolve to the same entity due to Place ID matching:")
    
    entity_1 = process_item("Dinner at Starbucks NYC")
    entity_2 = process_item("S.Bucks Coffee New York")
    
    if entity_1 == entity_2:
        print("\n🎉 Success! Both resolved to the same entity")
    else:
        print(f"\n⚠️  Different entities: {entity_1[:8]}... vs {entity_2[:8]}...")
    
    print("\n" + "=" * 50)
    print("\n📚 For more examples, see README.md")
    print("💡 To add custom enrichers, see src/enrichers.py")


if __name__ == "__main__":
    main()