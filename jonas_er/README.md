# Jonas-ER: Personal Entity Resolution Engine

## 🎯 Objective

A privacy-first, local-only system to link personal data (CSV, Photos, Emails) into a self-healing Knowledge Graph using Jeff Jonas's Entity-Centric principles.

## 🛠 Tech Stack

- **Engine**: Python 3.x
- **Storage**: SQLite (Row-based for point-lookups)
- **NLP**: spaCy (Transformer-based NER)
- **Integrity**: SHA-256 Content Hashing

## 🧠 Core Principles

- **Provenance**: Every piece of data is linked to its original source file.
- **Idempotency**: Using content hashes, the system ignores duplicate records automatically.
- **Sequence Neutrality**: It doesn't matter what order you import data; the final graph "heals" to the same state.
- **Weighted Resolution**: Matches are determined by the cumulative "uniqueness" (entropy) of shared attributes.

## 📂 Project Structure

```
jonas_er/
├── data/               # SQLite DB storage
├── src/
│   ├── __init__.py
│   ├── database.py     # SQLite connection & schema
│   ├── engine.py       # Core Jonas resolution logic
│   ├── extractors.py   # spaCy & Regex logic
│   └── models.py       # Pydantic models for data validation
├── main.py             # Entry point
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### Install Dependencies

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

For better accuracy, install the transformer-based model:

```bash
python -m spacy download en_core_web_trf
```

### Run Ingestion

```python
from src.database import Database
from src.engine import ResolutionEngine
from src.extractors import FeatureExtractor

# Initialize components
db = Database()
extractor = FeatureExtractor()
engine = ResolutionEngine(db)

# Process text and extract features
text = "John Smith works at Microsoft in Seattle"
features = extractor.extract_features(text)

# Resolve entity
entity_id = engine.resolve(features)
print(f"Entity ID: {entity_id}")
```

### Run the Demo

```bash
cd jonas_er
python main.py
```

## 📚 Module Documentation

### src/database.py (The Ledger)

Manages SQLite database connections and schema:

- **sources**: Tracks original data files
- **observations**: Stores individual records with content hashing
- **entity_index**: Fast lookups for entity attributes

### src/extractors.py (The Sifter)

Extracts features using NLP:

- Uses spaCy for Named Entity Recognition (NER)
- Generates SHA-256 hashes for content deduplication
- Falls back to `en_core_web_sm` if transformer model unavailable

### src/engine.py (The Brain)

Core resolution logic:

- Implements weighted matching based on attribute uniqueness
- Higher weights for more unique attributes (EMAIL: 0.9, PHONE: 0.8)
- Merges entities when confidence score >= 0.9

### src/models.py

Pydantic models for data validation:

- `Source`: Represents a data source file
- `Observation`: Individual data records
- `EntityAttribute`: Entity attributes for indexing
- `Features`: Extracted feature sets

## 🔧 Configuration

### Attribute Weights

The resolution engine uses weighted scoring for different attribute types. You can customize these in `src/engine.py`:

```python
self.weights = {
    "PERSON": 0.4,
    "ORG": 0.5,
    "GPE": 0.3,
    "EMAIL": 0.9,
    "PHONE": 0.8
}
```

### Database Location

By default, the SQLite database is stored in `data/knowledge.db`. You can customize this:

```python
db = Database(db_path="path/to/your/database.db")
```

## 🎓 Why This Is "Pythonic"

- **Modular**: You can swap `extractors.py` for an LLM (Gemma/Phi) without touching the database logic.
- **Declarative Schema**: The SQL is handled centrally in a Database class.
- **Context Management**: It uses `sqlite3.Row` for dictionary-like access to database results.
- **Type Safety**: Pydantic models ensure data validation.

## 🔍 Example Use Cases

1. **Personal Knowledge Management**: Link notes, emails, and documents about the same people/organizations
2. **Contact Deduplication**: Merge duplicate contacts from multiple sources
3. **Research Data Integration**: Combine information from various research sources
4. **Privacy-First CRM**: Build a local customer/contact database without cloud dependencies

## 🛣️ Future Enhancements

- Add a visualizer using NetworkX to plot the Entity Graph
- Support for image metadata extraction (EXIF data)
- CSV import/export utilities
- Email parser integration
- Configurable resolution thresholds
- REST API for integration with other tools

## 📄 License

This project is open source and available for personal and commercial use.

## 🙏 Acknowledgments

Based on the entity resolution principles developed by Jeff Jonas, emphasizing:
- Context accumulation
- Sequence neutrality
- Re-identification
- Anonymity protection through local processing

---

**Remember**: Your data stays local. No cloud. No tracking. Just pure Python. 🐍
