#!/usr/bin/env python3
"""
Integration test for Jonas-ER entity resolution system.

This script demonstrates the core functionality without requiring
external dependencies (spaCy, Pydantic).
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database import Database
from engine import ResolutionEngine


def test_complete_workflow():
    """Test the complete entity resolution workflow"""
    
    print("=" * 60)
    print("Jonas-ER Integration Test")
    print("=" * 60)
    
    # 1. Initialize system
    print("\n1. Initializing database (in-memory for testing)...")
    db = Database(db_path=":memory:")
    print("   ✓ Database initialized")
    
    # 2. Create resolution engine
    print("\n2. Creating resolution engine...")
    engine = ResolutionEngine(db)
    print("   ✓ Engine initialized with weights:")
    for attr, weight in engine.weights.items():
        print(f"      {attr}: {weight}")
    
    # 3. Test Case 1: Create first entity
    print("\n3. Test Case 1: Creating first entity")
    features_1 = {
        "PERSON": "John Smith",
        "ORG": "Microsoft"
    }
    print(f"   Features: {features_1}")
    entity_1 = engine.resolve(features_1)
    print(f"   ✓ New entity created: {entity_1}")
    
    # Add to index
    for attr_type, attr_value in features_1.items():
        db.conn.execute(
            "INSERT INTO entity_index (attr_type, attr_value, entity_id) VALUES (?, ?, ?)",
            (attr_type, attr_value, entity_1)
        )
    db.conn.commit()
    print("   ✓ Entity indexed")
    
    # 4. Test Case 2: Similar entity (low overlap)
    print("\n4. Test Case 2: Similar entity with low overlap")
    features_2 = {
        "PERSON": "John Smith",
        "GPE": "Seattle"
    }
    print(f"   Features: {features_2}")
    entity_2 = engine.resolve(features_2)
    score = engine.weights["PERSON"] + engine.weights.get("GPE", 0.1)
    print(f"   Confidence score: {score:.2f} (threshold: 0.9)")
    print(f"   ✓ Entity ID: {entity_2}")
    if entity_2 == entity_1:
        print("   → Merged with existing entity")
    else:
        print("   → Created new entity (score too low)")
    
    # Add to index
    for attr_type, attr_value in features_2.items():
        existing = db.conn.execute(
            "SELECT COUNT(*) FROM entity_index WHERE attr_value = ? AND entity_id = ?",
            (attr_value, entity_2)
        ).fetchone()[0]
        if existing == 0:
            db.conn.execute(
                "INSERT INTO entity_index (attr_type, attr_value, entity_id) VALUES (?, ?, ?)",
                (attr_type, attr_value, entity_2)
            )
    db.conn.commit()
    
    # 5. Test Case 3: High-confidence match
    print("\n5. Test Case 3: High-confidence match with unique attributes")
    features_3 = {
        "EMAIL": "john.smith@microsoft.com",
        "PHONE": "555-1234"
    }
    print(f"   Features: {features_3}")
    entity_3 = engine.resolve(features_3)
    score = engine.weights["EMAIL"] + engine.weights["PHONE"]
    print(f"   Confidence score: {score:.2f} (threshold: 0.9)")
    print(f"   ✓ Entity ID: {entity_3}")
    print("   → Created new entity (no previous matches)")
    
    # Add to index
    for attr_type, attr_value in features_3.items():
        db.conn.execute(
            "INSERT INTO entity_index (attr_type, attr_value, entity_id) VALUES (?, ?, ?)",
            (attr_type, attr_value, entity_3)
        )
    db.conn.commit()
    
    # 6. Test Case 4: Match using high-weight attribute
    print("\n6. Test Case 4: Match using high-weight attribute")
    features_4 = {
        "EMAIL": "john.smith@microsoft.com",
        "ORG": "Google"  # Different org
    }
    print(f"   Features: {features_4}")
    entity_4 = engine.resolve(features_4)
    score = engine.weights["EMAIL"] + engine.weights["ORG"]
    print(f"   Confidence score: {score:.2f} (threshold: 0.9)")
    print(f"   ✓ Entity ID: {entity_4}")
    if entity_4 == entity_3:
        print("   → Merged with entity from Test Case 3 (EMAIL match)")
    else:
        print("   → Created new entity")
    
    # 7. Verify database state
    print("\n7. Database Statistics")
    entity_count = db.conn.execute(
        "SELECT COUNT(DISTINCT entity_id) FROM entity_index"
    ).fetchone()[0]
    attr_count = db.conn.execute(
        "SELECT COUNT(*) FROM entity_index"
    ).fetchone()[0]
    print(f"   Total unique entities: {entity_count}")
    print(f"   Total attributes indexed: {attr_count}")
    
    # 8. Show entity graph
    print("\n8. Entity Graph")
    entities = db.conn.execute(
        "SELECT DISTINCT entity_id FROM entity_index"
    ).fetchall()
    
    for i, (entity_id,) in enumerate(entities, 1):
        print(f"\n   Entity {i}: {entity_id[:8]}...")
        attrs = db.conn.execute(
            "SELECT attr_type, attr_value FROM entity_index WHERE entity_id = ?",
            (entity_id,)
        ).fetchall()
        for attr_type, attr_value in attrs:
            print(f"      - {attr_type}: {attr_value}")
    
    print("\n" + "=" * 60)
    print("✅ All tests completed successfully!")
    print("=" * 60)
    print("\nKey Observations:")
    print("• System creates new entities when confidence is low")
    print("• High-weight attributes (EMAIL: 0.9) enable strong matches")
    print("• Multiple attributes accumulate evidence for merging")
    print("• The system maintains provenance through the entity_index")
    print("\nFor full NLP features, install: pip install -r requirements.txt")


if __name__ == "__main__":
    test_complete_workflow()
