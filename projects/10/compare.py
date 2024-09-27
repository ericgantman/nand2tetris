import xml.etree.ElementTree as ET
import sys


def compare_xml(file1, file2):
    try:
        tree1 = ET.parse(file1)
        tree2 = ET.parse(file2)
    except ET.ParseError as e:
        print("Error parsing XML:", e)
        return False

    root1 = tree1.getroot()
    root2 = tree2.getroot()

    if root1.tag != root2.tag or root1.attrib != root2.attrib:
        print("Root elements are different")
        return False

    return compare_elements(root1, root2)


def compare_elements(elem1, elem2):
    if elem1.tag != elem2.tag or elem1.attrib != elem2.attrib:
        print("Elements are different:", elem1.tag, elem2.tag)
        return False

    if elem1.text != elem2.text:
        print("Text content is different:", elem1.text, elem2.text)
        return False

    if len(elem1) != len(elem2):
        print("Different number of child elements:", len(elem1), len(elem2))
        return False

    for child1, child2 in zip(elem1, elem2):
        if not compare_elements(child1, child2):
            return False

    return True


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare.py <file1.xml> <file2.xml>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    if compare_xml(file1, file2):
        print("XML files are identical")
    else:
        print("XML files are different")
