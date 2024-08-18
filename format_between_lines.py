import subprocess
import argparse

def extract_lines(file_path, start_line, end_line):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines[start_line-1:end_line]

def format_with_black(code):
    result = subprocess.run(
        ['black', '-', '-l', '100'],
        input="".join(code),
        text=True,
        capture_output=True,
    )
    return result.stdout

def lint_with_pylint(code):
    with open('temp_code.py', 'w') as temp_file:
        temp_file.writelines(code)

    subprocess.run(['pylint', 'temp_code.py'])
    subprocess.run(['rm', 'temp_code.py'])

def replace_lines(file_path, start_line, end_line, new_code):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    lines[start_line-1:end_line] = new_code

    with open(file_path, 'w') as file:
        file.writelines(lines)

def main(file_path, start_line, end_line):
    code_to_process = extract_lines(file_path, start_line, end_line)

    formatted_code = format_with_black(code_to_process)

    lint_with_pylint(formatted_code.splitlines(keepends=True))  # Linting after formatting

    replace_lines(file_path, start_line, end_line, formatted_code.splitlines(keepends=True))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Format and lint specific lines in a Python file.")
    parser.add_argument("file_path", type=str, help="Path to the Python file.")
    parser.add_argument("start_line", type=int, help="Starting line number (1-indexed).")
    parser.add_argument("end_line", type=int, help="Ending line number (inclusive, 1-indexed).")

    args = parser.parse_args()
    print(args)
    main(args.file_path, args.start_line, args.end_line)
