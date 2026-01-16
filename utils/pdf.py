import os
from fpdf import FPDF
from fpdf.enums import Align, XPos, YPos

# Optional: render LaTeX-like math (e.g., \frac{a}{b}) as images via matplotlib (headless).
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    _MATH_RENDER_AVAILABLE = True
except Exception:
    _MATH_RENDER_AVAILABLE = False

# Set up font paths (assumed to be correct)
FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts')
FONT_FILE_NORMAL = os.path.join(FONT_DIR, 'STIXTwoMath-Regular.ttf')
FONT_FILE_BOLD = os.path.join(FONT_DIR, 'STIXTwoMath-Regular.ttf')
FONT_FAMILY = "STIXTwoText-Regular"
LINE_SPACE_AFTER_TITLE = 15


class ACSLPDF(FPDF):
    """FPDF with a simple page footer: 'current/total' (e.g., 1/5)."""

    def footer(self):
        # Position at 15 mm from bottom
        self.set_y(-15)
        # Use the same font family (already registered in _create_pdf)
        try:
            self.set_font(FONT_FAMILY, "", 10)
        except Exception:
            # Fallback if font isn't set yet
            self.set_font("Helvetica", "", 10)
        self.set_text_color(80, 80, 80)
        self.cell(0, 10, f"{self.page_no()}/{{nb}}", align=Align.C)
        self.set_text_color(0, 0, 0)


def generate_pdf_files(
        project,
        problem_answer_list,
        num_column=1,
        row_spacing=20,
        output_dir: str | None = None,
):

    try:
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # Generate Problems PDF
        pdf_problems = _create_pdf(f"{project}")
        _add_content(
            pdf_problems,
            problem_answer_list,
            num_column,
            row_spacing,
            project
        )
        output_name = f"{project.replace(' ', '_')}.pdf"
        output_path = os.path.join(output_dir, output_name) if output_dir else output_name
        pdf_problems.output(output_path)
        print(f"***'{output_path}' has been created.")

    except FileNotFoundError as e:
        print(f"Error: {e}")


def _create_pdf(title):
    """Helper to create a new FPDF object with standard settings."""
    pdf = ACSLPDF('P', 'mm', 'Letter')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.alias_nb_pages()
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
    # Add a small gutter between columns so the text doesn't start right on the divider line.
    gutter = 6 if num_columns > 1 else 0
    total_width = pdf.w - 2 * margin - gutter * (num_columns - 1)
    col_width = total_width / num_columns
    start_y = pdf.get_y()
    column_y = [start_y] * num_columns

    math_cache_dir = os.path.join(os.getcwd(), ".pdf_math_cache")
    math_image_cache: dict[tuple[str, int], str] = {}

    def _looks_like_frac_only(s: str) -> bool:
        s = s.strip()
        return s.startswith("\\frac{") and s.endswith("}") and s.count("{") >= 2 and s.count("}") >= 2

    def _render_math_png(expr: str, font_size_pt: int) -> str | None:
        """
        Render math expression to a transparent PNG and return the path.
        Uses matplotlib mathtext (no external LaTeX installation required).
        """
        if not _MATH_RENDER_AVAILABLE:
            return None

        key = (expr, font_size_pt)
        if key in math_image_cache:
            return math_image_cache[key]

        os.makedirs(math_cache_dir, exist_ok=True)
        safe = (
            expr.replace("\\", "_")
            .replace("{", "_")
            .replace("}", "_")
            .replace("/", "_")
            .replace(" ", "_")
        )
        filename = f"math_{font_size_pt}_{abs(hash(expr))}_{safe[:30]}.png"
        path = os.path.join(math_cache_dir, filename)

        if not os.path.exists(path):
            fig = plt.figure(figsize=(0.01, 0.01), dpi=300)
            fig.patch.set_alpha(0.0)
            # Render as math: wrap in $...$
            fig.text(0, 0, f"${expr}$", fontsize=font_size_pt)
            fig.savefig(path, transparent=True, bbox_inches="tight", pad_inches=0.02)
            plt.close(fig)

        math_image_cache[key] = path
        return path

    def _draw_column_dividers(divider_start_y: float):
        """Draw dotted vertical divider lines between columns for readability."""
        if num_columns <= 1:
            return

        prev_line_width = getattr(pdf, "line_width", 0.2)
        prev_color = getattr(pdf, "draw_color", None)

        pdf.set_draw_color(180, 180, 180)
        pdf.set_line_width(0.3)

        y1 = divider_start_y
        y2 = pdf.h - pdf.b_margin
        for i in range(1, num_columns):
            # Draw in the middle of the gutter so both columns keep the same left padding.
            x = margin + i * (col_width + gutter) - (gutter / 2)
            # fpdf2 supports dashed_line; use small dash/space to look like dotted.
            try:
                pdf.dashed_line(x, y1, x, y2, dash_length=1, space_length=1)
            except AttributeError:
                # Fallback: solid line if dashed_line is unavailable.
                pdf.line(x, y1, x, y2)

        # restore styling
        if prev_color is not None and all(hasattr(prev_color, c) for c in ("r", "g", "b")):
            pdf.set_draw_color(prev_color.r, prev_color.g, prev_color.b)
        else:
            pdf.set_draw_color(0, 0, 0)
        pdf.set_line_width(prev_line_width)

    # Draw dividers on the first page before content
    _draw_column_dividers(start_y)

    def _start_new_page():
        pdf.add_page()
        if project_title:
            pdf.set_font(FONT_FAMILY, 'B', 16)
            pdf.cell(w=0, h=10, text=project_title, new_x=XPos.LMARGIN, new_y=YPos.TOP, align=Align.C)
            pdf.ln(LINE_SPACE_AFTER_TITLE)
        pdf.set_font(FONT_FAMILY, '', 14)
        new_start_y = pdf.get_y()
        _draw_column_dividers(new_start_y)
        return new_start_y, [new_start_y] * num_columns

    for i, content in enumerate(content_list):
        # Check for page break marker (None or "__PAGE_BREAK__")
        if content is None or (isinstance(content, str) and content.strip() == "__PAGE_BREAK__"):
            # Force a new page before continuing
            start_y, column_y = _start_new_page()
            continue
        
        col_index = i % num_columns

        # Prevent drawing into the bottom margin/footer area:
        # if this column is too low, start a new page BEFORE rendering.
        if column_y[col_index] > pdf.page_break_trigger - 20:
            start_y, column_y = _start_new_page()

        x_col = margin + col_index * (col_width + gutter)
        pdf.set_xy(x_col, column_y[col_index])

        # Using multi_cell for automatic line breaks
        prefix = f"{i + 1}) "
        content_str = str(content)

        # Special-case: render pure LaTeX fraction answers as an image so they appear as a real fraction.
        if _looks_like_frac_only(content_str):
            # Draw the prefix as text, then draw the fraction image to the right.
            x0 = x_col
            y0 = column_y[col_index]

            pdf.set_xy(x0, y0)
            pdf.cell(w=pdf.get_string_width(prefix), h=pdf.font_size * 1.2, text=prefix)

            expr = content_str.strip()
            # Smaller columns need smaller rendered math.
            if num_columns >= 6:
                font_size_pt = 11
                img_h_factor = 1.05
            elif num_columns >= 4:
                font_size_pt = 13
                img_h_factor = 1.15
            elif num_columns == 3:
                font_size_pt = 16
                img_h_factor = 1.4
            else:
                font_size_pt = 18
                img_h_factor = 1.6

            img_path = _render_math_png(expr, font_size_pt=font_size_pt)
            if img_path:
                # Determine image aspect ratio and place it nicely within the column.
                try:
                    img = mpimg.imread(img_path)
                    h_px, w_px = img.shape[0], img.shape[1]
                    aspect = (w_px / h_px) if h_px else 1.0
                except Exception:
                    aspect = 1.6

                img_h = pdf.font_size * img_h_factor
                img_w = min(col_width - pdf.get_string_width(prefix) - 2, img_h * aspect)
                img_x = x0 + pdf.get_string_width(prefix) + 1
                img_y = y0 - (img_h * 0.15)
                pdf.image(img_path, x=img_x, y=img_y, w=img_w, h=img_h)
                column_y[col_index] = y0 + row_spacing
                continue

        text = f"{prefix}{content_str}"

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
        # (page breaks are handled before rendering each item)