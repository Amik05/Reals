from fpdf import FPDF
from PIL import Image

def build_pdf(screenshots, post_data, output="reals.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for i, (path, data) in enumerate(zip(screenshots, post_data)):
        pdf.add_page()

        # Header
        pdf.set_font("Helvetica", "B", 20)
        pdf.cell(0, 10, "Reals", ln=True, align="C")
        pdf.set_draw_color(200, 200, 200)
        pdf.line(10, 20, 200, 20)
        pdf.ln(5)

        # Username
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 8, f"@{data.get('username', 'unknown')}  [{data.get('type', 'post')}]", ln=True)
        pdf.ln(2)

        # Image
        try:
            img = Image.open(path)
            img_w, img_h = img.size
            aspect = img_h / img_w
            display_w = 180
            display_h = min(display_w * aspect, 160)
            pdf.image(path, x=15, w=display_w, h=display_h)
            pdf.ln(display_h + 5)
        except:
            pdf.ln(5)

        # Summary
        pdf.set_font("Helvetica", "I", 11)
        pdf.set_text_color(80, 80, 80)
        summary = data.get("summary", "")
        pdf.multi_cell(0, 7, f"Summary: {summary}")
        pdf.ln(2)

        # Caption
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(0, 0, 0)
        caption = data.get("caption", "")
        if caption:
            pdf.multi_cell(0, 6, caption[:300])  # cap length

        # Divider
        pdf.ln(3)
        pdf.set_draw_color(220, 220, 220)

    pdf.output(output)
    print(f"✅ PDF saved as {output}")