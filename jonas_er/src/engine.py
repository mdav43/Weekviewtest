"""
Resolution engine module for Jonas-ER

Implements the core entity resolution logic based on Jeff Jonas principles.
"""

import uuid


class ResolutionEngine:
    def __init__(self, db):
        self.db = db
        # Jeff Jonas Principles: Higher weight = more unique
        self.weights = {"PERSON": 0.4, "ORG": 0.5, "GPE": 0.3, "EMAIL": 0.9, "PHONE": 0.8}

    def resolve(self, features):
        candidate_scores = {}
        
        # Search for existing entities sharing these tethers
        for attr, val in features.items():
            query = "SELECT entity_id FROM entity_index WHERE attr_value = ?"
            rows = self.db.conn.execute(query, (val,)).fetchall()
            for row in rows:
                eid = row['entity_id']
                candidate_scores[eid] = candidate_scores.get(eid, 0) + self.weights.get(attr, 0.1)

        # Merge Decision
        if candidate_scores:
            best_eid = max(candidate_scores, key=candidate_scores.get)
            if candidate_scores[best_eid] >= 0.9:
                return best_eid
        
        return str(uuid.uuid4())  # New Entity
