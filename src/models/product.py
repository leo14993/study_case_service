from sqlalchemy import (JSON, Column, String, ForeignKey)
from sqlalchemy.dialects.postgresql import TIMESTAMP

from src.infrastructure.database.sql_alchemy import SqlBase


class Product(SqlBase):
    __tablename__ = 'products'

    id = Column(String(255), primary_key=True)
    information_id = Column(String(255), ForeignKey("information.id"))
    user_id = Column(String(255), nullable=False)
    product = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP(precision=0), nullable=False)

