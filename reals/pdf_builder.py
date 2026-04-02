from fpdf import FPDF
from PIL import Image

def build_pdf(screenshots, post_data, output="reals.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=False, margin=15)

    for i, ((path, comments_path), data) in enumerate(zip(screenshots, post_data)):
        
        # New page every 2 reels
        if i % 2 == 0:
            pdf.add_page()
            # Header
            pdf.set_font("Helvetica", "B", 20)
            pdf.cell(0, 10, "Reals", ln=True, align="C")
            pdf.set_draw_color(200, 200, 200)
            pdf.line(10, 12, 200, 12)

        # Top reel starts at y=20, bottom reel starts at y=155
        y_start = 20 if i % 2 == 0 else 155

        # Thumbnail left, comments right
        thumb_x, thumb_w, thumb_h = 10, 90, 123
        comments_x = thumb_x + thumb_w + 5
        comments_w, comments_h = 45, 92
        comments_y = y_start + (thumb_h - comments_h) / 2

        try:
            pdf.image(path, x=thumb_x, y=y_start, w=thumb_w, h=thumb_h)
        except:
            pass

        if comments_path:
            pdf.image(comments_path, x=comments_x, y=comments_y, w=comments_w, h=comments_h)

        # Summary inline to the right of comments
        summary_x = comments_x + comments_w + 5
        summary_w = 200 - summary_x - 5  # remaining page width

        pdf.set_xy(summary_x, y_start)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(0, 0, 0)
        pdf.multi_cell(summary_w, 5, f"@{data.get('username', 'unknown')}")

        pdf.set_xy(summary_x, pdf.get_y())
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(80, 80, 80)
        pdf.multi_cell(summary_w, 4, data.get("summary", ""))

        pdf.set_xy(summary_x, pdf.get_y() + 2)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(120, 120, 120)
        pdf.multi_cell(summary_w, 4, data.get("caption", "")[:150])

        # Divider between the two reels
        if i % 2 == 0:
            pdf.set_draw_color(220, 220, 220)
            pdf.line(10, 150, 200, 150)

    pdf.output(output)
    print(f"✅ PDF saved as {output}")