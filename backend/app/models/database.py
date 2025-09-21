import sqlite3
from typing import List, Optional
from ..models.evidence import FactCheck
from ..config import DATABASE_URL
import json

class Database:
    def __init__(self):
        self.db_path = DATABASE_URL
        self.init_db()
    
    def init_db(self):
        """Initialize the database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create fact_checks table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fact_checks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                claim TEXT NOT NULL,
                verdict TEXT NOT NULL,
                explanation TEXT,
                source TEXT,
                source_url TEXT,
                date_published TEXT,
                embedding TEXT
            )
        ''')
        
        # Create analysis_cache table for caching results
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analysis_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                input_hash TEXT UNIQUE,
                result TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def insert_fact_check(self, fact_check: FactCheck) -> int:
        """Insert a fact check into the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        embedding_json = json.dumps(fact_check.embedding) if fact_check.embedding else None
        
        cursor.execute('''
            INSERT INTO fact_checks (claim, verdict, explanation, source, source_url, date_published, embedding)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            fact_check.claim,
            fact_check.verdict,
            fact_check.explanation,
            fact_check.source,
            fact_check.source_url,
            fact_check.date_published,
            embedding_json
        ))
        
        fact_check_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return fact_check_id
    
    def get_all_fact_checks(self) -> List[FactCheck]:
        """Get all fact checks from the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM fact_checks')
        rows = cursor.fetchall()
        conn.close()
        
        fact_checks = []
        for row in rows:
            embedding = json.loads(row[7]) if row[7] else None
            fact_check = FactCheck(
                id=row[0],
                claim=row[1],
                verdict=row[2],
                explanation=row[3],
                source=row[4],
                source_url=row[5],
                date_published=row[6],
                embedding=embedding
            )
            fact_checks.append(fact_check)
        
        return fact_checks
    
    def cache_analysis(self, input_hash: str, result: dict):
        """Cache analysis result"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        result_json = json.dumps(result)
        cursor.execute('''
            INSERT OR REPLACE INTO analysis_cache (input_hash, result)
            VALUES (?, ?)
        ''', (input_hash, result_json))
        
        conn.commit()
        conn.close()
    
    def get_cached_analysis(self, input_hash: str) -> Optional[dict]:
        """Get cached analysis result"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT result FROM analysis_cache WHERE input_hash = ?', (input_hash,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return json.loads(row[0])
        return None

# Global database instance
db = Database()