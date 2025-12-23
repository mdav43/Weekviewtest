"""
Database module for Jonas-ER

Handles SQLite connection and schema management for the entity resolution system.
"""

import sqlite3


class Database:
    def __init__(self, db_path="data/knowledge.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        self.conn.executescript('''
            CREATE TABLE IF NOT EXISTS sources (
                id TEXT PRIMARY KEY,
                filename TEXT,
                imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS observations (
                hash TEXT PRIMARY KEY,
                source_id TEXT,
                entity_id TEXT,
                raw_data TEXT,
                FOREIGN KEY(source_id) REFERENCES sources(id)
            );
            CREATE TABLE IF NOT EXISTS observation_attributes (
                obs_hash TEXT,
                attr_type TEXT,
                attr_value TEXT,
                FOREIGN KEY(obs_hash) REFERENCES observations(hash)
            );
            CREATE TABLE IF NOT EXISTS entity_index (
                attr_type TEXT,
                attr_value TEXT,
                entity_id TEXT
            );
            CREATE INDEX IF NOT EXISTS idx_features ON entity_index(attr_value);
        ''')
