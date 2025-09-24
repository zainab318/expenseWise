"""
Authentication module for ExpenseWise
Handles user login, registration, and session management
"""

import streamlit as st
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional, Dict
from database import Database

class AuthManager:
    def __init__(self):
        self.db = Database()
        self.session_timeout = 24 * 60 * 60  # 24 hours in seconds
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def generate_session_token(self) -> str:
        """Generate a secure session token"""
        return secrets.token_urlsafe(32)
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        return 'user' in st.session_state and 'session_token' in st.session_state
    
    def get_current_user(self) -> Optional[Dict]:
        """Get current logged-in user"""
        if self.is_logged_in():
            return st.session_state.user
        return None
    
    def login(self, username: str, password: str) -> bool:
        """Authenticate user login"""
        user = self.db.authenticate_user(username, password)
        
        if user:
            # Create session
            st.session_state.user = user
            st.session_state.session_token = self.generate_session_token()
            st.session_state.login_time = datetime.now()
            
            # Store session in database (simplified)
            st.session_state.session_data = {
                'user_id': user['id'],
                'token': st.session_state.session_token,
                'created_at': datetime.now().isoformat()
            }
            
            return True
        
        return False
    
    def register(self, username: str, email: str, password: str, full_name: str = None) -> bool:
        """Register a new user"""
        # Validate input
        if not username or not email or not password:
            return False
        
        if len(password) < 6:
            st.error("Password must be at least 6 characters long")
            return False
        
        # Check if username or email already exists
        # This is a simplified check - in production, you'd query the database
        try:
            user_id = self.db.create_user(username, email, password, full_name)
            return user_id is not None
        except Exception as e:
            st.error(f"Registration failed: {str(e)}")
            return False
    
    def logout(self):
        """Logout current user"""
        if 'user' in st.session_state:
            del st.session_state.user
        if 'session_token' in st.session_state:
            del st.session_state.session_token
        if 'login_time' in st.session_state:
            del st.session_state.login_time
        if 'session_data' in st.session_state:
            del st.session_state.session_data
    
    def check_session_timeout(self) -> bool:
        """Check if session has timed out"""
        if not self.is_logged_in():
            return False
        
        login_time = st.session_state.get('login_time')
        if not login_time:
            return False
        
        time_diff = datetime.now() - login_time
        return time_diff.total_seconds() < self.session_timeout
    
    def require_auth(self, func):
        """Decorator to require authentication for a function"""
        def wrapper(*args, **kwargs):
            if not self.is_logged_in():
                st.error("Please log in to access this feature")
                st.stop()
            
            if not self.check_session_timeout():
                st.error("Session expired. Please log in again")
                self.logout()
                st.stop()
            
            return func(*args, **kwargs)
        return wrapper
    
    def show_login_form(self):
        """Display login form"""
        st.markdown("### 🔐 Login")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col1, col2 = st.columns(2)
            with col1:
                login_clicked = st.form_submit_button("🚀 Login", type="primary")
            with col2:
                register_clicked = st.form_submit_button("📝 Register")
            
            if login_clicked:
                if username and password:
                    if self.login(username, password):
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password")
                else:
                    st.error("Please enter both username and password")
            
            if register_clicked:
                st.session_state.show_register = True
                st.rerun()
    
    def show_register_form(self):
        """Display registration form"""
        st.markdown("### 📝 Create Account")
        
        with st.form("register_form"):
            username = st.text_input("Username", placeholder="Choose a username")
            email = st.text_input("Email", placeholder="Enter your email")
            full_name = st.text_input("Full Name", placeholder="Enter your full name")
            password = st.text_input("Password", type="password", placeholder="Choose a password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password")
            
            col1, col2 = st.columns(2)
            with col1:
                register_clicked = st.form_submit_button("📝 Register", type="primary")
            with col2:
                back_clicked = st.form_submit_button("← Back to Login")
            
            if register_clicked:
                if not all([username, email, password, confirm_password]):
                    st.error("Please fill in all required fields")
                elif password.strip() != confirm_password.strip():
                    st.error("Passwords do not match")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters long")
                else:
                    if self.register(username, email, password, full_name):
                        st.success("✅ Registration successful! Please log in.")
                        st.session_state.show_register = False
                        st.rerun()
                    else:
                        st.error("❌ Registration failed. Username or email may already exist.")
            
            if back_clicked:
                st.session_state.show_register = False
                st.rerun()
    
    def show_auth_page(self):
        """Show authentication page"""
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h1 style="color: #667eea;">💰 ExpenseWise</h1>
            <p style="color: #666; font-size: 1.2rem;">Smart Expense Management & Receipt Processing</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Check if user wants to register
        if st.session_state.get('show_register', False):
            self.show_register_form()
        else:
            self.show_login_form()
        
        # Show features preview
        st.markdown("---")
        st.markdown("### ✨ Features")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **💰 Expense Tracking**
            - Add and manage expenses
            - Automatic categorization
            - Receipt scanning
            """)
        
        with col2:
            st.markdown("""
            **📄 Document Processing**
            - OCR text extraction
            - AI-powered analysis
            - File upload & storage
            """)
        
        with col3:
            st.markdown("""
            **📊 Analytics**
            - Spending insights
            - Interactive charts
            - Export capabilities
            """)
    
    def get_user_teams(self) -> list:
        """Get teams for current user"""
        if not self.is_logged_in():
            return []
        
        user_id = st.session_state.user['id']
        return self.db.get_user_teams(user_id)
    
    def create_team(self, name: str, description: str = None) -> bool:
        """Create a new team"""
        if not self.is_logged_in():
            return False
        
        user_id = st.session_state.user['id']
        team_id = self.db.create_team(name, description, user_id)
        return team_id is not None
    
    def add_team_member(self, team_id: int, user_id: int, role: str = 'member') -> bool:
        """Add member to team"""
        return self.db.add_team_member(team_id, user_id, role)
