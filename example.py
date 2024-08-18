"""Example module."""
import subprocess


def format_with_black(code):
    """Formats the given code using black."""
    result = subprocess.run(
        ["black", "-"],
        input="".join(code),
        text=True,
        capture_output=True,
    )
    return result.stdout
