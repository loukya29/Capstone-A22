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

def generate_pdf_report(farmer_name, fruit_name, shelf_life, quality, recommendations, fruit_image=None):
    """Generate PDF report with improved formatting and image inclusion."""
    if not os.path.exists("reports"):
        os.makedirs("reports")

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"fruit_report_{farmer_name}_{timestamp}.pdf"
    filepath = os.path.join("reports", filename)

    doc = SimpleDocTemplate(filepath, pagesize=letter)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=24, alignment=1,
                                 textColor=colors.HexColor('#1e88e5'))
    heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=16,
                                   textColor=colors.HexColor('#43a047'))

    elements = [Paragraph("Fruit Quality Analysis Report", title_style), Spacer(1, 20)]

    # Format multiline text for table cells
    def format_cell_text(text):
        return Paragraph(text, styles['Normal'])

    # Prepare table data with farmer name first
    data = [
        ["Farmer Name:", format_cell_text(farmer_name)],
        ["Report Generated:", format_cell_text(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))],
        ["Fruit Type:", format_cell_text(fruit_name)],
        ["Shelf Life:", format_cell_text(shelf_life)],
        ["Quality Score:", format_cell_text(quality)]
    ]

    # Create table with adjusted styling
    table = Table(data, colWidths=[2 * inch, 4 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # Add the fruit image
    if fruit_image:
        try:
            # Save the image temporarily
            img_temp = BytesIO()
            pil_image = PILImage.open(fruit_image)
            pil_image.save(img_temp, format='PNG')
            img_temp.seek(0)

            # Add image to PDF
            img = RLImage(img_temp, width=4 * inch, height=3 * inch)
            elements.append(Paragraph("Analyzed Fruit Image:", heading_style))
            elements.append(Spacer(1, 10))
            elements.append(img)
            elements.append(Spacer(1, 20))
        except Exception as e:
            print(f"Error processing image: {str(e)}")
        finally:
            fruit_image.seek(0)  # Reset file pointer

    # Add recommendations
    elements.append(Paragraph("Recommendations:", heading_style))
    for rec in recommendations.split('\n'):
        if rec.strip():
            elements.append(Paragraph(f"• {rec.strip()}", styles['Normal']))
            elements.append(Spacer(1, 10))

    doc.build(elements)
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
            fruit_name = st.selectbox("🍎 Fruit Type", ["Banana", "Apple", "Orange", "Mango"])

        submitted = st.form_submit_button("Generate Report")

        if submitted:
            if farmer_name and fruit_name and fruit_image:
                with st.spinner("🔄 Analyzing Image and Generating Report..."):
                    try:
                        # Convert to PIL Image for analysis
                        pil_image = PILImage.open(fruit_image).convert("RGB")
                        quality, shelf_life, recommendations = analyze_fruit_image(pil_image)

                        # Reset file pointer after PIL usage
                        fruit_image.seek(0)

                        pdf_path = generate_pdf_report(
                            farmer_name, fruit_name, shelf_life, quality, recommendations, fruit_image
                        )

                        st.success("✅ Report generated successfully!")
                        st.markdown(get_download_link(pdf_path), unsafe_allow_html=True)
                        st.info(f"📂 Report saved locally at: {pdf_path}")
                    except Exception as e:
                        st.error(f"Error generating report: {str(e)}")
                        print(f"Detailed error: {str(e)}")  # Added for debugging
            else:
                st.error("❌ Please fill in all required fields")