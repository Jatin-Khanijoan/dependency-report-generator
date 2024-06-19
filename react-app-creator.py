import json
import subprocess
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


def run_docker():
    dockerfile_content = """
        # Step 1: Use an official Node runtime as a parent image
        FROM node:14-alpine

        # Step 2: Set the working directory in the container
        WORKDIR /app

        # Step 3: Copy the package.json and package-lock.json files to the working directory
        COPY package*.json ./

        # Step 4: Install dependencies
        RUN npm install

        # Step 5: Copy the rest of the application code to the working directory
        COPY . .

        # Step 6: Build the React application for production
        RUN npm run build

        # Step 7: Install a simple web server to serve the React app
        RUN npm install -g serve

        # Step 8: Expose the port the app runs on
        EXPOSE 5000

        # Step 9: Command to run the app
        CMD ["serve", "-s", "build", "-l", "5000"]
        """
    with open("Dockerfile", "w") as file:
        file.write(dockerfile_content)
    build_command = "docker build -t react-app ."
    build_process = subprocess.run(build_command, shell=True, check=True)
    print("Docker image built successfully!")
    run_command = "docker run -p 5000:5000 react-app"
    run_process = subprocess.Popen(run_command, shell=True)
    print("Docker container running on http://localhost:5000")


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
    run_docker()


if __name__ == "__main__":
    main()
