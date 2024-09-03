import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom import minidom

def prettify(element: ET.Element) -> str:
    """
    Return a pretty-printed XML string for the Element.

    Args:
        element (ET.Element): The XML element to be formatted.

    Returns:
        str: A pretty-printed XML string.
    """
    rough_string = ET.tostring(element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def add_element_with_text(parent: ET.Element, tag: str, text: str) -> ET.Element:
    """
    Create an XML element with the specified text and append it to the parent element.

    Args:
        parent (ET.Element): The parent element to append the new element to.
        tag (str): The tag name of the new element.
        text (str): The text content of the new element.

    Returns:
        ET.Element: The newly created element.
    """
    child = ET.SubElement(parent, tag)
    child.text = text
    return child

def dataframe_to_xml(df: pd.DataFrame, xml_file: str) -> None:
    """
    Convert a DataFrame to an XML file.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        xml_file (str): The path to the output XML file.
    """
    root = ET.Element("materiaux")
    
    for _, row in df.iterrows():
        materiau = ET.SubElement(root, "materiau")
        
        add_element_with_text(materiau, "nom", str(row["nom"]))
        add_element_with_text(materiau, "conductivite", str(row["conductivite"]))
        add_element_with_text(materiau, "capacite_thermique", str(row["capacite_thermique"]))
        add_element_with_text(materiau, "masse_volumique", str(row["masse_volumique"]))
                
    xml_str = prettify(root)
    
    # Insert a blank line between <materiau> elements for better readability
    lines = xml_str.split('\n')
    new_lines = []
    for line in lines:
        new_lines.append(line)
        if line.strip().endswith('</materiau>'):
            new_lines.append('')
    pretty_xml_str = '\n'.join(new_lines)
    
    with open(xml_file, "w", encoding="utf-8") as f:
        f.write(pretty_xml_str)

if __name__ == "__main__":
    # Example usage
    xls_file = ".../materiau.xlsx"  # Replace with your Excel file path
    xml_file = ".../materiau.xml"   # Replace with your output XML file path
    
    try:
        df = pd.read_excel(xls_file)
        dataframe_to_xml(df, xml_file)
        print(f"XML file successfully created at: {xml_file}")
    except Exception as e:
        print(f"An error occurred: {e}")
