#!/usr/bin/env python3
"""
Streamlit App Runner
Run this script to start the ExpenseWise Streamlit application
"""

import subprocess
import sys
import os

def main():
    """Run the Streamlit application"""
    try:
        # Check if streamlit is installed
        subprocess.run([sys.executable, "-c", "import streamlit"], check=True)
        
        # Run streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port=8501",
            "--server.address=0.0.0.0",
            "--theme.base=light",
            "--theme.primaryColor=#667eea",
            "--theme.backgroundColor=#ffffff",
            "--theme.secondaryBackgroundColor=#f0f2f6",
            "--theme.textColor=#262730"
        ])
    except subprocess.CalledProcessError:
        print("❌ Streamlit is not installed. Please install it first:")
        print("pip install streamlit plotly pandas pillow")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 ExpenseWise app stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()
