"""Formats and lints specific lines in a Python file."""

# pylint: disable=unspecified-encoding, broad-exception-caught
import logging
import subprocess
import argparse
from logging.handlers import RotatingFileHandler
handler = RotatingFileHandler("backend.log", maxBytes=50 * 1024 * 1024, backupCount=50)  # 50 MB
handler.setFormatter(
    logging.Formatter(
        "%(asctime)s - %(filename)s:%(lineno)d - %(funcName)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger = logging.getLogger(__name__)

def extract_lines(file_path, start_line, end_line):
    """Extracts the lines between the given start and end line numbers."""
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
        return lines[start_line - 1 : end_line]
    except Exception as error:
        logging.error("Error occurred while extracting lines: %s", error)

def format_with_black(code):
    """Formats the given code using black."""
    try:
        result = subprocess.run(
            ["black", "-", "-l", "100"],
            input="".join(code),
            text=True,
            check=True,
            capture_output=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as error:
        logging.error("Error occurred while formatting code: %s", error)
        raise
def lint_with_pylint(code):
    """Lints the given code using pylint."""
    with open("temp_code.py", "w") as temp_file:
        temp_file.writelines(code)

    try:
        result = subprocess.run(
            [
                "pylint",
                "temp_code.py",
                "--disable=missing-module-docstring,missing-function-docstring,invalid-name"
            ],
            check=False,  # Do not raise an exception for non-zero exit
            capture_output=True,
            text=True
        )
        logging.info("%s",result.stdout)  # Print pylint output
        logging.info("%s",result.stderr)  # Print any errors

        if result.returncode != 0:
            logging.error("Pylint found issues. Exit code: %s", result.returncode)
        else:
            logging.info("Pylint passed without issues.")
    except Exception as error:
        logging.error("An error occurred while running pylint: %s", error)
    finally:
        subprocess.run(["rm", "temp_code.py"], check=True)

def replace_lines(file_path, start_line, end_line, new_code):
    """Replaces the lines between the given start and end line numbers with the given new code."""
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()

        lines[start_line - 1 : end_line] = new_code

        with open(file_path, "w") as file:
            file.writelines(lines)
    except Exception as error:
        logging.error("Error occurred while replacing lines: %s", error)
def main(file_path, start_line, end_line):
    """Main function that formats and lints specific lines in a Python file."""
    try:
        code_to_process = extract_lines(file_path, start_line, end_line)
        code_str = "".join(code_to_process)
    except Exception as error:
        logging.error("Error occurred while extracting lines: %s", error)
    # Attempt to parse the code to ensure it's valid Python
    try:
        compile(code_str, "<string>", "exec")
    except SyntaxError as e:
        print(f"Code between lines {start_line} and {end_line} is incomplete or invalid: {e}")
        return
    try:
        # If the code is complete, format and lint it
        formatted_code = format_with_black(code_to_process)
        lint_with_pylint(formatted_code.splitlines(keepends=True))  # Linting after formatting
        replace_lines(file_path, start_line, end_line, formatted_code.splitlines(keepends=True))
    except Exception as error:
        logging.error("Error occurred while formatting and linting code: %s", error)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Format and lint specific lines in a Python file.")
    parser.add_argument("file_path", type=str, help="Path to the Python file.")
    parser.add_argument("start_line", type=int, help="Starting line number (1-indexed).")
    parser.add_argument("end_line", type=int, help="Ending line number (inclusive, 1-indexed).")

    args = parser.parse_args()
    main(args.file_path, args.start_line, args.end_line)
