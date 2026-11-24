# Builds the English PDF report. This file is not part of the assignment code.
from pathlib import Path

from fpdf import FPDF

FOLDER = Path(__file__).resolve().parent
CODE_FILE = FOLDER / "titanic_analiz.py"
FIGURES = FOLDER / "figures"
PDF_PATH = FOLDER / "Project1_Titanic_Report.pdf"

ARIAL = r"C:\Windows\Fonts\arial.ttf"
ARIAL_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
CONSOLAS = r"C:\Windows\Fonts\consola.ttf"


class Report(FPDF):
    def header(self):
        self.set_y(8)
        self.set_font("Arial", "", 9)
        self.set_text_color(90, 90, 90)
        self.cell(
            0,
            6,
            "Project 1  |  Titanic Dataset Analysis  |  Ayşe Reyyan KÜÇÜKKARA  |  November 2, 2026",
            align="R",
            new_x="LMARGIN",
            new_y="NEXT",
        )
        self.set_draw_color(190, 190, 190)
        self.line(18, 16, 192, 16)
        self.set_text_color(0, 0, 0)
        self.set_y(22)

    def footer(self):
        self.set_y(-14)
        self.set_font("Arial", "", 9)
        self.set_text_color(90, 90, 90)
        self.cell(0, 8, str(self.page_no()), align="C")
        self.set_text_color(0, 0, 0)


def write_text(pdf, text, height, align="L"):
    pdf.multi_cell(
        0,
        height,
        text,
        align=align,
        new_x="LMARGIN",
        new_y="NEXT",
    )


def heading(pdf, text):
    pdf.set_font("Arial", "B", 13)
    pdf.ln(3)
    write_text(pdf, text, 7)
    pdf.ln(1)
    pdf.set_font("Arial", "", 11)


def paragraph(pdf, text):
    pdf.set_font("Arial", "", 11)
    write_text(pdf, text, 6)
    pdf.ln(2)


def bullet(pdf, text):
    pdf.set_font("Arial", "", 11)
    write_text(pdf, "-  " + text, 6)
    pdf.ln(1)


def write_code(pdf, lines):
    pdf.set_font("Consolas", "", 8)
    for line in lines:
        body = line.lstrip()
        if body.startswith("#"):
            pdf.set_text_color(46, 90, 58)
        else:
            pdf.set_text_color(25, 25, 25)
        pdf.set_fill_color(246, 246, 246)
        pdf.multi_cell(
            0,
            3.7,
            line if line else " ",
            fill=True,
            align="L",
            new_x="LMARGIN",
            new_y="NEXT",
        )
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)


def figure_page(pdf, number, title, filename, caption):
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    write_text(pdf, f"Figure {number}. {title}", 8)
    pdf.ln(2)
    pdf.image(str(FIGURES / filename), w=174)
    pdf.ln(4)
    pdf.set_font("Arial", "", 11)
    write_text(pdf, caption, 6)


def main():
    pdf = Report(format="A4", unit="mm")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(18, 22, 18)
    pdf.add_font("Arial", "", ARIAL)
    pdf.add_font("Arial", "B", ARIAL_BOLD)
    pdf.add_font("Consolas", "", CONSOLAS)
    pdf.add_page()

    pdf.set_font("Arial", "B", 22)
    pdf.ln(4)
    write_text(pdf, "Project 1", 10)
    pdf.set_font("Arial", "B", 16)
    write_text(pdf, "Titanic Dataset Analysis", 8)
    pdf.ln(2)
    pdf.set_draw_color(31, 78, 121)
    pdf.set_line_width(0.6)
    pdf.line(18, pdf.get_y(), 100, pdf.get_y())
    pdf.ln(6)

    pdf.set_font("Arial", "", 12)
    write_text(pdf, "Name: Ayşe Reyyan KÜÇÜKKARA", 7)
    write_text(pdf, "Date: November 2, 2026", 7)
    write_text(pdf, "Course: Artificial Intelligence", 7)
    write_text(pdf, "Task: Lecture 1, slide 64", 7)
    pdf.ln(1)

    heading(pdf, "Task")
    paragraph(
        pdf,
        "This report loads the Titanic dataset into a DataFrame, removes rows "
        "with empty cells, and creates the plots requested on slide 64.",
    )
    bullet(pdf, "Load the Titanic dataset and put it into a DataFrame.")
    bullet(pdf, "Clear the data by removing rows with empty cells.")
    bullet(pdf, "Show the passenger age distribution with a histogram.")
    bullet(pdf, "Show the number of victims and survivors in each class.")
    bullet(pdf, "Show the number of victims and survivors on each deck.")
    bullet(pdf, "Add two further plots: survival by sex, and fare by class.")

    heading(pdf, "Data cleaning")
    paragraph(
        pdf,
        "The seaborn Titanic table has 891 rows and 15 columns. After dropna "
        "removes every row with at least one empty cell, 182 rows remain. "
        "Most of the loss comes from missing deck values. Every plot below "
        "uses these 182 complete records, so second and third class are less "
        "represented than in the full passenger list.",
    )
    pdf.set_font("Arial", "", 11)
    write_text(pdf, "Original dataset: 891 rows", 6)
    write_text(pdf, "Cleaned dataset: 182 rows", 6)
    write_text(pdf, "Removed rows: 709", 6)
    write_text(pdf, "Remaining data: 20.43%", 6)
    pdf.ln(2)
    paragraph(
        pdf,
        "A total of 709 rows were removed because they contained at least one "
        "missing value. Only 20.43% of the original dataset remained after cleaning.",
    )

    heading(pdf, "Python code")
    paragraph(
        pdf,
        "The script that carries out the task is titanic_analiz.py. "
        "A comment above each command states what that command does. "
        "Blue bars are survivors and orange bars are victims.",
    )
    code = CODE_FILE.read_text(encoding="utf-8").splitlines()
    write_code(pdf, code)

    figure_page(
        pdf,
        1,
        "Passenger age distribution",
        "01_age_distribution.png",
        "The histogram shows the ages of the 182 passengers left after cleaning. "
        "Ages range from 0.92 to 80. The mean age is 35.6 and the median age "
        "is 36. The distribution is concentrated between 20 and 40, and the "
        "tallest bar is about 30 to 35 years. The bar near zero shows that "
        "the cleaned table still contains children. The curve is a smooth "
        "summary of the same distribution.",
    )
    figure_page(
        pdf,
        2,
        "Victims and survivors in each class",
        "02_survival_by_class.png",
        "In first class, 106 passengers survived and 51 died. In second class "
        "the counts are 12 survived and 3 died. In third class the counts are "
        "5 survived and 5 died. The second and third class bars are short "
        "because cabin information is often missing in those classes, and "
        "rows with empty cells were removed. Among the remaining records, "
        "first class dominates, and survivors outnumber victims.",
    )
    figure_page(
        pdf,
        3,
        "Victims and survivors on each deck",
        "03_survival_by_deck.png",
        "Deck B has 32 survivors and 11 victims. Deck C has 30 survivors and "
        "21 victims. Deck D has 23 survivors and 8 victims, and deck E has "
        "22 survivors and 8 victims. Deck A has 7 survivors and 5 victims, "
        "deck F has 7 survivors and 4 victims, and deck G has 2 survivors "
        "and 2 victims. On decks B, D, and E, survivors clearly outnumber victims.",
    )
    figure_page(
        pdf,
        4,
        "Victims and survivors by sex (extra plot)",
        "04_survival_by_sex.png",
        "This is the first of the two additional plots. Of the female "
        "passengers, 82 survived and 6 died. Of the male passengers, "
        "41 survived and 53 died. In the cleaned data, most women survived, "
        "while male victims outnumber male survivors.",
    )
    figure_page(
        pdf,
        5,
        "Fare by passenger class (extra plot)",
        "05_fare_by_class.png",
        "This is the second additional plot. The box plot summarizes how "
        "ticket fares are spread in each class. The median fare is 71.28 in "
        "first class, 13.00 in second class, and 10.46 in third class. "
        "First-class fares cover a much wider range and include outliers "
        "up to 512.33. Second and third class fares stay lower and tighter.",
    )

    pdf.add_page()
    heading(pdf, "Short conclusion")
    paragraph(
        pdf,
        "After empty rows were removed, the analysis covers 182 passengers. "
        "Ages cluster around a mean of 35.6. Survivors outnumber victims in "
        "first class and on decks B, C, D, and E. Almost all of the women "
        "survived, while more men died than survived. Fare also rises with "
        "class: the first-class median is well above the second-class and "
        "third-class medians.",
    )

    try:
        pdf.output(str(PDF_PATH))
        print(PDF_PATH)
    except PermissionError:
        # The report is open in the editor, so the original file cannot be replaced.
        alternate = PDF_PATH.with_name("Project1_Titanic_Report_updated.pdf")
        pdf.output(str(alternate))
        print(alternate)


if __name__ == "__main__":
    main()
