from lxml import etree
import pickle
from region import Region
from svgpathtools import Document

pkl_path = "Files/MouseRegions.pkl"

def read_metadata(svg_path):
    tree = etree.parse(svg_path)
    root = tree.getroot()
    metadata = []
    return metadata

def get_region(structure_id, region_lookup):
    try:
        region = region_lookup[int(structure_id)]
        if region["has_children"] is False:
            return region
    except (KeyError, TypeError, ValueError):
        return None
    return None

def read_file(svg_path):
    with open(pkl_path, "rb") as f:
        region_lookup = pickle.load(f)

    parser = etree.XMLParser(huge_tree=True)
    tree = etree.parse(svg_path, parser)
    root = tree.getroot()
    doc = Document(svg_path) # Read svg using svgpathtools (applies any transforms / deformations)
    regions = {}

    for path in doc.paths(): 
        element = path.element
        structure_id = element.get("structure_id") # Extract allen id
        info = get_region(structure_id, region_lookup) # Look up allen id in pkl
      
        if not structure_id and info is None: continue # Sanity check, keep in idfk why

        structure_id = int(structure_id) # remove this lmao
        if structure_id not in regions:
            regions[structure_id] = Region(
                name=info["name"],
                parent=info["parent"],
                root=info["root"],
                paths=[]
            )
        regions[structure_id].add_path(path) # path already has SVG transforms applied
    return regions
