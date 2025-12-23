"""
Feature extraction module for Jonas-ER

Handles NLP-based feature extraction using spaCy and content hashing.
"""

import spacy
import hashlib
import json


class FeatureExtractor:
    def __init__(self):
        # Load spaCy (ensure 'en_core_web_trf' is installed for best accuracy)
        try:
            self.nlp = spacy.load("en_core_web_trf")
        except:
            self.nlp = spacy.load("en_core_web_sm")

    def extract_features(self, text):
        doc = self.nlp(text)
        features = {}
        for ent in doc.ents:
            features[ent.label_] = ent.text
        return features

    def compute_hash(self, data):
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
