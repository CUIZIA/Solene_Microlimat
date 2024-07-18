import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom import minidom

def prettify(element):
    """Return a pretty-printed XML string for the Element."""
    rough_string = ET.tostring(element, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def dataframe_to_xml(df, xml_file):
    root = ET.Element("familles")
    
    for _, row in df.iterrows():
        famille = ET.SubElement(root, "famille")
        
        name = ET.SubElement(famille, "name")
        name.text = str(row["name"])
        
        classe = ET.SubElement(famille, "classe")
        classe.text = str(row["classe"])
        
        if pd.notna(row["albedo"]):
            albedo = ET.SubElement(famille, "albedo")
            albedo.text = str(row["albedo"])
            
        if pd.notna(row["transmittance"]):
            transmittance = ET.SubElement(famille, "transmittance")
            transmittance.text = str(row["transmittance"])
            
        if pd.notna(row["emissivite"]):
            emissivite = ET.SubElement(famille, "emissivite")
            emissivite.text = str(row["emissivite"])
        
        if pd.notna(row["materiau"]) and pd.notna(row["epaisseur"]):
            layers = ET.SubElement(famille, "layers")
            materials = str(row["materiau"]).split(';')
            thicknesses = str(row["epaisseur"]).split(';')
            
            for i, (materiau, epaisseur) in enumerate(zip(materials, thicknesses), start=1):
                layer = ET.SubElement(layers, "layer")
                
                position = ET.SubElement(layer, "position")
                position.text = str(i)
                
                materiau_el = ET.SubElement(layer, "materiau")
                materiau_el.text = materiau
                
                epaisseur_el = ET.SubElement(layer, "epaisseur")
                epaisseur_el.text = epaisseur
        
        if pd.notna(row["LAI"]):
            lai = ET.SubElement(famille, "LAI")
            lai.text = str(row["LAI"])
        
        if pd.notna(row["epaisseur_feuillage"]):
            epaisseur_feuillage = ET.SubElement(famille, "epaisseur_feuillage")
            epaisseur_feuillage.text = str(row["epaisseur_feuillage"])
            
        if pd.notna(row["coeff_extinction"]):
            coeff_extinction = ET.SubElement(famille, "coeff_extinction")
            coeff_extinction.text = str(row["coeff_extinction"])
            
        soleneID = ET.SubElement(famille, "soleneID")
        soleneID.text = str(row["soleneID"]) if pd.notna(row["soleneID"]) else "0"
        
        saturneID = ET.SubElement(famille, "saturneID")
        saturneID.text = str(row["saturneID"]) if pd.notna(row["saturneID"]) else "0"
        
    xml_str = prettify(root)
    
    lines = xml_str.split('\n')
    new_lines = []
    for line in lines:
        new_lines.append(line)
        if line.strip().endswith('</famille>'):
            new_lines.append('')
    pretty_xml_str = '\n'.join(new_lines)
    
    with open(xml_file, "w", encoding="utf-8") as f:
        f.write(pretty_xml_str)

# xls_file = "/Users/.../famille.xlsx" 
# xml_file = "/Users/.../famille.xml"
# df = pd.read_excel(xls_file)
# dataframe_to_xml(df, xml_file)
