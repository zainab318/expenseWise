"""
Database module for ExpenseWise
Uses SQLite for easy deployment and free hosting compatibility
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import hashlib
import secrets

class Database:
    def __init__(self, db_path: str = "multitools.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT,
                role TEXT DEFAULT 'user',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Expenses table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                title TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                date DATE NOT NULL,
                receipt_path TEXT,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Files table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_type TEXT NOT NULL,
                file_size INTEGER,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed BOOLEAN DEFAULT 0,
                extracted_data TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Teams table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                created_by INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (created_by) REFERENCES users (id)
            )
        ''')
        
        # Team members table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS team_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                team_id INTEGER,
                user_id INTEGER,
                role TEXT DEFAULT 'member',
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (team_id) REFERENCES teams (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Settings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                setting_key TEXT NOT NULL,
                setting_value TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username: str, email: str, password: str, full_name: str = None) -> int:
        """Create a new user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        
        try:
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, full_name)
                VALUES (?, ?, ?, ?)
            ''', (username, email, password_hash, full_name))
            
            user_id = cursor.lastrowid
            conn.commit()
            return user_id
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        """Authenticate user login"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        password_hash = self.hash_password(password)
        
        cursor.execute('''
            SELECT id, username, email, full_name, role
            FROM users 
            WHERE username = ? AND password_hash = ? AND is_active = 1
        ''', (username, password_hash))
        
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                'id': user[0],
                'username': user[1],
                'email': user[2],
                'full_name': user[3],
                'role': user[4]
            }
        return None
    
    def add_expense(self, user_id: int, title: str, amount: float, category: str, 
                   description: str = None, date: str = None, receipt_path: str = None) -> int:
        """Add a new expense"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute('''
            INSERT INTO expenses (user_id, title, amount, category, description, date, receipt_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, title, amount, category, description, date, receipt_path))
        
        expense_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return expense_id
    
    def get_expenses(self, user_id: int, limit: int = 100) -> List[Dict]:
        """Get user expenses"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, title, amount, category, description, date, receipt_path, status, created_at
            FROM expenses 
            WHERE user_id = ?
            ORDER BY date DESC, created_at DESC
            LIMIT ?
        ''', (user_id, limit))
        
        expenses = []
        for row in cursor.fetchall():
            expenses.append({
                'id': row[0],
                'title': row[1],
                'amount': row[2],
                'category': row[3],
                'description': row[4],
                'date': row[5],
                'receipt_path': row[6],
                'status': row[7],
                'created_at': row[8]
            })
        
        conn.close()
        return expenses
    
    def update_expense(self, expense_id: int, **kwargs) -> bool:
        """Update an expense"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Build dynamic update query
        set_clauses = []
        values = []
        
        for key, value in kwargs.items():
            if key in ['title', 'amount', 'category', 'description', 'date', 'status']:
                set_clauses.append(f"{key} = ?")
                values.append(value)
        
        if not set_clauses:
            return False
        
        set_clauses.append("updated_at = ?")
        values.append(datetime.now().isoformat())
        values.append(expense_id)
        
        query = f"UPDATE expenses SET {', '.join(set_clauses)} WHERE id = ?"
        
        cursor.execute(query, values)
        conn.commit()
        conn.close()
        
        return cursor.rowcount > 0
    
    def delete_expense(self, expense_id: int, user_id: int) -> bool:
        """Delete an expense"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM expenses WHERE id = ? AND user_id = ?', (expense_id, user_id))
        conn.commit()
        conn.close()
        
        return cursor.rowcount > 0
    
    def add_file(self, user_id: int, filename: str, file_path: str, file_type: str, 
                 file_size: int, extracted_data: str = None) -> int:
        """Add a new file"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO files (user_id, filename, file_path, file_type, file_size, extracted_data)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, filename, file_path, file_type, file_size, extracted_data))
        
        file_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return file_id
    
    def get_files(self, user_id: int) -> List[Dict]:
        """Get user files"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, filename, file_type, file_size, upload_date, processed, extracted_data
            FROM files 
            WHERE user_id = ?
            ORDER BY upload_date DESC
        ''', (user_id,))
        
        files = []
        for row in cursor.fetchall():
            files.append({
                'id': row[0],
                'filename': row[1],
                'file_type': row[2],
                'file_size': row[3],
                'upload_date': row[4],
                'processed': bool(row[5]),
                'extracted_data': row[6]
            })
        
        conn.close()
        return files
    
    def get_expense_stats(self, user_id: int) -> Dict:
        """Get expense statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total expenses
        cursor.execute('SELECT SUM(amount) FROM expenses WHERE user_id = ?', (user_id,))
        total_amount = cursor.fetchone()[0] or 0
        
        # Count of expenses
        cursor.execute('SELECT COUNT(*) FROM expenses WHERE user_id = ?', (user_id,))
        expense_count = cursor.fetchone()[0]
        
        # Average expense
        avg_expense = total_amount / expense_count if expense_count > 0 else 0
        
        # Category breakdown
        cursor.execute('''
            SELECT category, SUM(amount), COUNT(*)
            FROM expenses 
            WHERE user_id = ?
            GROUP BY category
            ORDER BY SUM(amount) DESC
        ''', (user_id,))
        
        categories = []
        for row in cursor.fetchall():
            categories.append({
                'category': row[0],
                'amount': row[1],
                'count': row[2]
            })
        
        conn.close()
        
        return {
            'total_amount': total_amount,
            'expense_count': expense_count,
            'average_expense': avg_expense,
            'categories': categories
        }
    
    def create_team(self, name: str, description: str, created_by: int) -> int:
        """Create a new team"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO teams (name, description, created_by)
            VALUES (?, ?, ?)
        ''', (name, description, created_by))
        
        team_id = cursor.lastrowid
        
        # Add creator as admin
        cursor.execute('''
            INSERT INTO team_members (team_id, user_id, role)
            VALUES (?, ?, ?)
        ''', (team_id, created_by, 'admin'))
        
        conn.commit()
        conn.close()
        
        return team_id
    
    def add_team_member(self, team_id: int, user_id: int, role: str = 'member') -> bool:
        """Add member to team"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO team_members (team_id, user_id, role)
                VALUES (?, ?, ?)
            ''', (team_id, user_id, role))
            
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_user_teams(self, user_id: int) -> List[Dict]:
        """Get teams for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT t.id, t.name, t.description, tm.role, t.created_at
            FROM teams t
            JOIN team_members tm ON t.id = tm.team_id
            WHERE tm.user_id = ?
            ORDER BY t.created_at DESC
        ''', (user_id,))
        
        teams = []
        for row in cursor.fetchall():
            teams.append({
                'id': row[0],
                'name': row[1],
                'description': row[2],
                'role': row[3],
                'created_at': row[4]
            })
        
        conn.close()
        return teams
