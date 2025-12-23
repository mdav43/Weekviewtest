"""
Jonas-ER Main Entry Point

Example usage of the Jonas-ER entity resolution system.
"""

from src.database import Database
from src.engine import ResolutionEngine
from src.extractors import FeatureExtractor


def main():
    """
    Main entry point for Jonas-ER demonstration.
    """
    print("🧠 Jonas-ER: Personal Entity Resolution Engine")
    print("=" * 50)
    
    # Initialize components
    print("\n1. Initializing database...")
    db = Database()
    
    print("2. Loading NLP models...")
    extractor = FeatureExtractor()
    
    print("3. Initializing resolution engine...")
    engine = ResolutionEngine(db)
    
    print("\n✅ System initialized successfully!")
    print("\nExample usage:")
    print("  from src.database import Database")
    print("  from src.engine import ResolutionEngine")
    print("  from src.extractors import FeatureExtractor")
    print("\n  db = Database()")
    print("  extractor = FeatureExtractor()")
    print("  engine = ResolutionEngine(db)")
    print("\n  # Extract features from text")
    print('  text = "John Smith works at Microsoft in Seattle"')
    print("  features = extractor.extract_features(text)")
    print("\n  # Resolve entity")
    print("  entity_id = engine.resolve(features)")
    print("\n📚 See README.md for more information.")


if __name__ == "__main__":
    main()