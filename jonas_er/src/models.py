"""
Data models module for Jonas-ER

Defines Pydantic models for data validation across the entity resolution system.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime


class Source(BaseModel):
    """Represents a data source file"""
    id: str
    filename: str
    imported_at: Optional[datetime] = None


class Observation(BaseModel):
    """Represents a single observation from a source"""
    hash: str
    source_id: str
    entity_id: str
    raw_data: str


class EntityAttribute(BaseModel):
    """Represents an attribute of an entity"""
    attr_type: str
    attr_value: str
    entity_id: str


class Features(BaseModel):
    """Represents extracted features from text"""
    features: Dict[str, str] = Field(default_factory=dict)
