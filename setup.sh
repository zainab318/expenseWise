#!/bin/bash

# ExpenseWise Setup Script
echo "💰 Setting up ExpenseWise - Smart Expense Management..."

# Check Python version
echo "🐍 Checking Python version..."
python --version

# Install Python dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create database
echo "🗄️ Initializing database..."
python -c "from database import Database; Database()"

# Create uploads directory
echo "📁 Creating uploads directory..."
mkdir -p uploads
mkdir -p temp

# Set permissions
echo "🔐 Setting permissions..."
chmod +x run_streamlit.py
chmod +x setup.sh

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "🔧 Creating environment file..."
    cat > .env << EOF
# ExpenseWise Environment Variables
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///expensewise.db
DEBUG=False
EOF
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To run the application:"
echo "   python run_streamlit.py"
echo ""
echo "🌐 Access the app at: http://localhost:8501"
echo ""
echo "📚 For deployment instructions, see DEPLOYMENT_GUIDE.md"
echo ""
echo "💰 ExpenseWise is ready to manage your expenses!"
