import os

def find_dep_file(directory):
    req_files = ['requirements.txt', 'package.json', 'pom.xml', 'go.mod']
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file in req_files:
                return os.path.join(root, file)
    return None

def generate_report(dep_file, output_file):
    try:
        with open(dep_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                outfile.write(line)
        print(f"Report generated as {output_file}")
    except Exception as e:
        print(f"An error occurred while generating report {e}")

def main():
    project_folder = input("Enter the path of the project folder: ").strip()
    
    if not os.path.isdir(project_folder):
        print(f"The specified path '{project_folder}' is not a valid directory.")
        return

    dep_file = find_dep_file(project_folder)
    
    if dep_file:
        print(f"Dependencies file found: {dep_file}")
        analysis_file = os.path.join(os.getcwd(), 'report.txt')
        generate_report(dep_file, analysis_file)
    else:
        print("No dependencies file found in the specified project folder.")

if __name__ == "__main__":
    main()
