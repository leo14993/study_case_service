from sqlalchemy import (
    JSON,
    Float,
    Column,
    String,
    Boolean,
    Integer,
    text
)
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship

from src.infrastructure.database.sql_alchemy import SqlBase


class Information(SqlBase):
    __tablename__ = 'information'

    id = Column(String(255), primary_key=True)
    consumer = Column(JSON, nullable=False)
    partners = Column(JSON, nullable=False)
    offers = Column(JSON)
    client = Column(String(255), nullable=False)
    value = Column(Float(53))
    adjusted = Column(Boolean)
    products = Column(JSON)
    new_products_table = relationship("Product")
    created_at = Column(TIMESTAMP(precision=0), nullable=False)
    updated_at = Column(TIMESTAMP(precision=0), server_default=text("NULL::timestamp without time zone"))


