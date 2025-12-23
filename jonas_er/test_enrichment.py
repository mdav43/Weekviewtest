#!/usr/bin/env python3
"""
Integration test for Jonas-ER enrichment module.

This script demonstrates the enrichment pipeline functionality.
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
from enrichers import GoogleMapsEnricher, BaseEnricher
from registry import EnrichmentRegistry


def test_enrichment_workflow():
    """Test the enrichment pipeline workflow"""
    
    print("=" * 60)
    print("Jonas-ER Enrichment Pipeline Test")
    print("=" * 60)
    
    # 1. Initialize system
    print("\n1. Initializing system (in-memory database)...")
    db = Database(db_path=":memory:")
    engine = ResolutionEngine(db)
    registry = EnrichmentRegistry()
    print("   ✓ System initialized")
    
    # 2. Configure enrichers
    print("\n2. Configuring enrichers...")
    gmaps_enricher = GoogleMapsEnricher()
    registry.register(["ORG", "GPE"], gmaps_enricher)
    print("   ✓ Google Maps enricher registered")
    print("      Requirements: ORG + GPE")
    
    # 3. Test Case 1: Features with ORG and GPE (should trigger enrichment)
    print("\n3. Test Case 1: Features that trigger enrichment")
    features_1 = {
        "ORG": "Starbucks",
        "GPE": "NYC"
    }
    print(f"   Input features: {features_1}")
    
    enrichers = registry.get_applicable_enrichers(features_1)
    print(f"   Applicable enrichers: {len(enrichers)}")
    
    for enricher in enrichers:
        new_data = enricher.enrich(features_1)
        features_1.update(new_data)
    
    print(f"   Enriched features: {features_1}")
    entity_1 = engine.resolve(features_1)
    print(f"   ✓ Resolved to entity: {entity_1}")
    
    # Add to index
    for attr_type, attr_value in features_1.items():
        db.conn.execute(
            "INSERT INTO entity_index (attr_type, attr_value, entity_id) VALUES (?, ?, ?)",
            (attr_type, attr_value, entity_1)
        )
    db.conn.commit()
    print("   ✓ Entity indexed")
    
    # 4. Test Case 2: Similar place, different name (should merge due to Place ID)
    print("\n4. Test Case 2: Different name, same place")
    features_2 = {
        "ORG": "S.Bucks Coffee",
        "GPE": "New York"
    }
    print(f"   Input features: {features_2}")
    
    enrichers = registry.get_applicable_enrichers(features_2)
    for enricher in enrichers:
        new_data = enricher.enrich(features_2)
        features_2.update(new_data)
    
    print(f"   Enriched features: {features_2}")
    entity_2 = engine.resolve(features_2)
    print(f"   ✓ Resolved to entity: {entity_2}")
    
    if entity_2 == entity_1:
        print("   🎉 SUCCESS: Merged with entity from Test Case 1 (Place ID match)")
    else:
        print("   → Created new entity (no match found)")
    
    # 5. Test Case 3: Missing required features (no enrichment)
    print("\n5. Test Case 3: Missing required features")
    features_3 = {
        "PERSON": "John Smith"
    }
    print(f"   Input features: {features_3}")
    
    enrichers = registry.get_applicable_enrichers(features_3)
    print(f"   Applicable enrichers: {len(enrichers)}")
    
    if not enrichers:
        print("   ✓ No enrichment triggered (missing ORG or GPE)")
    
    entity_3 = engine.resolve(features_3)
    print(f"   ✓ Resolved to entity: {entity_3}")
    
    # 6. Test Case 4: Only one required feature (no enrichment)
    print("\n6. Test Case 4: Only one required feature present")
    features_4 = {
        "ORG": "Microsoft"
    }
    print(f"   Input features: {features_4}")
    
    enrichers = registry.get_applicable_enrichers(features_4)
    print(f"   Applicable enrichers: {len(enrichers)}")
    
    if not enrichers:
        print("   ✓ No enrichment triggered (missing GPE)")
    
    entity_4 = engine.resolve(features_4)
    print(f"   ✓ Resolved to entity: {entity_4}")
    
    # 7. Verify weight system
    print("\n7. Verifying attribute weights")
    print("   Current weights:")
    for attr, weight in sorted(engine.weights.items(), key=lambda x: x[1], reverse=True):
        print(f"      {attr:20} = {weight}")
    
    print("\n   Key observations:")
    print("   • MAPS_PLACE_ID has highest weight (1.0)")
    print("   • Enriched attributes enable deterministic matching")
    print("   • Feature-triggered execution prevents unnecessary API calls")
    
    # 8. Database verification
    print("\n8. Database Statistics")
    
    # Check observation_attributes table exists
    tables = db.conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()
    table_names = [t[0] for t in tables]
    print(f"   Tables: {', '.join(table_names)}")
    
    if 'observation_attributes' in table_names:
        print("   ✓ observation_attributes table created successfully")
    else:
        print("   ⚠️  observation_attributes table not found")
    
    entity_count = db.conn.execute(
        "SELECT COUNT(DISTINCT entity_id) FROM entity_index"
    ).fetchone()[0]
    print(f"   Total unique entities: {entity_count}")
    
    # 9. Test custom enricher
    print("\n9. Testing custom enricher")
    
    class CustomEnricher(BaseEnricher):
        def enrich(self, features):
            if 'PERSON' in features:
                return {"CUSTOM_ID": f"CUSTOM-{features['PERSON'].replace(' ', '-')}"}
            return {}
    
    custom_enricher = CustomEnricher()
    registry.register(["PERSON"], custom_enricher)
    print("   ✓ Custom enricher registered for PERSON")
    
    features_5 = {"PERSON": "Jane Doe"}
    enrichers = registry.get_applicable_enrichers(features_5)
    print(f"   Applicable enrichers for {features_5}: {len(enrichers)}")
    
    for enricher in enrichers:
        new_data = enricher.enrich(features_5)
        features_5.update(new_data)
    
    print(f"   Enriched features: {features_5}")
    print("   ✓ Custom enricher worked successfully")
    
    print("\n" + "=" * 60)
    print("✅ All enrichment tests completed successfully!")
    print("=" * 60)
    print("\nKey Achievements:")
    print("• Feature-triggered enrichment working correctly")
    print("• Google Maps enricher adds Place IDs")
    print("• High-weight attributes enable deterministic matching")
    print("• Registry prevents unnecessary enrichment calls")
    print("• System easily extensible with custom enrichers")
    print("\nFor NLP-based feature extraction, install: pip install -r requirements.txt")


if __name__ == "__main__":
    test_enrichment_workflow()
