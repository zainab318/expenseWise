"""
AI Processing module for ExpenseWise
Handles OCR, document analysis, and expense extraction
"""

import os
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import base64
from PIL import Image
import io

# Mock AI functions for free deployment
# In production, you'd use real AI services like OpenAI, Google Vision, etc.

class AIProcessor:
    def __init__(self):
        self.supported_formats = ['.pdf', '.jpg', '.jpeg', '.png', '.gif', '.tiff', '.bmp']
        self.expense_patterns = {
            'amount': [
                r'\$(\d+\.?\d*)',
                r'(\d+\.?\d*)\s*dollars?',
                r'total[:\s]*\$?(\d+\.?\d*)',
                r'amount[:\s]*\$?(\d+\.?\d*)'
            ],
            'date': [
                r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
                r'(\d{4}-\d{2}-\d{2})',
                r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d{1,2},?\s+\d{4}',
                r'(\d{1,2}\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d{4})'
            ],
            'vendor': [
                r'from[:\s]*([a-zA-Z\s&]+)',
                r'vendor[:\s]*([a-zA-Z\s&]+)',
                r'store[:\s]*([a-zA-Z\s&]+)',
                r'merchant[:\s]*([a-zA-Z\s&]+)'
            ]
        }
    
    def extract_text_from_image(self, image_path: str) -> str:
        """Extract text from image using OCR (mock implementation)"""
        # In production, use libraries like:
        # - pytesseract (Tesseract OCR)
        # - easyocr
        # - Google Vision API
        # - AWS Textract
        
        # Mock OCR result based on filename
        filename = os.path.basename(image_path).lower()
        
        mock_texts = {
            'receipt': """
            STARBUCKS COFFEE
            123 Main Street
            New York, NY 10001
            
            Date: 01/15/2024
            Time: 14:30
            
            Large Coffee        $4.50
            Muffin              $2.75
            Tax                 $0.65
            -----------------
            Total              $7.90
            
            Thank you for your visit!
            """,
            'invoice': """
            ACME CORPORATION
            Invoice #INV-2024-001
            
            Bill To:
            John Doe
            456 Business Ave
            City, State 12345
            
            Date: January 15, 2024
            Due Date: February 15, 2024
            
            Services:
            Web Development    $2,500.00
            Design Services    $1,200.00
            Consultation       $300.00
            -------------------------
            Subtotal          $4,000.00
            Tax (8.5%)         $340.00
            -------------------------
            Total             $4,340.00
            """,
            'default': """
            Sample Document
            Date: 01/15/2024
            Amount: $25.50
            Vendor: Sample Store
            Description: Sample purchase
            """
        }
        
        for key, text in mock_texts.items():
            if key in filename:
                return text
        
        return mock_texts['default']
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF (mock implementation)"""
        # In production, use libraries like:
        # - PyPDF2
        # - pdfplumber
        # - pymupdf (fitz)
        
        return """
        INVOICE
        
        Company: Tech Solutions Inc.
        Invoice #: INV-2024-001
        Date: January 15, 2024
        
        Bill To:
        Client Name
        123 Business Street
        City, State 12345
        
        Services:
        Software Development    $5,000.00
        Project Management      $1,500.00
        Testing & QA           $800.00
        ---------------------------
        Subtotal              $7,300.00
        Tax (10%)              $730.00
        ---------------------------
        Total                 $8,030.00
        
        Payment Terms: Net 30
        """
    
    def extract_expense_data(self, text: str) -> Dict:
        """Extract structured expense data from text"""
        extracted_data = {
            'amount': None,
            'date': None,
            'vendor': None,
            'description': None,
            'category': None,
            'confidence': 0.0
        }
        
        # Extract amount
        for pattern in self.expense_patterns['amount']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    extracted_data['amount'] = float(match.group(1))
                    break
                except ValueError:
                    continue
        
        # Extract date
        for pattern in self.expense_patterns['date']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                extracted_data['date'] = match.group(1)
                break
        
        # Extract vendor
        for pattern in self.expense_patterns['vendor']:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                extracted_data['vendor'] = match.group(1).strip()
                break
        
        # Categorize based on keywords
        text_lower = text.lower()
        if any(word in text_lower for word in ['coffee', 'starbucks', 'restaurant', 'food', 'lunch', 'dinner']):
            extracted_data['category'] = 'Food & Dining'
        elif any(word in text_lower for word in ['gas', 'fuel', 'gasoline', 'petrol']):
            extracted_data['category'] = 'Transportation'
        elif any(word in text_lower for word in ['hotel', 'accommodation', 'lodging']):
            extracted_data['category'] = 'Travel'
        elif any(word in text_lower for word in ['office', 'supplies', 'stationery', 'paper']):
            extracted_data['category'] = 'Office Supplies'
        elif any(word in text_lower for word in ['software', 'subscription', 'license', 'saas']):
            extracted_data['category'] = 'Technology'
        else:
            extracted_data['category'] = 'Other'
        
        # Generate description
        lines = text.split('\n')
        description_parts = []
        for line in lines:
            line = line.strip()
            if line and not re.match(r'^\$?\d+\.?\d*$', line) and len(line) > 3:
                description_parts.append(line)
        
        extracted_data['description'] = ' | '.join(description_parts[:3])
        
        # Calculate confidence
        confidence = 0.0
        if extracted_data['amount']:
            confidence += 0.4
        if extracted_data['date']:
            confidence += 0.3
        if extracted_data['vendor']:
            confidence += 0.2
        if extracted_data['category'] != 'Other':
            confidence += 0.1
        
        extracted_data['confidence'] = confidence
        
        return extracted_data
    
    def process_document(self, file_path: str, file_type: str) -> Dict:
        """Process a document and extract expense information"""
        try:
            # Extract text based on file type
            if file_type.lower() in ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/tiff', 'image/bmp']:
                text = self.extract_text_from_image(file_path)
            elif file_type.lower() == 'application/pdf':
                text = self.extract_text_from_pdf(file_path)
            else:
                return {
                    'success': False,
                    'error': f'Unsupported file type: {file_type}',
                    'extracted_data': None
                }
            
            # Extract structured data
            extracted_data = self.extract_expense_data(text)
            
            return {
                'success': True,
                'raw_text': text,
                'extracted_data': extracted_data,
                'processing_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'extracted_data': None
            }
    
    def categorize_expense_automatically(self, title: str, description: str = None) -> str:
        """Automatically categorize expense based on title and description"""
        text = f"{title} {description or ''}".lower()
        
        category_keywords = {
            'Food & Dining': ['restaurant', 'food', 'coffee', 'lunch', 'dinner', 'breakfast', 'cafe', 'bar', 'pizza', 'burger'],
            'Transportation': ['gas', 'fuel', 'uber', 'lyft', 'taxi', 'parking', 'toll', 'metro', 'bus', 'train'],
            'Travel': ['hotel', 'flight', 'airline', 'accommodation', 'lodging', 'booking', 'airbnb'],
            'Office Supplies': ['office', 'supplies', 'stationery', 'paper', 'pens', 'notebook', 'stapler'],
            'Technology': ['software', 'subscription', 'license', 'saas', 'cloud', 'hosting', 'domain', 'app'],
            'Business': ['meeting', 'client', 'conference', 'seminar', 'workshop', 'training'],
            'Healthcare': ['doctor', 'medical', 'pharmacy', 'hospital', 'clinic', 'medicine', 'health'],
            'Entertainment': ['movie', 'theater', 'concert', 'sports', 'game', 'entertainment', 'netflix', 'spotify']
        }
        
        for category, keywords in category_keywords.items():
            if any(keyword in text for keyword in keywords):
                return category
        
        return 'Other'
    
    def suggest_expense_title(self, vendor: str, amount: float, category: str) -> str:
        """Suggest expense title based on extracted data"""
        if vendor:
            return f"{vendor} - {category}"
        elif category != 'Other':
            return f"{category} Expense"
        else:
            return f"Business Expense - ${amount:.2f}"
    
    def validate_expense_data(self, data: Dict) -> Tuple[bool, List[str]]:
        """Validate extracted expense data"""
        errors = []
        
        if not data.get('amount') or data['amount'] <= 0:
            errors.append("Invalid or missing amount")
        
        if not data.get('date'):
            errors.append("No date found in document")
        
        if data.get('confidence', 0) < 0.3:
            errors.append("Low confidence in extracted data")
        
        return len(errors) == 0, errors
    
    def generate_expense_summary(self, expenses: List[Dict]) -> Dict:
        """Generate summary statistics for expenses"""
        if not expenses:
            return {
                'total_amount': 0,
                'expense_count': 0,
                'average_expense': 0,
                'top_category': None,
                'monthly_trend': []
            }
        
        total_amount = sum(exp.get('amount', 0) for exp in expenses)
        expense_count = len(expenses)
        average_expense = total_amount / expense_count if expense_count > 0 else 0
        
        # Category breakdown
        categories = {}
        for exp in expenses:
            category = exp.get('category', 'Other')
            categories[category] = categories.get(category, 0) + exp.get('amount', 0)
        
        top_category = max(categories.items(), key=lambda x: x[1])[0] if categories else None
        
        return {
            'total_amount': total_amount,
            'expense_count': expense_count,
            'average_expense': average_expense,
            'top_category': top_category,
            'category_breakdown': categories,
            'monthly_trend': []  # Would need date processing for this
        }
