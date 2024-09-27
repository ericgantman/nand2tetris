def compare_asm_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    num_lines = min(len(lines1), len(lines2))
    for i in range(num_lines):
        if lines1[i].startswith("//") or lines2[i].startswith("//") or lines1[i] == (""):
            continue
        if lines1[i] != lines2[i]:
            print(
                f"Difference found at line {i + 1}:\n{file1}: {lines1[i]}{file2}: {lines2[i]}")
            return

    if len(lines1) != len(lines2):
        print("Files have different lengths.")
    else:
        print("Files are identical.")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python compare.py file1.asm file2.asm")
    else:
        file1 = sys.argv[1]
        file2 = sys.argv[2]
        compare_asm_files(file1, file2)
