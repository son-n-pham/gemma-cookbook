import os
from docling.doc import Document
from pypdf import PdfReader  # For potentially reading PDFs
import json


def process_document_with_docling(file_path):
    """
    Processes a document (PDF or image) using Docling to extract text and structure.

    Args:
        file_path (str): The path to the input PDF or image file.

    Returns:
        dict: A dictionary containing the extracted content,
              or None if processing fails.
    """
    try:
        # Docling can directly process file paths
        doc = Document.from_file(file_path)

        # You can get various representations.
        # For querying with an LLM, the raw text or markdown is often best.
        # Let's get markdown for structured content like tables.
        markdown_content = doc.to_markdown()

        # You can also get plain text
        plain_text_content = doc.to_text()

        # Or a more structured JSON representation if needed for deeper parsing
        # json_content = doc.to_json() # This can be quite detailed

        print(f"Docling processing successful for: {file_path}")
        print("\n--- Extracted Markdown (first 500 chars) ---")
        print(markdown_content[:500])
        print("\n--- Extracted Plain Text (first 500 chars) ---")
        print(plain_text_content[:500])

        return {
            "markdown_content": markdown_content,
            "plain_text_content": plain_text_content,
            # "json_content": json.loads(json_content) # if you choose to use it
        }

    except Exception as e:
        print(f"Error processing document with Docling: {e}")
        return None


# --- Example Usage for Docling Processing ---
if __name__ == "__main__":
    # Create a dummy PDF for demonstration if you don't have one
    # For a real scenario, you'd replace this with your actual drilling reports.
    dummy_pdf_path = (
        "C:\\development\\gemma-cookbook\\Gemma\\Docling_Gemma3\\pdf\\ddr.pdf"
    )
    if not os.path.exists(dummy_pdf_path):
        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            Table,
            TableStyle,
        )
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.units import inch
        from reportlab.lib import colors

        doc = SimpleDocTemplate(dummy_pdf_path)
        styles = getSampleStyleSheet()
        story = []

        # Title
        story.append(
            Paragraph("<b>Daily Drilling Report - Well X-123</b>", styles["h1"])
        )
        story.append(Spacer(1, 0.2 * inch))

        # Date and Time
        story.append(Paragraph("<b>Date:</b> 2025-05-24", styles["Normal"]))
        story.append(Paragraph("<b>Time:</b> 06:00 - 06:00 (24 hrs)", styles["Normal"]))
        story.append(Spacer(1, 0.2 * inch))

        # Operations Summary
        story.append(Paragraph("<b>Operations Summary:</b>", styles["h2"]))
        story.append(
            Paragraph(
                'Continued drilling 12-1/4" hole section. Encountered minor shale stringer at 3500 ft. Circulated bottoms up and resumed drilling. No issues encountered with mud properties. Pump pressure stable.',
                styles["Normal"],
            )
        )
        story.append(Spacer(1, 0.2 * inch))

        # Drilling Parameters Table
        story.append(Paragraph("<b>Drilling Parameters:</b>", styles["h2"]))
        data = [
            ["Parameter", "Value", "Unit"],
            ["Current Depth", "3600", "ft"],
            ["Bit Depth", "3590", "ft"],
            ["ROP (Avg)", "50", "ft/hr"],
            ["WOB", "30", "klbs"],
            ["RPM", "120", "rpm"],
            ["Mud Weight In", "9.8", "ppg"],
            ["Mud Weight Out", "9.9", "ppg"],
        ]
        table = Table(data, colWidths=[2 * inch, 1.5 * inch, 1 * inch])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )
        story.append(table)
        story.append(Spacer(1, 0.2 * inch))

        # Incidents
        story.append(Paragraph("<b>Incidents:</b>", styles["h2"]))
        story.append(Paragraph("None.", styles["Normal"]))
        story.append(Spacer(1, 0.2 * inch))

        # Crew
        story.append(
            Paragraph(
                "<b>Crew On Duty:</b> John Doe (Driller), Jane Smith (Assistant Driller)",
                styles["Normal"],
            )
        )

        doc.build(story)
        print(f"Created dummy PDF at: {dummy_pdf_path}")

    # Process the dummy PDF
    extracted_data = process_document_with_docling(dummy_pdf_path)

    if extracted_data:
        # Now, proceed to Gemma integration with extracted_data
        print("\nDocling extraction complete. Ready for Gemma integration.")
    else:
        print("\nDocling extraction failed. Cannot proceed to Gemma integration.")
