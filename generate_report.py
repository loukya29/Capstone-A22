from PIL import ImageOps

from constants.common_imports import *

API_KEY = "AIzaSyDMEdiL-HTYOXl8bGSDHSJ98UV3UEte3MU"
genai.configure(api_key= API_KEY)


def analyze_fruit_image(image):
    """Analyze the fruit image using Google Gemini AI."""
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Structured prompt for multiple fruits
    prompt = """Analyze the given image and provide the following details for each fruit present:

    For each fruit, follow this exact format:
    Fruit Name: [fruit name]
    Quality: [Good/Bad] - [reasoning]
    Estimated Shelf Life: [number] days

    After analyzing all fruits, provide 3-4 specific recommendations for maintaining their quality. 
    Format recommendations exactly like this:
    Recommendations:
    1. [First recommendation]
    2. [Second recommendation]
    3. [Third recommendation]
    4. [Fourth recommendation] (if applicable)

    Important: 
    - Separate each fruit's analysis with a blank line
    - Maintain the exact same heading format for each section
    - List all fruits present in the image
    - Do not use any markdown formatting (no ** or other formatting)"""

    response = model.generate_content([prompt, image])
    processed_text = response.text

    # Clean the text by removing any remaining markdown
    cleaned_text = processed_text.replace("**", "").strip()

    # Parse the structured response
    fruits = []
    current_fruit = {}
    recommendations = []
    in_recommendations = False

    for line in cleaned_text.split("\n"):
        line = line.strip()

        if line.startswith("Fruit Name:"):
            if current_fruit:  # Save previous fruit if exists
                fruits.append(current_fruit)
            current_fruit = {
                'name': line.split(":", 1)[-1].strip(),
                'quality': None,
                'shelf_life': None
            }
        elif line.startswith("Quality:") and current_fruit:
            current_fruit['quality'] = line.split(":", 1)[-1].strip()
        elif line.startswith("Estimated Shelf Life:") and current_fruit:
            current_fruit['shelf_life'] = line.split(":", 1)[-1].strip()
        elif line.startswith("Recommendations:"):
            in_recommendations = True
        elif in_recommendations and line and line[0].isdigit():
            rec = line.split(".", 1)[-1].strip()
            recommendations.append(rec)

    # Add the last fruit if exists
    if current_fruit:
        fruits.append(current_fruit)

    # Format the output without any markdown
    quality = ", ".join([f"{f['name']}: {f['quality']}" for f in fruits])
    shelf_life = ", ".join([f"{f['name']}: {f['shelf_life']}" for f in fruits])
    recommendations_str = "\n".join(recommendations)

    return quality, shelf_life, recommendations_str


def generate_pdf_report(farmer_name, shelf_life, quality, recommendations, fruit_image=None):
    """Generate PDF report with modern, professional theme and improved structure."""
    if not os.path.exists("reports"):
        os.makedirs("reports")

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"fruit_report_{farmer_name}_{timestamp}.pdf"
    filepath = os.path.join("reports", filename)

    doc = SimpleDocTemplate(filepath, pagesize=letter,
                            leftMargin=0.75 * inch, rightMargin=0.75 * inch,
                            topMargin=0.75 * inch, bottomMargin=0.75 * inch)
    styles = getSampleStyleSheet()

    # Professional color scheme
    background_color = '#F5F6F5'  # Light gray
    primary_color = '#2C3E50'  # Dark blue-gray
    accent_color = '#3498DB'  # Blue
    text_color = '#333333'  # Dark gray
    card_bg = '#FFFFFF'  # White for cards

    # Define custom styles only if they don't exist
    style_definitions = {
        'ReportTitle': ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=22,
            alignment=1,
            textColor=colors.HexColor(primary_color),
            spaceAfter=24
        ),
        'SectionHeading': ParagraphStyle(
            'SectionHeading',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=16,
            textColor=colors.HexColor(primary_color),
            spaceAfter=12,
            spaceBefore=12
        ),
        'BodyText': ParagraphStyle(
            'BodyText',
            parent=styles['Normal'],
            fontName='Helvetica',
            textColor=colors.HexColor(text_color),
            fontSize=11,
            leading=14,
            spaceAfter=8
        ),
        'CardLabel': ParagraphStyle(
            'CardLabel',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            textColor=colors.HexColor(text_color),
            fontSize=11,
            leading=14
        )
    }

    # Add styles only if they don't already exist
    for style_name, style in style_definitions.items():
        if style_name not in styles:
            styles.add(style)

    # Create story elements
    elements = []

    # Header
    elements.append(Paragraph("Fruit Quality Analysis Report", styles['ReportTitle']))
    elements.append(Spacer(1, 12))

    # Farmer Info Section
    farmer_data = [
        ["Farmer Name:", Paragraph(farmer_name, styles['BodyText'])],
        ["Report Date:", Paragraph(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                                   styles['BodyText'])],
        ["Fruit Type:", Paragraph("Banana", styles['BodyText'])]  # Assuming from input PDF
    ]

    farmer_table = Table(farmer_data, colWidths=[2 * inch, 4.5 * inch])
    farmer_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(card_bg)),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor(primary_color)),
        ('TEXTCOLOR', (1, 0), (-1, -1), colors.HexColor(text_color)),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#E0E0E0')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E0E0E0')),
    ]))
    elements.append(farmer_table)
    elements.append(Spacer(1, 24))

    # Analysis Section
    elements.append(Paragraph("Fruit Analysis", styles['SectionHeading']))

    # Split shelf life and quality for better formatting
    shelf_life_lines = shelf_life.split(', ')
    quality_lines = quality.split(', ')

    analysis_data = [
        ["Shelf Life:", Paragraph("<br/>".join(shelf_life_lines), styles['BodyText'])],
        ["Quality Assessment:", Paragraph("<br/>".join(quality_lines), styles['BodyText'])]
    ]

    analysis_table = Table(analysis_data, colWidths=[2 * inch, 4.5 * inch])
    analysis_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(card_bg)),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor(primary_color)),
        ('TEXTCOLOR', (1, 0), (-1, -1), colors.HexColor(text_color)),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#E0E0E0')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E0E0E0')),
    ]))
    elements.append(analysis_table)
    elements.append(Spacer(1, 24))

    # Image Section
    if fruit_image:
        try:
            elements.append(Paragraph("Analyzed Fruit Image", styles['SectionHeading']))

            img_temp = BytesIO()
            pil_image = PILImage.open(fruit_image)

            # Professional image border
            bordered_img = ImageOps.expand(pil_image, border=8,
                                           fill=(255, 255, 255))  # White border
            bordered_img.save(img_temp, format='PNG')
            img_temp.seek(0)

            from reportlab.platypus import Image as RLImage
            img = RLImage(img_temp, width=4 * inch, height=3 * inch)
            img.hAlign = 'CENTER'
            elements.append(img)
            elements.append(Spacer(1, 24))
        except Exception as e:
            print(f"Error processing image: {str(e)}")
        finally:
            if hasattr(fruit_image, 'seek'):
                fruit_image.seek(0)

    # Recommendations Section
    elements.append(Paragraph("Recommendations", styles['SectionHeading']))

    rec_list = [r.strip() for r in recommendations.split('\n') if r.strip()]
    for rec in rec_list:
        bullet = Paragraph(f"• {rec}", styles['BodyText'])
        elements.append(bullet)
        elements.append(Spacer(1, 6))

    # Footer
    elements.append(Spacer(1, 36))
    if 'Footer' not in styles:
        styles.add(ParagraphStyle('Footer',
                                  parent=styles['Normal'],
                                  fontName='Helvetica',
                                  fontSize=9,
                                  textColor=colors.HexColor('#666666'),
                                  alignment=1))
    elements.append(Paragraph("Generated by Fruit Quality Analyzer", styles['Footer']))

    # Background
    def add_background(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(colors.HexColor(background_color))
        canvas.rect(0, 0, doc.width + doc.leftMargin * 2,
                    doc.height + doc.topMargin * 2, stroke=0, fill=1)
        canvas.restoreState()
        return None

    doc.build(elements, onFirstPage=add_background, onLaterPages=add_background)

    return filepath

def get_download_link(file_path):
    """Generate a download link for the PDF report."""
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    filename = os.path.basename(file_path)
    return f'<a href="data:application/pdf;base64,{b64}" download="{filename}">Download Report</a>'


def render_report_form():
    """Render the report generation form."""
    st.title("📝 Generate Fruit Quality Report")

    with st.form("report_form"):
        col1, col2 = st.columns(2)

        with col1:
            farmer_name = st.text_input("👨‍🌾 Farmer Name")
            fruit_image = st.file_uploader("🍎 Upload Fruit Image", type=['jpg', 'jpeg', 'png'])
            # fruit_name = st.selectbox("🍎 Fruit Type", ["Banana", "Apple", "Orange", "Mango"])

        submitted = st.form_submit_button("Generate Report")

        if submitted:
            if farmer_name and fruit_image:
                with st.spinner("🔄 Analyzing Image and Generating Report..."):
                    try:
                        # Convert to PIL Image for analysis
                        pil_image = PILImage.open(fruit_image).convert("RGB")
                        quality, shelf_life, recommendations = analyze_fruit_image(pil_image)

                        # Reset file pointer after PIL usage
                        fruit_image.seek(0)

                        pdf_path = generate_pdf_report(
                            farmer_name, shelf_life, quality, recommendations, fruit_image
                        )

                        st.success("✅ Report generated successfully!")
                        st.markdown(get_download_link(pdf_path), unsafe_allow_html=True)
                        st.info(f"📂 Report saved locally at: {pdf_path}")
                    except Exception as e:
                        st.error(f"Error generating report: {str(e)}")
                        print(f"Detailed error: {str(e)}")  # Added for debugging
            else:
                st.error("❌ Please fill in all required fields")