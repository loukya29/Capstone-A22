from tkinter import Image
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
import datetime
import os
import firebase_admin
from firebase_admin import storage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import streamlit as st
import firebase_admin
from firebase_admin import credentials, storage
import json

# Initialize Firebase (only do this once)
def initialize_firebase():
    if not firebase_admin._apps:
        try:
            # Your credentials dictionary
            firebase_config = {
  "type": "service_account",
  "project_id": "visionml-flask",
  "private_key_id": "bb711339e4a0e57701e9dde2fa42dbc6c12c1af3",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQClr/ToH5pxsVhc\n3zrSxclo+c7aVihhQZc6CSDDkrmSCqIJ6S1L+e8v5hiHeUMmS8xvt3x2A0BOwjhU\n5gwTUF9DP94FgVWtLQw69EI1urXL0QmAbUIide6bvG+3gG+uC+KR1nKkGXFWooEs\nNloSCSFNyGYiaIjvdE4DlBrCXYcE2BMVS8EV6xXQ2D4dYOUJyKt6Gd8X7j6QumkC\nbbDLzazyvI1JJAB4kvC8dZZ13u42pIrAF5L1uCBJcIfjivuPQkGPylrkto9LZ4pZ\nb15iZxK1xhFiNrCEBheBX6890/nVmPb8Fu00jddN5wweCnBhm2uP0tv4NaTLzBlH\nW6vrytetAgMBAAECggEAKUGY30LdS3GQMeHw7QJMblwDrpi1CdCSBiS3OJOcqxmE\nMykReyFjNl9aXMNsXckSgP/kmSMinGneqn804wtIiT+KOn8ztQEqUjS3ltbkxTlK\nHyU1ikyoyzUe8UelJ2a0tkE6fxOJxfuFZButjl+hIBPmIKu8azmf4mK6zgqJYAJB\nveizqTWmD3tgdxg+dolDERGFau8UIfmPlJtfD7mw99kFpIwa9gyHswdPnb29jslR\ngFiuqYRk9S/7INkV1lEuFLrm3I5jUWfSil+P7Djy79z+ei7V2/V2W5/Hta75Tm4g\nf4utEZkBGcKy+nfPx6j1EYECHA7T7RSh8zLO6sMYGQKBgQDge2CNMQ7lj9OVc6DL\nbbJKbNUShR7mEKfSIyKplGkG/1PK1IIEPRG5X3dP25UAXcF8RvhTTyt9vCF1sMJy\n95N2i+ww0BuG/UxQb1OvYVOlF807jaYnnXR38NeiB4P0f0kL2WOhkBXRKV5z6/pO\nOnJ3NQmzqJu2zMpBgE+6sCMgSQKBgQC8806P6gg5EXtx+x03UEApPQsn3A8KLAAZ\nzRuuRVLXBUgFHVD4mi/IWJK6YB0xCkjqK3NTVdIaej/ic8n0TOJ3Gq19Fmbdn2qQ\nBBvH61bHpYLMH/YnVevdTSDHlnlTfWAC1CqHv6dysybMiMFb2RhqlHmq0GN7jLEP\nS1LE+0IERQKBgQCE7KnMkWsnxhXc3n4tV4SGi5FUCR21z9EAHqwMzIOwkAp3BYUD\nq4HOSdhlojnF4L6Mr52l/zBaoMcTYJqT50Qbo1k1wlU6hszkqDdel3wnO0Pc6tCj\njpoD18pn+JlLcv+3E3/qkF5K33s9m1M5dWSIcBCRoNqr0PJG/Qq5GkmCeQKBgQCw\nlyx7cByTSXV3x1s80PHGGNkOPaqItSq68mjGbN/JOZRfw1Bjp6a0taMcMKvXo2cW\nA9narsCYIl0GhXTfr+OPsQ0ndQJaap0rT8uvApGuMU+W+uART0oLIARcxJNLpkdP\nHX9KM6KJnknKqp0b/D/HjFBRhkUTuR/ZzWnj03eViQKBgEQdPwPGnPy4rOgOv9Yg\n3uWLUOa8MIfp/vstofKClSrKcKhgvE4mEqOCLyLH1Te+oeDQgCD+kpTc2My3/ofV\nWSv0x129qMXceE3/0tpTOiiWXNo37zRqg1iLgLeJadFGnfTDSH2nral4bcV9z75c\no7OPRhQ+0PzcUdBOUae5Z11h\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-njze6@visionml-flask.iam.gserviceaccount.com",
  "client_id": "107571811659290193675",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-njze6%40visionml-flask.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
            
            cred = credentials.Certificate(firebase_config)
            firebase_admin.initialize_app(cred, {
                'storageBucket': 'visionml-flask.appspot.com'
            })
            return True
        except Exception as e:
            st.error(f"Firebase initialization error: {e}")
            return False
    return True

# Test function to verify Firebase connection
def test_firebase_connection():
    try:
        # Initialize Firebase
        if initialize_firebase():
            # Try to access the bucket
            bucket = storage.bucket()
            st.success("✅ Successfully connected to Firebase Storage!")
            return True
        return False
    except Exception as e:
        st.error(f"Failed to connect to Firebase: {e}")
        return False

# # Add this to your main app to test:
# if st.button("Test Firebase Connection"):
#     test_firebase_connection()

def generate_pdf_report(farmer_name, fruit_name, shelf_life, recommendations, quality_score=None, fruit_image=None):
    """Generate an enhanced colorful PDF report"""
    if not os.path.exists("reports"):
        os.makedirs("reports")

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{farmer_name}_{timestamp}.pdf"
    filepath = os.path.join("reports", filename)

    doc = SimpleDocTemplate(
        filepath,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    styles = getSampleStyleSheet()
    
    # Enhanced custom styles with more color
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1,  # Center alignment
        textColor=colors.HexColor('#1e88e5')  # Blue title
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=10,
        textColor=colors.HexColor('#43a047')  # Green headings
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=12,
        spaceBefore=6,
        spaceAfter=6,
        textColor=colors.HexColor('#37474f')  # Dark gray text
    )

    elements = []

    # Title
    elements.append(Paragraph("🍎 Fruit Quality Analysis Report", title_style))
    elements.append(Spacer(1, 20))

    # Add report date and ID with colorful styling
    report_info = [
        ["Report ID:", f"FQA-{timestamp}"],
        ["Generated on:", datetime.datetime.now().strftime("%B %d, %Y at %I:%M %p")]
    ]
    
    report_table = Table(report_info, colWidths=[2*inch, 4*inch])
    report_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e3f2fd')),  # Light blue background
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1976d2')),  # Dark blue text
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bbdefb')),  # Light blue grid
    ]))
    elements.append(report_table)
    elements.append(Spacer(1, 20))

    # If fruit image is provided
    if fruit_image:
        # Process and add the fruit image
        elements.append(Paragraph("Fruit Image Analysis", heading_style))
        elements.append(Image(fruit_image, width=4*inch, height=3*inch))
        elements.append(Spacer(1, 20))

    # Farmer and Fruit Information with enhanced styling
    elements.append(Paragraph("Fruit Details", heading_style))
    basic_info = [
        ["Farmer Name:", farmer_name],
        ["Fruit Type:", fruit_name],
        ["Shelf Life:", f"{shelf_life} days"],
        ["Quality Score:", f"{quality_score}%" if quality_score is not None else "N/A"],
    ]
    
    info_table = Table(basic_info, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#c8e6c9')),  # Light green grid
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f5e9')),  # Light green background
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2e7d32')),  # Dark green text
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('PADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 20))

    # Quality Score Visualization with color-coded categories
    if quality_score is not None:
        elements.append(Paragraph("Quality Analysis", heading_style))
        quality_categories = {
            (90, 100): ("Excellent", '#2e7d32'),  # Dark green
            (80, 89): ("Very Good", '#388e3c'),   # Green
            (70, 79): ("Good", '#fdd835'),        # Yellow
            (60, 69): ("Fair", '#fb8c00'),        # Orange
            (0, 59): ("Needs Improvement", '#e53935')  # Red
        }
        
        quality_category, category_color = next(
            ((cat, color) for (start, end), (cat, color) in quality_categories.items() 
             if start <= quality_score <= end), 
            ("N/A", '#757575')
        )
        
        quality_info = [
            ["Score Category:", quality_category],
            ["Market Readiness:", "Ready for Premium Market" if quality_score >= 80 else 
                                "Ready for Standard Market" if quality_score >= 60 else 
                                "Requires Further Improvement"],
        ]
        
        quality_table = Table(quality_info, colWidths=[2*inch, 4*inch])
        quality_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e0e0e0')),
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor(category_color)),
            ('BACKGROUND', (1, 0), (1, 0), colors.HexColor(category_color)),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('PADDING', (0, 0), (-1, -1), 12),
        ]))
        elements.append(quality_table)
        elements.append(Spacer(1, 20))

    # Recommendations with colorful bullets
    elements.append(Paragraph("Storage & Handling Recommendations", heading_style))
    bullet_colors = ['#1e88e5', '#43a047', '#fb8c00', '#e53935', '#8e24aa']  # Different colors for bullets
    for i, rec in enumerate(recommendations.split('\n')):
        if rec.strip():
            bullet_style = ParagraphStyle(
                f'Bullet{i}',
                parent=body_style,
                textColor=colors.HexColor(bullet_colors[i % len(bullet_colors)]),
                leftIndent=20
            )
            elements.append(Paragraph(f"• {rec.strip()}", bullet_style))
    
    # Footer with gradient-like effect
    elements.append(Spacer(1, 30))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#546e7a'),
        alignment=1  # Center alignment
    )
    footer_text = f"""
    This report was generated by the Fruit Quality Analysis System.
    Report ID: FQA-{timestamp}
    For questions or concerns, please contact support.
    """
    elements.append(Paragraph(footer_text, footer_style))
    
    doc.build(elements)
    return filepath

def render_report_form():
    """Render the report generation form in Streamlit"""
    st.title("📝 Generate Fruit Quality Report")
    
    with st.form("report_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            farmer_name = st.text_input("👨‍🌾 Farmer Name")
            fruit_image = st.file_uploader("🍎 Upload Fruit Image", type=['jpg', 'jpeg', 'png'])
            fruit_name = st.selectbox("🍎 Fruit Type", ["Banana", "Apple", "Orange", "Mango"])
        
        with col2:
            shelf_life = st.number_input("📅 Estimated Shelf Life (days)", 
                                       min_value=1, max_value=30, value=7)
            quality_score = st.slider("✨ Quality Score", 0, 100, 85)
        
        recommendations = st.text_area(
            "📋 Recommendations",
            """1. Store in a cool, dry place
               2. Maintain optimal temperature between 13-15°C
               3. Check regularly for signs of ripening
               4. Ensure proper ventilation
               5. Handle with care to prevent bruising"""
        )
        
        submitted = st.form_submit_button("Generate Report")
        
        if submitted:
            if farmer_name and fruit_name:
                with st.spinner("🔄 Generating report..."):
                    try:
                        # Generate PDF with fruit image if provided
                        pdf_path = generate_pdf_report(
                            farmer_name, 
                            fruit_name, 
                            shelf_life, 
                            recommendations,
                            quality_score,
                            fruit_image
                        )
                        
                        # Upload to Firebase
                        bucket = storage.bucket()
                        blob = bucket.blob(f"reports/{os.path.basename(pdf_path)}")
                        blob.upload_from_filename(pdf_path)
                        blob.make_public()
                        report_url = blob.public_url
                        
                        st.success("✅ Report generated successfully!")
                        st.markdown(f"📎 Report URL: [{report_url}]({report_url})")
                    
                    except Exception as e:
                        st.error(f"Error generating report: {str(e)}")
            else:
                st.error("❌ Please fill in all required fields")              
def send_email(recipient_email, report_url, farmer_name):
    """Send email with report link"""
    sender_email = "your-email@gmail.com"  # Replace with your email
    password = "your-app-password"  # Replace with your app password
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = f"Fruit Quality Report for {farmer_name}"
    
    body = f"""
    Dear {farmer_name},
    
    Your fruit quality report is ready. You can access it using the following link:
    {report_url}
    
    Best regards,
    Fruit Quality Analysis Team
    """
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")
        return False


def upload_to_firebase(file_path, destination_blob_name):
    try:
        # Get bucket
        bucket = storage.bucket()
        
        # Create blob
        blob = bucket.blob(destination_blob_name)
        
        # Upload file
        blob.upload_from_filename(file_path)
        
        # Make the blob publicly accessible
        blob.make_public()
        
        # Get the public URL
        public_url = blob.public_url
        
        st.success(f"✅ File uploaded successfully to Firebase Storage!")
        return public_url
    
    except Exception as e:
        st.error(f"Failed to upload file to Firebase: {e}")
        return None