# 💰 ExpenseWise - Streamlit Frontend

A colorful, interactive Streamlit application for smart expense management and receipt processing.

## 🎨 Features

### 🏠 **Home Dashboard**
- **Colorful Metrics**: Beautiful gradient cards showing expense statistics
- **Quick Actions**: One-click access to main features
- **Recent Expenses**: Preview of latest expenses with colorful cards
- **Interactive Navigation**: Smooth sidebar navigation

### 💰 **Expense Management**
- **Add Expenses**: Interactive form with validation
- **Filter & Search**: Real-time filtering by category, date, amount
- **Sort Options**: Multiple sorting options for better organization
- **Delete Expenses**: One-click deletion with confirmation
- **Colorful Cards**: Gradient expense cards with category badges

### 📁 **File Upload & Processing**
- **Drag & Drop**: Interactive file upload area
- **Multiple Formats**: Support for PDF, DOC, XLS, PPT, images
- **Processing Options**: OCR, AI analysis, expense extraction
- **Progress Tracking**: Real-time upload and processing progress
- **File Management**: View, process, and remove uploaded files

### 📊 **Analytics Dashboard**
- **Interactive Charts**: Pie charts, bar charts, trend analysis
- **Summary Metrics**: Total, average, highest expenses
- **Category Analysis**: Expense breakdown by category
- **Monthly Trends**: Time-series analysis
- **Export Options**: Download data as CSV

### ⚙️ **Settings & Configuration**
- **Theme Selection**: Multiple color themes
- **Application Settings**: Auto-save, notifications, data retention
- **Data Export**: Export expenses and analytics
- **User Preferences**: Customizable interface

## 🚀 Quick Start

### Option 1: Direct Python Run
```bash
# Install dependencies
pip install streamlit plotly pandas pillow python-multipart

# Run the application
python run_streamlit.py
```

### Option 2: Streamlit Command
```bash
# Install dependencies
pip install streamlit plotly pandas pillow python-multipart

# Run directly
streamlit run streamlit_app.py --server.port=8501
```

### Option 3: Docker
```bash
# Build and run with Docker Compose
docker-compose up frontend
```

## 🎨 Design Features

### **Colorful Theme**
- **Gradient Backgrounds**: Blue-purple gradients throughout
- **Interactive Cards**: Hover effects and smooth transitions
- **Color-coded Categories**: Visual category identification
- **Status Indicators**: Color-coded status messages
- **Responsive Design**: Works on all screen sizes

### **Interactive Elements**
- **Real-time Updates**: Instant UI updates on data changes
- **Progress Bars**: Visual feedback for long operations
- **Hover Effects**: Smooth animations and transitions
- **Form Validation**: Real-time input validation
- **File Drag & Drop**: Intuitive file handling

## 📱 Pages Overview

### 🏠 **Home Page**
- Welcome header with gradient background
- Quick stats in colorful metric cards
- Recent expenses preview
- Quick action buttons

### 💰 **Expense Management**
- Add new expense form with validation
- Filter and search functionality
- Sortable expense list
- Delete functionality

### 📁 **File Upload**
- Drag and drop upload area
- File type validation
- Processing options
- Progress tracking

### 📊 **Analytics**
- Interactive charts and graphs
- Summary statistics
- Category breakdown
- Export functionality

### ⚙️ **Settings**
- Theme customization
- Application preferences
- Data export options
- User configuration

## 🛠️ Technical Details

### **Dependencies**
- `streamlit`: Web application framework
- `plotly`: Interactive charts and graphs
- `pandas`: Data manipulation and analysis
- `pillow`: Image processing
- `python-multipart`: File upload handling

### **Features**
- **Session State**: Persistent data across page navigation
- **File Handling**: Multiple file upload with validation
- **Data Visualization**: Interactive charts and graphs
- **Responsive Design**: Mobile-friendly interface
- **Real-time Updates**: Instant UI feedback

## 🎯 Usage

1. **Start the Application**: Run `python run_streamlit.py`
2. **Navigate**: Use the sidebar to switch between pages
3. **Add Expenses**: Use the expense management page
4. **Upload Files**: Use the file upload page for document processing
5. **View Analytics**: Check the analytics dashboard for insights
6. **Configure Settings**: Customize the application in settings

## 🔧 Configuration

### **Port Configuration**
- Default port: `8501`
- Change in `run_streamlit.py` or docker-compose.yml

### **Theme Customization**
- Modify CSS in the `st.markdown()` sections
- Update color schemes in the gradient definitions
- Customize button styles and hover effects

### **Data Persistence**
- Uses Streamlit session state
- Data persists during session
- Export functionality for data backup

## 🎨 Color Scheme

- **Primary**: Blue-purple gradients (#667eea to #764ba2)
- **Secondary**: Pink-red gradients (#f093fb to #f5576c)
- **Accent**: Blue-cyan gradients (#4facfe to #00f2fe)
- **Success**: Green gradients (#11998e to #38ef7d)
- **Warning**: Orange-red gradients

## 📈 Performance

- **Fast Loading**: Optimized for quick page loads
- **Smooth Animations**: CSS transitions for better UX
- **Efficient Data Handling**: Pandas for data operations
- **Interactive Charts**: Plotly for responsive visualizations

## 🚀 Future Enhancements

- **Database Integration**: Persistent data storage
- **User Authentication**: Login and user management
- **API Integration**: Connect to backend services
- **Advanced Analytics**: More chart types and insights
- **Mobile App**: React Native or Flutter mobile app
- **Real-time Processing**: WebSocket integration

---

**💰 ExpenseWise - Built with ❤️ using Streamlit, Plotly, and Pandas**
