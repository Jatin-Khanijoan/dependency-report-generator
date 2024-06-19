import json
from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.set_text_color(40, 40, 40)
        self.cell(0, 10, "Dependency Analyzer Report", 0, 1, "C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

    def chapter_title(self, title):
        self.set_font("Arial", "B", 14)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, 0, 1, "L", 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font("Arial", "", 12)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 10, body)
        self.ln()


def generate_pdf(data, output_file):
    pdf = PDF()
    pdf.add_page()

    if "name" in data:
        pdf.chapter_title("name")
        pdf.chapter_body(data["name"])

    if "dependencies" in data:
        pdf.chapter_title("Dependencies")
        dependencies = "\n".join(
            [f"{key}: {value}" for key, value in data["dependencies"].items()]
        )
        pdf.chapter_body(dependencies)

    if "devDependencies" in data:
        pdf.chapter_title("Dev Dependencies")
        dev_dependencies = "\n".join(
            [f"{key}: {value}" for key, value in data["devDependencies"].items()]
        )
        pdf.chapter_body(dev_dependencies)

    if "version" in data:
        pdf.chapter_title("Version")
        pdf.chapter_body(data["version"])

    if "peerDependencies" in data:
        pdf.chapter_title("Peer Dependencies")
        peer_dependencies = "\n".join(
            [f"{key}: {value}" for key, value in data["peerDependencies"].items()]
        )
        pdf.chapter_body(peer_dependencies)

    pdf.output(output_file)


def main():
    with open("package.json", "r") as file:
        data = json.load(file)

    generate_pdf(data, "dependency_report.pdf")


if __name__ == "__main__":
    main()
