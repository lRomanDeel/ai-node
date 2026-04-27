"""
PostgreSQL Storage Client

Responsibilities:
- connect to PostgreSQL
- store documents
- store chunks
"""

import uuid
import psycopg2
from typing import List


class PostgresStorage:
    """
    PostgreSQL storage wrapper
    """

    def __init__(
        self,
        host: str = "localhost",
        port: int = 5432,
        database: str = "ai_media",
        user: str = "ai_user",
        password: str = "Support01!"
    ):
        """
        Initialize connection
        """

        self.conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=database,
            user=user,
            password=password
        )

        self.conn.autocommit = True

    # ------------------------------------------------------------------
    # CREATE DOCUMENT
    # ------------------------------------------------------------------
    def create_document(self, source: str, content: str) -> str:
        """
        Insert document and return ID
        """

        doc_id = str(uuid.uuid4())

        with self.conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO documents (id, source, content)
                VALUES (%s, %s, %s)
                """,
                (doc_id, source, content)
            )

        return doc_id

    # ------------------------------------------------------------------
    # CREATE CHUNKS
    # ------------------------------------------------------------------
    def create_chunks(self, document_id: str, chunks: List[str]) -> List[str]:
        """
        Insert chunks and return their IDs
        """

        chunk_ids = []

        with self.conn.cursor() as cursor:
            for i, chunk in enumerate(chunks):
                chunk_id = str(uuid.uuid4())
                chunk_ids.append(chunk_id)

                cursor.execute(
                    """
                    INSERT INTO chunks (id, document_id, chunk_index, text)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (chunk_id, document_id, i, chunk)
                )

        return chunk_ids
