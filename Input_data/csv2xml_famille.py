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

def add_optional_element(parent: ET.Element, tag: str, value) -> None:
    """
    Add an optional XML element if the value is not NaN.
    
    Args:
        parent (ET.Element): The parent element to add the child element to.
        tag (str): The tag name of the child element.
        value: The value to be added as text in the child element.
    """
    if pd.notna(value):
        child = ET.SubElement(parent, tag)
        child.text = str(int(value)) if isinstance(value, float) and value.is_integer() else str(value)

def dataframe_to_xml(df: pd.DataFrame, xml_file: str) -> None:
    """
    Convert a DataFrame to an XML file.
    
    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        xml_file (str): The path to the output XML file.
    """
    root = ET.Element("familles")
    
    for _, row in df.iterrows():
        famille = ET.SubElement(root, "famille")
        
        ET.SubElement(famille, "name").text = str(row["name"])
        ET.SubElement(famille, "classe").text = str(row["classe"])
        
        add_optional_element(famille, "albedo", row["albedo"])
        add_optional_element(famille, "transmittance", row["transmittance"])
        add_optional_element(famille, "emissivite", row["emissivite"])
        
        if pd.notna(row["materiau"]) and pd.notna(row["epaisseur"]):
            layers = ET.SubElement(famille, "layers")
            materials = str(row["materiau"]).split(';')
            thicknesses = str(row["epaisseur"]).split(';')
            
            for i, (materiau, epaisseur) in enumerate(zip(materials, thicknesses), start=1):
                layer = ET.SubElement(layers, "layer")
                ET.SubElement(layer, "position").text = str(i)
                ET.SubElement(layer, "materiau").text = materiau
                ET.SubElement(layer, "epaisseur").text = epaisseur
        
        add_optional_element(famille, "LAI", row["LAI"])
        add_optional_element(famille, "epaisseur_feuillage", row["epaisseur_feuillage"])
        add_optional_element(famille, "coeff_extinction", row["coeff_extinction"])
        
        ET.SubElement(famille, "soleneID").text = str(int(row["soleneID"])) if pd.notna(row["soleneID"]) else "0"
        ET.SubElement(famille, "saturneID").text = str(int(row["saturneID"])) if pd.notna(row["saturneID"]) else "0"
        
    xml_str = prettify(root)
    
    # Insert a blank line between <famille> elements for better readability
    pretty_xml_str = '\n\n'.join(xml_str.split('</famille>\n')).replace('\n\n<', '\n<')
    
    with open(xml_file, "w", encoding="utf-8") as f:
        f.write(pretty_xml_str)

if __name__ == "__main__":
    # Example usage
    xls_file = ".../famille.xlsx"  # Replace with your Excel file path
    xml_file = ".../famille.xml"   # Replace with your output XML file path
    
    try:
        df = pd.read_excel(xls_file)
        dataframe_to_xml(df, xml_file)
        print(f"XML file successfully created at: {xml_file}")
    except Exception as e:
        print(f"An error occurred: {e}")
