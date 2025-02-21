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
# from firebase_config import test_firebase_connection, upload_to_firebase
import os
import base64


def generate_pdf_report(farmer_name, fruit_name, shelf_life, recommendations, quality_score=None, fruit_image=None):
    """Generate PDF report and return the file path"""
    # Create reports directory if it doesn't exist
    if not os.path.exists("reports"):
        os.makedirs("reports")

    # Generate unique filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"fruit_report_{farmer_name}_{timestamp}.pdf"
    filepath = os.path.join("reports", filename)

    doc = SimpleDocTemplate(
        filepath,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1,
        textColor=colors.HexColor('#1e88e5')
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=10,
        textColor=colors.HexColor('#43a047')
    )

    elements = []

    # Add content to the PDF
    elements.append(Paragraph("Fruit Quality Analysis Report", title_style))
    elements.append(Spacer(1, 20))

    # Basic information table
    data = [
        ["Report Generated:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M")],
        ["Farmer Name:", farmer_name],
        ["Fruit Type:", fruit_name],
        ["Shelf Life:", f"{shelf_life} days"],
        ["Quality Score:", f"{quality_score}%" if quality_score else "N/A"]
    ]

    table = Table(data, colWidths=[2*inch, 4*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)
    elements.append(Spacer(1, 20))

    # Recommendations
    elements.append(Paragraph("Recommendations:", heading_style))
    for rec in recommendations.split('\n'):
        if rec.strip():
            elements.append(Paragraph(f"• {rec.strip()}", styles['Normal']))
            elements.append(Spacer(1, 10))

    # Build PDF
    doc.build(elements)
    return filepath

def get_download_link(file_path):
    """Generate a download link for a file"""
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    filename = os.path.basename(file_path)
    return f'<a href="data:application/pdf;base64,{b64}" download="{filename}">Download Report</a>'

def render_report_form():
    """Render the report generation form"""
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
                        # Generate PDF
                        pdf_path = generate_pdf_report(
                            farmer_name, 
                            fruit_name, 
                            shelf_life, 
                            recommendations,
                            quality_score,
                            fruit_image
                        )
                        
                        # Create download link
                        st.success("✅ Report generated successfully!")
                        st.markdown(get_download_link(pdf_path), unsafe_allow_html=True)
                        
                        # Optional: Display file location
                        st.info(f"📂 Report saved locally at: {pdf_path}")
                        
                    except Exception as e:
                        st.error(f"Error generating report: {str(e)}")
            else:
                st.error("❌ Please fill in all required fields")
# def render_report_form():
#     st.title("📝 Generate Fruit Quality Report")
    
#     with st.form("report_form"):
#         col1, col2 = st.columns(2)
        
#         with col1:
#             farmer_name = st.text_input("👨‍🌾 Farmer Name")
#             fruit_image = st.file_uploader("🍎 Upload Fruit Image", type=['jpg', 'jpeg', 'png'])
#             fruit_name = st.selectbox("🍎 Fruit Type", ["Banana", "Apple", "Orange", "Mango"])
        
#         with col2:
#             shelf_life = st.number_input("📅 Estimated Shelf Life (days)", 
#                                        min_value=1, max_value=30, value=7)
#             quality_score = st.slider("✨ Quality Score", 0, 100, 85)
        
#         recommendations = st.text_area(
#             "📋 Recommendations",
#             """1. Store in a cool, dry place
#                2. Maintain optimal temperature between 13-15°C
#                3. Check regularly for signs of ripening
#                4. Ensure proper ventilation
#                5. Handle with care to prevent bruising"""
#         )
        
#         submitted = st.form_submit_button("Generate Report")
        
#         if submitted:
#             if farmer_name and fruit_name:
#                 with st.spinner("🔄 Generating report..."):
#                     try:
#                         pdf_path = generate_pdf_report(
#                             farmer_name, 
#                             fruit_name, 
#                             shelf_life, 
#                             recommendations,
#                             quality_score,
#                             fruit_image
#                         )
                        
#                         report_url = upload_to_firebase(
#                             pdf_path, 
#                             f"reports/{os.path.basename(pdf_path)}"
#                         )
                        
#                         if report_url:
#                             st.success("✅ Report generated successfully!")
#                             st.markdown(f"📎 Report URL: [{report_url}]({report_url})")
                    
#                     except Exception as e:
#                         st.error(f"Error generating report: {str(e)}")
#             else:
#                 st.error("❌ Please fill in all required fields")            
# def send_email(recipient_email, report_url, farmer_name):
#     """Send email with report link"""
#     sender_email = "your-email@gmail.com"  # Replace with your email
#     password = "your-app-password"  # Replace with your app password
    
#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = recipient_email
#     msg['Subject'] = f"Fruit Quality Report for {farmer_name}"
    
#     body = f"""
#     Dear {farmer_name},
    
#     Your fruit quality report is ready. You can access it using the following link:
#     {report_url}
    
#     Best regards,
#     Fruit Quality Analysis Team
#     """
    
#     msg.attach(MIMEText(body, 'plain'))
    
#     try:
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.starttls()
#         server.login(sender_email, password)
#         server.send_message(msg)
#         server.quit()
#         return True
#     except Exception as e:
#         st.error(f"Failed to send email: {str(e)}")
#         return False


# def upload_to_firebase(file_path, destination_blob_name):
#     try:
#         # Get bucket
#         bucket = storage.bucket()
        
#         # Create blob
#         blob = bucket.blob(destination_blob_name)
        
#         # Upload file
#         blob.upload_from_filename(file_path)
        
#         # Make the blob publicly accessible
#         blob.make_public()
        
#         # Get the public URL
#         public_url = blob.public_url
        
#         st.success(f"✅ File uploaded successfully to Firebase Storage!")
#         return public_url
    
#     except Exception as e:
#         st.error(f"Failed to upload file to Firebase: {e}")
#         return None