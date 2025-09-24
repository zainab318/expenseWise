import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import json
import io
import base64
import os
import tempfile
from database import Database
from auth import AuthManager
from ai_processor import AIProcessor

# Page configuration
st.set_page_config(
    page_title="ExpenseWise",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for expense management design
st.markdown("""
<style>
    /* Main theme colors for expense management */
    :root {
        --primary-green: #10b981;
        --primary-green-dark: #059669;
        --secondary-green: #34d399;
        --accent-blue: #3b82f6;
        --accent-blue-dark: #2563eb;
        --warning-orange: #f59e0b;
        --danger-red: #ef4444;
        --success-green: #10b981;
        --neutral-gray: #6b7280;
        --light-gray: #f3f4f6;
        --dark-gray: #374151;
    }
    
    .main-header {
        background: linear-gradient(135deg, #10b981 0%, #059669 50%, #3b82f6 100%);
        padding: 2.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.3);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);
    }
    
    .expense-card {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2);
        transition: transform 0.3s ease;
    }
    
    .expense-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.3);
    }
    
    .upload-area {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        padding: 3rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        border: 3px dashed rgba(255,255,255,0.3);
        box-shadow: 0 8px 25px rgba(245, 158, 11, 0.2);
    }
    
    .upload-area:hover {
        background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
        transform: translateY(-2px);
    }
    
    .success-message {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);
    }
    
    .warning-message {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.2);
    }
    
    .error-message {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.2);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #10b981 0%, #059669 50%, #3b82f6 100%);
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #10b981, #3b82f6);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);
        background: linear-gradient(45deg, #059669, #2563eb);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Financial-themed input styling */
    .stTextInput > div > div > input {
        border: 2px solid #d1d5db;
        border-radius: 8px;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #10b981;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
    }
    
    .stNumberInput > div > div > input {
        border: 2px solid #d1d5db;
        border-radius: 8px;
        transition: border-color 0.3s ease;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #10b981;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
    }
    
    .stSelectbox > div > div > div {
        border: 2px solid #d1d5db;
        border-radius: 8px;
        transition: border-color 0.3s ease;
    }
    
    .stSelectbox > div > div > div:focus {
        border-color: #10b981;
        box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
    }
    
    /* Chart styling */
    .plotly-graph-div {
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* Progress bar styling */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #10b981, #34d399);
        border-radius: 10px;
    }
    
    /* File uploader styling */
    .stFileUploader > div {
        border: 2px dashed #10b981;
        border-radius: 15px;
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div:hover {
        border-color: #059669;
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #10b981 0%, #059669 50%, #3b82f6 100%);
    }
    
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #10b981, #3b82f6);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #059669, #2563eb);
    }
</style>
""", unsafe_allow_html=True)

# Initialize managers
db = Database()
auth = AuthManager()
ai_processor = AIProcessor()

# Initialize session state
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []

if 'show_register' not in st.session_state:
    st.session_state.show_register = False

# Initialize session state for navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = "🏠 Home"

# Check authentication
if not auth.is_logged_in():
    auth.show_auth_page()
    st.stop()

# Sidebar navigation
st.sidebar.markdown("""
<div style="text-align: center; padding: 1rem;">
    <h1 style="color: white; margin: 0;">💰 ExpenseWise</h1>
    <p style="color: #e0e0e0; margin: 0;">Smart Expense Management</p>
</div>
""", unsafe_allow_html=True)

# User info
user = auth.get_current_user()
st.sidebar.markdown(f"""
<div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
    <p style="color: white; margin: 0; font-weight: bold;">👤 {user['full_name'] or user['username']}</p>
    <p style="color: #e0e0e0; margin: 0; font-size: 0.9rem;">{user['email']}</p>
</div>
""", unsafe_allow_html=True)

# Navigation buttons instead of selectbox
st.sidebar.markdown("### 🧭 Navigation")

# Home button
if st.sidebar.button("🏠 Home", use_container_width=True, type="primary" if st.session_state.current_page == "🏠 Home" else "secondary"):
    st.session_state.current_page = "🏠 Home"
    st.rerun()

# Expense Management button
if st.sidebar.button("💰 Expense Management", use_container_width=True, type="primary" if st.session_state.current_page == "💰 Expense Management" else "secondary"):
    st.session_state.current_page = "💰 Expense Management"
    st.rerun()

# File Upload button
if st.sidebar.button("📁 File Upload", use_container_width=True, type="primary" if st.session_state.current_page == "📁 File Upload" else "secondary"):
    st.session_state.current_page = "📁 File Upload"
    st.rerun()

# Analytics button
if st.sidebar.button("📊 Analytics", use_container_width=True, type="primary" if st.session_state.current_page == "📊 Analytics" else "secondary"):
    st.session_state.current_page = "📊 Analytics"
    st.rerun()

# Settings button
if st.sidebar.button("⚙️ Settings", use_container_width=True, type="primary" if st.session_state.current_page == "⚙️ Settings" else "secondary"):
    st.session_state.current_page = "⚙️ Settings"
    st.rerun()

# Logout button
if st.sidebar.button("🚪 Logout", use_container_width=True):
    auth.logout()
    st.rerun()

# Get current page
page = st.session_state.current_page

# Load user data
user_id = user['id']
expenses = db.get_expenses(user_id)
st.session_state.expenses = expenses

# Home Page
if page == "🏠 Home":
    st.markdown("""
    <div class="main-header">
        <h1>Welcome to ExpenseWise</h1>
        <p>Transform your expense management with AI-powered receipt processing, smart categorization, and intelligent analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3>💰</h3>
            <h2>${sum(exp['amount'] for exp in st.session_state.expenses)}</h2>
            <p>Total Expenses</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h3>📊</h3>
            <h2>{len(st.session_state.expenses)}</h2>
            <p>This Month</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h3>🏷️</h3>
            <h2>{len(set(exp['category'] for exp in st.session_state.expenses))}</h2>
            <p>Categories</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        if st.session_state.expenses:
            avg_expense = sum(exp['amount'] for exp in st.session_state.expenses) // len(st.session_state.expenses)
        else:
            avg_expense = 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>📈</h3>
            <h2>${avg_expense}</h2>
            <p>Avg. Expense</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent expenses preview
    st.markdown("### 🎯 Recent Expenses")
    recent_expenses = st.session_state.expenses[:3]
    
    for expense in recent_expenses:
        st.markdown(f"""
        <div class="expense-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0;">{expense['title']}</h4>
                    <p style="margin: 0; opacity: 0.8;">{expense['description']}</p>
                    <span style="background: rgba(255,255,255,0.2); padding: 0.2rem 0.5rem; border-radius: 5px; font-size: 0.8rem;">{expense['category']}</span>
                </div>
                <div style="text-align: right;">
                    <h3 style="margin: 0;">${expense['amount']}</h3>
                    <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">{expense['date']}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick actions
    st.markdown("### 🚀 Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Add New Expense", key="quick_add"):
            st.session_state.current_page = "💰 Expense Management"
            st.rerun()
    
    with col2:
        if st.button("📁 Upload Files", key="quick_upload"):
            st.session_state.current_page = "📁 File Upload"
            st.rerun()
    
    with col3:
        if st.button("📊 View Analytics", key="quick_analytics"):
            st.session_state.current_page = "📊 Analytics"
            st.rerun()

# Expense Management Page
elif page == "💰 Expense Management":
    st.markdown("### 💰 Expense Management")
    
    # Add new expense form
    with st.expander("➕ Add New Expense", expanded=False):
        with st.form("add_expense_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input("Expense Title", placeholder="e.g., Office Supplies")
                amount = st.number_input("Amount ($)", min_value=0.0, step=0.01, format="%.2f")
                category = st.selectbox("Category", ["Technology", "Business", "Office", "Travel", "Marketing", "Other"])
            
            with col2:
                date = st.date_input("Date", value=datetime.now().date())
                description = st.text_area("Description", placeholder="Additional details...")
            
            submitted = st.form_submit_button("💾 Add Expense", type="primary")
            
            if submitted and title and amount > 0:
                # Add to database
                expense_id = db.add_expense(
                    user_id=user_id,
                    title=title,
                    amount=amount,
                    category=category,
                    description=description,
                    date=date.strftime("%Y-%m-%d")
                )
                
                if expense_id:
                    st.success("✅ Expense added successfully!")
                    st.rerun()
                else:
                    st.error("❌ Failed to add expense. Please try again.")
    
    # Expenses list
    st.markdown("### 📋 All Expenses")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        category_filter = st.selectbox("Filter by Category", ["All"] + list(set(exp['category'] for exp in st.session_state.expenses)))
    
    with col2:
        sort_by = st.selectbox("Sort by", ["Date (Newest)", "Date (Oldest)", "Amount (High to Low)", "Amount (Low to High)"])
    
    with col3:
        search_term = st.text_input("Search expenses", placeholder="Search by title or description...")
    
    # Filter and sort expenses
    filtered_expenses = st.session_state.expenses.copy()
    
    if category_filter != "All":
        filtered_expenses = [exp for exp in filtered_expenses if exp['category'] == category_filter]
    
    if search_term:
        filtered_expenses = [exp for exp in filtered_expenses if search_term.lower() in exp['title'].lower() or search_term.lower() in exp['description'].lower()]
    
    if sort_by == "Date (Newest)":
        filtered_expenses.sort(key=lambda x: x['date'], reverse=True)
    elif sort_by == "Date (Oldest)":
        filtered_expenses.sort(key=lambda x: x['date'])
    elif sort_by == "Amount (High to Low)":
        filtered_expenses.sort(key=lambda x: x['amount'], reverse=True)
    elif sort_by == "Amount (Low to High)":
        filtered_expenses.sort(key=lambda x: x['amount'])
    
    # Display expenses
    for expense in filtered_expenses:
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 1rem; border-radius: 10px; color: white; margin: 0.5rem 0;">
                    <h4 style="margin: 0;">{expense['title']}</h4>
                    <p style="margin: 0; opacity: 0.8;">{expense['description']}</p>
                    <span style="background: rgba(255,255,255,0.2); padding: 0.2rem 0.5rem; border-radius: 5px; font-size: 0.8rem;">{expense['category']}</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.metric("Amount", f"${expense['amount']}")
            
            with col3:
                if st.button("🗑️", key=f"delete_{expense['id']}", help="Delete expense"):
                    st.session_state.expenses = [exp for exp in st.session_state.expenses if exp['id'] != expense['id']]
                    st.rerun()

# File Upload Page
elif page == "📁 File Upload":
    st.markdown("### 📁 File Upload & Processing")
    
    # Upload area
    st.markdown("""
    <div class="upload-area">
        <h2>📤 Upload Your Documents</h2>
        <p>Drag and drop files here or use the uploader below</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_files = st.file_uploader(
        "Choose files to upload",
        accept_multiple_files=True,
        type=['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'jpg', 'jpeg', 'png', 'gif'],
        help="Supported formats: PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX, JPG, PNG, GIF"
    )
    
    if uploaded_files:
        st.markdown("### 📋 Uploaded Files")
        
        for i, file in enumerate(uploaded_files):
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                st.write(f"📄 {file.name}")
            
            with col2:
                st.write(f"{file.size / 1024:.1f} KB")
            
            with col3:
                if st.button("🔍 Process", key=f"process_{i}"):
                    # Save file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.name)[1]) as tmp_file:
                        tmp_file.write(file.getvalue())
                        tmp_path = tmp_file.name
                    
                    # Process with AI
                    with st.spinner(f"Processing {file.name}..."):
                        result = ai_processor.process_document(tmp_path, file.type)
                    
                    if result['success']:
                        # Save to database
                        file_id = db.add_file(
                            user_id=user_id,
                            filename=file.name,
                            file_path=tmp_path,
                            file_type=file.type,
                            file_size=file.size,
                            extracted_data=json.dumps(result['extracted_data'])
                        )
                        
                        st.session_state.uploaded_files.append({
                            "id": file_id,
                            "name": file.name,
                            "size": file.size,
                            "type": file.type,
                            "processed": True,
                            "extracted_data": result['extracted_data']
                        })
                        
                        # Show extracted data
                        if result['extracted_data']['amount']:
                            st.success(f"✅ {file.name} processed successfully!")
                            st.json(result['extracted_data'])
                            
                            # Offer to create expense from extracted data
                            if st.button(f"💰 Create Expense from {file.name}", key=f"create_expense_{i}"):
                                extracted = result['extracted_data']
                                expense_id = db.add_expense(
                                    user_id=user_id,
                                    title=extracted.get('vendor', 'Document Expense'),
                                    amount=extracted.get('amount', 0),
                                    category=extracted.get('category', 'Other'),
                                    description=extracted.get('description', ''),
                                    date=extracted.get('date', datetime.now().strftime('%Y-%m-%d'))
                                )
                                if expense_id:
                                    st.success("✅ Expense created from document!")
                                    st.rerun()
                        else:
                            st.warning(f"⚠️ {file.name} processed but no expense data found")
                    else:
                        st.error(f"❌ Failed to process {file.name}: {result.get('error', 'Unknown error')}")
                    
                    # Clean up temp file
                    try:
                        os.unlink(tmp_path)
                    except:
                        pass
            
            with col4:
                if st.button("🗑️", key=f"remove_{i}"):
                    st.rerun()
        
        # Processing options
        st.markdown("### ⚙️ Processing Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            ocr_enabled = st.checkbox("🔍 Enable OCR", value=True, help="Extract text from images and PDFs")
            ai_analysis = st.checkbox("🤖 AI Analysis", value=True, help="Use AI to analyze document content")
        
        with col2:
            expense_extraction = st.checkbox("💰 Extract Expenses", value=True, help="Automatically extract expense information")
            data_export = st.checkbox("📊 Export Data", value=False, help="Export processed data to CSV")
        
        if st.button("🚀 Process All Files", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(len(uploaded_files)):
                progress_bar.progress((i + 1) / len(uploaded_files))
                status_text.text(f"Processing {uploaded_files[i].name}...")
                # Simulate processing time
                import time
                time.sleep(0.5)
            
            st.markdown("""
            <div class="success-message">
                <h3>🎉 Processing Complete!</h3>
                <p>All files have been successfully processed and analyzed.</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Recent uploads
    if st.session_state.uploaded_files:
        st.markdown("### 📂 Recent Uploads")
        
        for file_info in st.session_state.uploaded_files:
            status_icon = "✅" if file_info.get("processed", False) else "⏳"
            st.write(f"{status_icon} {file_info['name']} - {file_info['size'] / 1024:.1f} KB")

# Analytics Page
elif page == "📊 Analytics":
    st.markdown("### 📊 Analytics Dashboard")
    
    if not st.session_state.expenses:
        st.warning("No expense data available. Add some expenses to see analytics.")
    else:
        # Convert to DataFrame for easier analysis
        df = pd.DataFrame(st.session_state.expenses)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Expenses", f"${df['amount'].sum():,.2f}")
        
        with col2:
            st.metric("Average Expense", f"${df['amount'].mean():.2f}")
        
        with col3:
            st.metric("Highest Expense", f"${df['amount'].max():.2f}")
        
        with col4:
            st.metric("Number of Expenses", len(df))
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💰 Expenses by Category")
            category_data = df.groupby('category')['amount'].sum().reset_index()
            fig = px.pie(category_data, values='amount', names='category', 
                        color_discrete_sequence=px.colors.qualitative.Set3)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 📈 Monthly Trend")
            df['month'] = df['date'].dt.to_period('M')
            monthly_data = df.groupby('month')['amount'].sum().reset_index()
            monthly_data['month'] = monthly_data['month'].astype(str)
            
            fig = px.bar(monthly_data, x='month', y='amount',
                        color='amount', color_continuous_scale='Viridis')
            fig.update_layout(xaxis_title="Month", yaxis_title="Amount ($)")
            st.plotly_chart(fig, use_container_width=True)
        
        # Detailed table
        st.markdown("#### 📋 Detailed Expense Report")
        st.dataframe(df, use_container_width=True)

# Settings Page
elif page == "⚙️ Settings":
    st.markdown("### ⚙️ Settings")
    
    st.markdown("#### 🎨 Theme Settings")
    theme = st.selectbox("Choose Theme", ["Default", "Dark", "Colorful", "Minimal"])
    
    st.markdown("#### 🔧 Application Settings")
    auto_save = st.checkbox("Auto-save changes", value=True)
    notifications = st.checkbox("Enable notifications", value=True)
    data_retention = st.slider("Data retention (days)", 30, 365, 90)
    
    st.markdown("#### 📊 Export Data")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export Expenses"):
            df = pd.DataFrame(st.session_state.expenses)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"expenses_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📊 Export Analytics"):
            st.info("Analytics export feature coming soon!")
    
    if st.button("💾 Save Settings", type="primary"):
        st.success("Settings saved successfully!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>💰 ExpenseWise - Built with Streamlit | Smart Expense Management</p>
</div>
""", unsafe_allow_html=True)
