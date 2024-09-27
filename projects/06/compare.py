import sys


def compare_files(file1_path, file2_path):
    with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
        lines1 = file1.readlines()
        lines2 = file2.readlines()

    # Compare line by line
    for line_num, (line1, line2) in enumerate(zip(lines1, lines2), start=1):
        if line1 != line2:
            print(
                f"Difference found at line {line_num}:\n{line1.strip()}\n{line2.strip()}\n")

    # Check for extra lines in one of the files
    if len(lines1) > len(lines2):
        for i in range(len(lines2), len(lines1)):
            print(
                f"Extra line in {file1_path} at line {i + 1}:\n{lines1[i].strip()}\n")
    elif len(lines1) < len(lines2):
        for i in range(len(lines1), len(lines2)):
            print(
                f"Extra line in {file2_path} at line {i + 1}:\n{lines2[i].strip()}\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_files.py <file1_path> <file2_path>")
        sys.exit(1)

    file1_path = sys.argv[1]
    file2_path = sys.argv[2]
    compare_files(file1_path, file2_path)
