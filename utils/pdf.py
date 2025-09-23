import os
from fpdf import FPDF
from fpdf.enums import Align, XPos, YPos

# Set up font paths (assumed to be correct)
FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')
FONT_FILE_NORMAL = os.path.join(FONT_DIR, 'STIXTwoMath-Regular.ttf')
FONT_FILE_BOLD = os.path.join(FONT_DIR, 'STIXTwoMath-Regular.ttf')
FONT_FAMILY = "STIXTwoText-Regular"
LINE_SPACE_AFTER_TITLE = 15

def generate_pdf_files(
        project,
        problem_answer_list,
        num_column=1,
        row_spacing=20
):

    try:

        # Generate Problems PDF
        pdf_problems = _create_pdf(f"{project}")
        _add_content(
            pdf_problems,
            problem_answer_list,
            num_column,
            row_spacing,
            project
        )
        pdf_problems.output(f"{project.replace(" ", "_")}.pdf")
        print(f"***'{project.replace(" ", "_")}.pdf' has been created.")

    except FileNotFoundError as e:
        print(f"Error: {e}")


def _create_pdf(title):
    """Helper to create a new FPDF object with standard settings."""
    pdf = FPDF('P', 'mm', 'Letter')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    if not os.path.exists(FONT_FILE_NORMAL) or not os.path.exists(FONT_FILE_BOLD):
        raise FileNotFoundError(f"One or more font files not found in {FONT_DIR}")
    pdf.add_font(FONT_FAMILY, "", FONT_FILE_NORMAL)
    pdf.add_font(FONT_FAMILY, "B", FONT_FILE_BOLD)
    pdf.set_font(FONT_FAMILY, 'B', 16)
    pdf.cell(w=0, h=10, text=title, new_x=XPos.LMARGIN, new_y=YPos.TOP, align=Align.C)
    pdf.ln(LINE_SPACE_AFTER_TITLE)
    pdf.set_font(FONT_FAMILY, '', 14)
    return pdf


def _add_content(pdf, content_list, num_columns, row_spacing, project_title=None):
    """
    A general-purpose helper to add content in multiple columns, with automatic line wrapping.
    """
    margin = 10
    total_width = pdf.w - 2 * margin
    col_width = total_width / num_columns
    column_y = [pdf.get_y()] * num_columns

    for i, content in enumerate(content_list):
        col_index = i % num_columns

        pdf.set_xy(margin + col_index * col_width, column_y[col_index])

        # Using multi_cell for automatic line breaks
        prefix = f"{i + 1}) "
        text = f"{prefix}{content}"

        #print(f"prefix: {prefix}, y: {pdf.get_y()}")
        # Calculate text height for the current cell
        text_height = pdf.get_string_width(text) / col_width * pdf.font_size * 1.2
        if text_height < pdf.font_size * 1.2:
            text_height = pdf.font_size * 1.2

        # Draw the text and get the new y position
        pdf.multi_cell(
            w=col_width,
            h=pdf.font_size * 1.2,
            text=text,
            align=Align.L,
            new_x=XPos.RIGHT,
            new_y=YPos.TOP
        )
        column_y[col_index] = pdf.get_y() + row_spacing - text_height

        # Add new page if any column reaches the bottom
        if max(column_y) > pdf.page_break_trigger - 20 and (i+1)%num_columns == 0:
            print("adding page!!")
            pdf.add_page()
            if project_title:
                pdf.set_font(FONT_FAMILY, 'B', 16)
                pdf.cell(w=0, h=10, text=project_title, new_x=XPos.LMARGIN, new_y=YPos.TOP, align=Align.C)
                pdf.ln(LINE_SPACE_AFTER_TITLE)
            pdf.set_font(FONT_FAMILY, '', 14)
            column_y = [pdf.get_y()] * num_columns