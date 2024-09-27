import sys
from JackAnalyzer import JackAnalyzer


def main():
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python Main.py <file_path>")
        sys.exit(1)

    # Extract the file path from the command-line arguments
    file_path = sys.argv[1]

    # Call the JackAnalyzer with the provided file path
    JackAnalyzer(file_path)


if __name__ == '__main__':

    file_path = sys.argv[1]
    JackAnalyzer(file_path)
