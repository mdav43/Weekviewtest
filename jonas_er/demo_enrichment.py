#!/usr/bin/env python3
"""
Minimal demo of Jonas-ER enrichment pipeline without NLP dependencies.

This script demonstrates the enrichment workflow with manually created features.
"""

import sys
import os
import logging

# Configure logging to show debug messages
logging.basicConfig(level=logging.INFO, format='%(message)s')
# Enable debug logging for enrichers module
logging.getLogger('enrichers').setLevel(logging.DEBUG)

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database import Database
from engine import ResolutionEngine
from enrichers import GoogleMapsEnricher
from registry import EnrichmentRegistry


def main():
    """Run enrichment pipeline demo"""
    
    print("🧠 Jonas-ER: Enrichment Pipeline Demo")
    print("=" * 60)
    
    # 1. Initialize components
    print("\n1. Initializing system...")
    db = Database(db_path=":memory:")
    engine = ResolutionEngine(db)
    registry = EnrichmentRegistry()
    print("   ✓ Database, engine, and registry initialized")
    
    # 2. Configure enrichers
    print("\n2. Configuring enrichers...")
    registry.register(["ORG", "GPE"], GoogleMapsEnricher())
    print("   ✓ Google Maps enricher registered (requires ORG + GPE)")
    
    # 3. Define process_item function
    def process_item(raw_text, features):
        """Process item through enrichment pipeline"""
        print(f"\n📝 Processing: '{raw_text}'")
        print(f"   Extracted features: {features}")
        
        # Triage & Enrich
        enrichers = registry.get_applicable_enrichers(features)
        if enrichers:
            print(f"   Applying {len(enrichers)} enricher(s)...")
            for enricher in enrichers:
                new_data = enricher.enrich(features)
                features.update(new_data)
            print(f"   Enriched features: {features}")
        else:
            print("   No applicable enrichers")
        
        # Resolve
        entity_id = engine.resolve(features)
        print(f"   ✓ Resolved to Entity: {entity_id[:8]}...")
        
        # Index the entity
        for attr_type, attr_value in features.items():
            existing = db.conn.execute(
                "SELECT COUNT(*) FROM entity_index WHERE attr_value = ? AND entity_id = ?",
                (attr_value, entity_id)
            ).fetchone()[0]
            if existing == 0:
                db.conn.execute(
                    "INSERT INTO entity_index (attr_type, attr_value, entity_id) VALUES (?, ?, ?)",
                    (attr_type, attr_value, entity_id)
                )
        db.conn.commit()
        
        return entity_id
    
    # 4. Test scenarios
    print("\n" + "=" * 60)
    print("🎯 Scenario 1: Places with ORG + GPE (triggers enrichment)")
    print("=" * 60)
    
    # Manually created features (simulating NLP extraction)
    entity_1 = process_item(
        "Dinner at Starbucks NYC",
        {"ORG": "Starbucks", "GPE": "NYC"}
    )
    
    entity_2 = process_item(
        "Coffee at Starbucks New York",
        {"ORG": "Starbucks", "GPE": "New York"}
    )
    
    print("\n" + "=" * 60)
    print("🎯 Scenario 2: Person without location (no enrichment)")
    print("=" * 60)
    
    entity_3 = process_item(
        "Meeting with John Smith",
        {"PERSON": "John Smith"}
    )
    
    print("\n" + "=" * 60)
    print("🎯 Scenario 3: Organization with location (triggers enrichment)")
    print("=" * 60)
    
    entity_4 = process_item(
        "Microsoft Seattle campus",
        {"ORG": "Microsoft", "GPE": "Seattle"}
    )
    
    # 5. Summary
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)
    
    entity_count = db.conn.execute(
        "SELECT COUNT(DISTINCT entity_id) FROM entity_index"
    ).fetchone()[0]
    attr_count = db.conn.execute(
        "SELECT COUNT(*) FROM entity_index"
    ).fetchone()[0]
    
    print(f"\nTotal entities created: {entity_count}")
    print(f"Total attributes indexed: {attr_count}")
    
    print("\n✨ Key Observations:")
    print("• Enrichment only runs when required features are present")
    print("• Google Maps enricher adds MAPS_PLACE_ID with weight 1.0")
    print("• Feature-triggered execution prevents unnecessary API calls")
    print("• System is modular - easily add new enrichers")
    
    print("\n📚 See README.md for full documentation")
    print("💻 Run test_enrichment.py for comprehensive tests")


if __name__ == "__main__":
    main()
